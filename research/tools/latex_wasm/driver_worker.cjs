// Node worker-thread driver for the patched pdftex.js engine (emscripten pdftex + embedded texmf).
// Vendor files (pdftex-worker.js / .data / .mem) are loaded from workerData.vendorDir.
'use strict';
const { parentPort, workerData } = require('worker_threads');
const fs = require('fs');
const path = require('path');

const VENDOR_DIR = workerData.vendorDir;
globalThis.__LATEX_WASM_VENDOR_DIR__ = VENDOR_DIR; // engine resolves .mem relative to vendor

// ---- environment shims expected by the engine ----
globalThis.location = { pathname: '/pdftex.js/', origin: '' };
// noExitRuntime: keep the process alive after main() returns instead of process.exit()
globalThis.Module = { noExitRuntime: true };
globalThis.require = require;

// XHR shim: the engine fetches pdftex-worker.data through XHR; serve it from disk.
function XHRShim() {
  this.readyState = 0; this.status = 0; this.response = null;
  this.responseType = ''; this.onload = null; this.onerror = null; this.onprogress = null;
  this.addedTotal = false; this._url = '';
}
XHRShim.prototype.open = function (method, url) { this._url = url; };
XHRShim.prototype.setRequestHeader = function () {};
XHRShim.prototype.send = function () {
  const self = this;
  try {
    const name = path.basename(String(this._url).split('?')[0]);
    const buf = fs.readFileSync(path.join(VENDOR_DIR, name));
    const u8 = new Uint8Array(buf.length);
    u8.set(buf);
    this.response = this.responseType === 'arraybuffer' ? u8.buffer : u8;
    this.status = 200;
    if (this.onprogress) this.onprogress({ total: buf.length, loaded: buf.length });
    if (this.onload) this.onload({ target: this });
  } catch (e) {
    this.status = 0;
    if (this.onerror) this.onerror(e);
  }
};
globalThis.XMLHttpRequest = XHRShim;

// ---- message plumbing ----
const listeners = [];
globalThis.addEventListener = function (type, fn) {
  if (type === 'message') listeners.push(fn);
};
globalThis.postMessage = function (m) { parentPort.postMessage(m); };
globalThis.self = globalThis;
parentPort.on('message', function (d) {
  listeners.forEach(function (fn) { fn({ data: d }); });
});

process.on('uncaughtException', (e) => {
  try { parentPort.postMessage({ type: 'err', value: 'UNCAUGHT: ' + ((e && e.stack) || e) }); } catch (_) {}
  setTimeout(() => process.exit(0), 200);
});
process.on('unhandledRejection', (e) => {
  try { parentPort.postMessage({ type: 'err', value: 'UNHANDLED REJECTION: ' + ((e && e.stack) || e) }); } catch (_) {}
});
// ---- load the patched engine ----
const code = fs.readFileSync(path.join(VENDOR_DIR, 'pdftex-worker.js'), 'utf8');
(0, eval)(code);


// The engine posts 'ready' only when its preloaded data package arrives
// asynchronously; with our synchronous disk-backed XHR shim everything is ready
// by the time eval returns, and 'ready' is never posted. Emit it ourselves.
setTimeout(() => {
  try { parentPort.postMessage({ type: 'log', value: '[driver] Module.noExitRuntime=' + (globalThis.Module && globalThis.Module.noExitRuntime) + ' ENV_NODE=' + globalThis.ENVIRONMENT_IS_NODE + ' calledRun=' + (globalThis.Module && globalThis.Module.calledRun) }); } catch (_) {}
  parentPort.postMessage({ type: 'ready' });
}, 800);
