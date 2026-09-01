#!/usr/bin/env node
// Offline LaTeX validation compiler for the Wind Energy Science manuscripts.
//
// The sandbox/user machine may lack a TeX distribution; this harness compiles the
// .tex manuscripts with the pdftex.js engine (emscripten pdftex + embedded texmf)
// running in Node worker threads. Copernicus-class commands are emulated by
// copernicus_local.sty, booktabs by booktabs.sty (local shims), and the bibliography
// is injected as a thebibliography block generated from refs.bib.
//
// Usage: node compile.mjs <paper.tex> [--out out.pdf] [--passes 2]
// Expects: vendor/ (pdftex-worker.js/.data/.mem), ./copernicus_local.sty, ./booktabs.sty,
//          ../papers/refs.bib, figures under ../ws_submodularity/.
import { Worker } from 'worker_threads';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import { dirname, join, basename, resolve } from 'path';
import { fileURLToPath } from 'url';

const HERE = dirname(fileURLToPath(import.meta.url));
const PAPERS = resolve(HERE, '../../papers');
const WS = resolve(HERE, '../../ws_submodularity');
const VENDOR = join(HERE, 'vendor');
const STY = join(HERE, '.');

function b64(path) { return readFileSync(path).toString('base64'); }

function runPass({ source, extraFiles, readBack, cwd }) {
  return new Promise((resolveP, rejectP) => {
    const worker = new Worker(join(HERE, 'driver_worker.cjs'), {
      workerData: { vendorDir: VENDOR },
    });
    const logs = [];
    let finished = false;
    let started = false;
    const timer = setTimeout(() => {
      if (!finished) {
        worker.terminate();
        rejectP(new Error('pass timeout'));
      }
    }, 300000);
    worker.on('message', (m) => {
      if (m.type === 'log') logs.push(m.value);
      else if (m.type === 'err') logs.push('ERR: ' + m.value);
      else if (m.type === 'ready') {
        worker.postMessage({ type: 'start', source, extraFiles, readBack });
      } else if (m.type === 'finish') {
        finished = true;
        clearTimeout(timer);
        const v = m.value || {};
        const out = {
          success: !!v.success,
          log: (logs.concat([v.log || ''])).join('\n'),
          pdf: v.pdf ? Buffer.from(v.pdf, 'base64') : null,
          files: {},
        };
        for (const [k, val] of Object.entries(v.files || {})) {
          out.files[k] = val ? Buffer.from(val, 'base64') : null;
        }
        worker.terminate();
        resolveP(out);
      }
    });
    worker.on('error', (e) => {
      if (!finished) { finished = true; clearTimeout(timer); rejectP(e); }
    });
    worker.on('exit', (code) => {
      if (!finished) {
        finished = true; clearTimeout(timer);
        rejectP(new Error('worker exited: ' + code + '\n--- worker log ---\n' + logs.join('\n')));
      }
    });
  });
}

function preprocess(tex, bibBlock) {
  let s = tex;
  if (/\\documentclass\[[^\]]*\]\{copernicus\}/.test(s)) {
    s = s.replace(/\\documentclass\[[^\]]*\]\{copernicus\}/, '\\documentclass[11pt]{article}');
  } else if (/\\documentclass\{copernicus\}/.test(s)) {
    s = s.replace(/\\documentclass\{copernicus\}/, '\\documentclass[11pt]{article}');
  }
  // article class + shim
  s = s.replace(/(\\documentclass[^\n]*\})/, `$1\n\\usepackage{copernicus_local}`);
  // the embedded texmf lacks amssymb/amsthm: strip and rely on the shim
  s = s.replace(/\\usepackage\{([^}]*\bamssymb\b[^}]*)\}/, (m, g) => {
    const rest = g.split(',').map(x => x.trim()).filter(x => x && x !== 'amssymb' && x !== 'amsthm');
    return rest.length ? '\\usepackage{' + rest.join(', ') + '}' : '% amssymb stripped (local build)';
  });
  // bibliography -> thebibliography
  s = s.replace(/\\bibliography\{[^}]*\}[^\n]*\n?/, '');
  s = s.replace(/\\bibliographystyle\{[^}]*\}[^\n]*\n?/, '');
  s = s.replace(/\\end\{document\}/, bibBlock + '\n\n\\end{document}');
  // figure paths: ../ws_submodularity/X -> /ws_submodularity/X
  s = s.split('../ws_submodularity/').join('/ws_submodularity/');
  return s;
}

function analyzeLog(log) {
  const errors = (log.match(/^![^\n]*/gm) || []).filter(l => !/^!\s*$/.test(l));
  const undefinedRefs = log.match(/LaTeX Warning: Reference [`'][^`']+[`'] on page \d+ undefined/g) || [];
  const undefinedCites = log.match(/LaTeX Warning: Citation [`'][^`']+[`'] on page \d+ undefined/g) || [];
  const rerun = log.match(/LaTeX Warning: (Label\(s\)|There were undefined references)/g) || [];
  const overfull = log.match(/Overfull \\hbox \([^)]*\)/g) || [];
  const missingPng = log.match(/! LaTeX Error: File `[^`']+' not found/g) || [];
  return { errors, undefinedRefs, undefinedCites, rerun, overfull, missingPng };
}

async function main() {
  const args = process.argv.slice(2);
  if (!args[0]) { console.error('usage: node compile.mjs <paper.tex> [--out out.pdf] [--passes N]'); process.exit(2); }
  const texPath = resolve(args[0]);
  let outPath = null, passes = 2;
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--out') outPath = resolve(args[++i]);
    else if (args[i] === '--passes') passes = parseInt(args[++i], 10);
  }
  if (!outPath) {
    outPath = join(PAPERS, 'compiled_pdfs', basename(texPath).replace(/\.tex$/, '_local.pdf'));
  }
  if (!existsSync(VENDOR + '/pdftex-worker.js')) {
    console.error('vendor files missing; run setup.sh first');
    process.exit(2);
  }

  // bibliography (only the keys actually cited in this paper)
  const bibPy = join(HERE, 'bib2thebibliography.py');
  const texSrc0 = readFileSync(texPath, 'utf8');
  const cited = new Set();
  for (const m of texSrc0.matchAll(/\\cite[pt]?(?:\[[^\]]*\])?\{([^}]+)\}/g)) {
    for (const k of m[1].split(',')) cited.add(k.trim());
  }
  const bibBlock = execSync(
    `python3 ${bibPy} ${join(PAPERS, 'refs.bib')} ${[...cited].join(',')}`
  ).toString();
  console.error(`[compile] bibliography: ${cited.size} cited keys injected`);

  // figures
  const figFiles = readdirSync(WS).filter(f => f.endsWith('.png'));
  const extraBase = [
    { path: '/copernicus_local.sty', b64: b64(join(STY, 'copernicus_local.sty')) },
    { path: '/booktabs.sty', b64: b64(join(STY, 'booktabs.sty')) },
  ];
  for (const f of figFiles) {
    extraBase.push({ path: '/ws_submodularity/' + f, b64: b64(join(WS, f)) });
  }

  const source = preprocess(texSrc0, bibBlock);
  console.error('[compile] pass 1 ...');
  const p1 = await runPass({ source, extraFiles: extraBase, readBack: ['/input.aux'] });
  if (!p1.success) {
    console.error('[compile] PASS 1 FAILED\n' + p1.log);
    process.exit(1);
  }
  const aux = p1.files['/input.aux'];
  let last = p1;
  for (let p = 2; p <= passes; p++) {
    const files = extraBase.slice();
    if (aux) files.push({ path: '/input.aux', b64: aux.toString('base64') });
    console.error(`[compile] pass ${p} ...`);
    last = await runPass({ source, extraFiles: files, readBack: ['/input.aux'] });
    if (!last.success) {
      console.error(`[compile] PASS ${p} FAILED\n` + last.log);
      process.exit(1);
    }
  }
  const report = analyzeLog(last.log);
  mkdirSync(dirname(outPath), { recursive: true });
  writeFileSync(outPath, last.pdf);
  writeFileSync(outPath.replace(/\.pdf$/, '.log'), last.log);
  console.error('[compile] OK -> ' + outPath);
  console.error('[compile] errors: ' + report.errors.length +
    ' | undefined refs: ' + report.undefinedRefs.length +
    ' | undefined cites: ' + report.undefinedCites.length +
    ' | overfull: ' + report.overfull.length);
  for (const e of report.errors) console.error('   ' + e.trim());
  for (const u of report.undefinedRefs.concat(report.undefinedCites, report.missingPng)) console.error('   ' + u);
  if (report.errors.length || report.undefinedRefs.length || report.undefinedCites.length) process.exit(3);
}

main().catch(e => { console.error(e); process.exit(1); });
