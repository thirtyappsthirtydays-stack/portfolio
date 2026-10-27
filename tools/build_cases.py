#!/usr/bin/env python3
"""Build cases/<id>.js from src/cases/<id>.html.

Each source file starts with a meta comment:
  <!--meta {"theme": {...}, "fonts": [...], "boards": ["ScreenHome", ...]} -->
followed by the page HTML. `<!--phasebar-->` marks where the sticky section bar goes.

The screens a page mounts (`<div class="plate" data-screen="...">`) are recreated boards kept in
the existing cases/<id>.js; `boards` in the meta lists which of them to keep. Extra or replacement
boards can be added in src/cases/<id>.boards.json (a list of board objects).
live, proto and carousel settings are carried over from the existing file unchanged.

Usage: python3 tools/build_cases.py [id ...]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_case(cid):
    src = open(os.path.join(ROOT, 'cases', cid + '.js'), encoding='utf-8').read()
    return json.loads(src[src.index('(') + 1:src.rindex(')')])


def build(cid):
    raw = open(os.path.join(ROOT, 'src', 'cases', cid + '.html'), encoding='utf-8').read()
    m = re.match(r'\s*<!--meta\s+(.*?)\s*-->', raw, re.S)
    if not m:
        raise SystemExit(cid + ': missing <!--meta ...--> header')
    meta = json.loads(m.group(1))
    html = raw[m.end():].strip()
    old = load_case(cid)
    boards = {b['id']: b for b in old.get('boards', [])}
    extra = os.path.join(ROOT, 'src', 'cases', cid + '.boards.json')
    if os.path.exists(extra):
        for b in json.load(open(extra, encoding='utf-8')):
            boards[b['id']] = b
    want = list(meta.get('boards', []))
    for key in ('carousel',):
        if old.get(key):
            want += [b for b in old[key]['boards'] if b not in want]
    used = set(re.findall(r'data-screen="([^"]+)"', html))
    missing = [b for b in used if b not in want]
    if missing:
        raise SystemExit(cid + ': screens used but not listed in meta boards: ' + ', '.join(missing))
    out = {'id': cid, 'fonts': meta.get('fonts', old.get('fonts', [])), 'theme': meta['theme'], 'html': html,
           'boards': [boards[b] for b in want if b in boards]}
    gone = [b for b in want if b not in boards]
    if gone:
        raise SystemExit(cid + ': boards not found: ' + ', '.join(gone))
    for key in ('live', 'proto', 'carousel'):
        if old.get(key):
            out[key] = old[key]
    js = 'window.__caseLoaded(' + json.dumps(out, ensure_ascii=False) + ');\n'
    open(os.path.join(ROOT, 'cases', cid + '.js'), 'w', encoding='utf-8').write(js)
    print('built', cid, len(js), 'bytes,', len(out['boards']), 'boards')


if __name__ == '__main__':
    ids = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(os.path.join(ROOT, 'src', 'cases'))) if f.endswith('.html')]
    for cid in ids:
        build(cid)
    # cache-busting: stamp each case file's content hash into index.html
    import hashlib, re
    idx = os.path.join(ROOT, 'index.html')
    html = open(idx, encoding='utf-8').read()
    vers = {}
    for f in sorted(os.listdir(os.path.join(ROOT, 'cases'))):
        if f.endswith('.js'):
            vers[f[:-3]] = hashlib.sha1(open(os.path.join(ROOT, 'cases', f), 'rb').read()).hexdigest()[:10]
    html = re.sub(r'var CASE_V = \{.*?\}; /\* case-versions \*/', 'var CASE_V = ' + json.dumps(vers) + '; /* case-versions */', html, count=1)
    open(idx, 'w', encoding='utf-8').write(html)
