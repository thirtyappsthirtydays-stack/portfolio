#!/usr/bin/env python3
"""Build src/cases/bofa.boards.json from the Capital Workbench concept screens.

The three screens are kept as design-canvas files in src/boards/bofa/*.dc.html. This turns each
into a fixed-size board (1440px wide) for the Bank of America case study: the {{accent}} tweaks
become plain colours, links to other screens become "#", and the board height is measured in a
headless browser so nothing is clipped.

Usage: python3 -B tools/bofa_boards.py [--fonts DIR]
  --fonts DIR  a folder with IBM Plex woff2 files (e.g. node_modules/@fontsource), so the height is
               measured with the real typeface. Without it the fallback font is used.
Then: python3 -B tools/build_cases.py bofa
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'boards', 'bofa')
OUT = os.path.join(ROOT, 'src', 'cases', 'bofa.boards.json')
W = 1440
FONTS = ['https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap']
BOARDS = [
    ('BofaOverview', 'Overview.dc.html', 'Overview: the quarter-end capital position'),
    ('BofaRules', 'Rules.dc.html', 'Rule detail: threshold deductions'),
    ('BofaRecon', 'Reconciliation.dc.html', 'Reconciliation against the spreadsheet model'),
]


def mix(hex_a, hex_b, t):
    a = [int(hex_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(hex_b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join('%02X' % round(x + (y - x) * t) for x, y in zip(a, b))


ACCENT = '#24508F'
HOLES = {'accent': ACCENT, 'accentTint': mix(ACCENT, '#FFFFFF', 0.55), 'accentSoft': mix(ACCENT, '#FCFCFB', 0.9)}


def convert(path):
    raw = open(path, encoding='utf-8').read()
    body = raw[raw.index('<x-dc>') + len('<x-dc>'):raw.index('</x-dc>')]
    helmet = re.search(r'<helmet>(.*?)</helmet>', body, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S).strip()
    css = re.search(r'<style>(.*?)</style>', helmet, re.S).group(1)
    css = '\n'.join(l for l in css.strip().splitlines() if not l.startswith('body{'))
    css = ':host{margin:0}\nbutton,input{font:inherit}\n' + css + '\n'
    body = re.sub(r'\{\{\s*(\w+)\s*\}\}', lambda m: HOLES[m.group(1)], body)
    body = re.sub(r'href="[A-Za-z]+\.dc\.html"', 'href="#"', body)
    body = re.sub(r'\s+\n', '\n', body)
    if 'min-height: 100vh;' not in body:
        raise SystemExit(path + ': root min-height not found')
    return css, body


def measure(boards, font_dir):
    from playwright.sync_api import sync_playwright
    faces = ''
    if font_dir:
        for fam, slug, weights in (('IBM Plex Sans', 'ibm-plex-sans', (400, 500, 600)), ('IBM Plex Mono', 'ibm-plex-mono', (400, 500))):
            for w in weights:
                f = os.path.join(font_dir, slug, 'files', '%s-latin-%d-normal.woff2' % (slug, w))
                faces += "@font-face{font-family:'%s';font-weight:%d;src:url('file://%s')}\n" % (fam, w, f)
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={'width': W, 'height': 900})
        for bid, (css, html) in boards.items():
            page = '<!doctype html><html><head><style>body{margin:0}%s%s</style></head><body>%s</body></html>' % (faces, css.replace(':host{margin:0}', ''), html.replace('min-height: 100vh;', ''))
            pg.set_content(page)
            pg.evaluate('document.fonts.ready')
            out[bid] = pg.evaluate('document.body.firstElementChild.getBoundingClientRect().height')
        br.close()
    return out


def main():
    font_dir = None
    if '--fonts' in sys.argv:
        font_dir = sys.argv[sys.argv.index('--fonts') + 1]
    converted = {bid: convert(os.path.join(SRC, f)) for bid, f, _ in BOARDS}
    heights = measure(converted, font_dir)
    boards = []
    for bid, f, title in BOARDS:
        css, html = converted[bid]
        h = int(-(-heights[bid] // 8) * 8) + 16  # round up, with a little room for font differences
        html = html.replace('min-height: 100vh;', 'position: relative; width: %dpx; height: %dpx; overflow: hidden;' % (W, h), 1)
        boards.append({'id': bid, 'title': title, 'w': W, 'h': h, 'lang': 'en', 'dir': None, 'css': css, 'html': html, 'fonts': FONTS})
        print(bid, W, 'x', h)
    json.dump(boards, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)


if __name__ == '__main__':
    main()
