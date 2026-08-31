#!/usr/bin/env python3
"""Convert refs.bib to a natbib-style thebibliography block for local validation
compiles (no bibtex binary in the wasm toolchain). Author-year labels follow the
Copernicus/Natbib convention: "Surname, YYYY" / "A and B, YYYY" / "A et al., YYYY".
"""
import re
import sys


def parse_bib(path):
    text = open(path, encoding="utf-8").read()
    entries = []
    for m in re.finditer(
        r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}', text, re.S
    ):
        etype, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for fm in re.finditer(r'(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}', body, re.S):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append((key, etype, fields))
    return entries


def parse_authors(s):
    # split on " and " (case-insensitive), tolerate trailing commas
    s = re.sub(r'\s+', ' ', s)
    parts = [p.strip().rstrip(',') for p in re.split(r'\s+and\s+', s, flags=re.I)]
    out = []
    for p in parts:
        if not p:
            continue
        if ',' in p:  # "Surname, First"
            surname = p.split(',')[0].strip()
        else:  # "First Last"
            toks = p.split()
            surname = toks[-1].strip()
        # keep LaTeX accents intact (e.g. Tak\'a\v{c}); no bare braces in our bib authors
        out.append(surname)
    return out


def author_text(names, max_before_et_al=4):
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} et al."


def latex_escape(s):
    s = re.sub(r'(?<!\\\\)[{}]', '', s)  # strip unescaped braces only (keep \\v{c} etc.)
    s = s.replace('&', '\\&').replace('%', '\\%').replace('#', '\\#').replace('_', '\\_')
    return s


def main(bib_path, only_keys=None):
    entries = parse_bib(bib_path)
    if only_keys:
        entries = [e for e in entries if e[0] in only_keys]
    lines = ["\\begin{thebibliography}{99}"]
    n = 0
    for key, etype, f in entries:
        authors = parse_authors(f.get('author', f.get('editor', '')))
        if not authors:
            authors = ['Anon']
        year = f.get('year', 'n.d.')
        label = f"{author_text(authors)}, {year}"
        atext = author_text(authors, max_before_et_al=99)
        title = latex_escape(f.get('title', ''))
        body = [f"{atext}: {title}."]
        if 'journal' in f:
            body.append(latex_escape(f['journal']))
        elif 'booktitle' in f:
            body.append("In: " + latex_escape(f['booktitle']))
        if f.get('volume'):
            body.append(f['volume'].replace('--', '-'))
        if f.get('number'):
            body.append(f"({f['number']})")
        if f.get('pages'):
            body.append(f['pages'])
        if 'publisher' in f and 'journal' not in f and 'booktitle' not in f:
            body.append(latex_escape(f['publisher']))
        if 'institution' in f:
            body.append(latex_escape(f['institution']))
        body.append(year + '.')
        if f.get('doi'):
            body.append(f"\\doi{{{f['doi']}}}.")
        text = ', '.join(b for b in body if b)
        text = re.sub(r', (\d{4}\.)', r', \1', text)
        text = re.sub(r'\s+', ' ', text)
        lines.append(f"\\bibitem[{label}]{{{key}}} {text}")
        n += 1
    lines.append("\\end{thebibliography}")
    return "\n".join(lines), n


if __name__ == '__main__':
    only = None
    if len(sys.argv) > 2 and sys.argv[2].strip():
        only = set(k.strip() for k in sys.argv[2].split(','))
    out, n = main(sys.argv[1], only)
    sys.stderr.write(f"[bib2thebibliography] {n} entries\n")
    print(out)
