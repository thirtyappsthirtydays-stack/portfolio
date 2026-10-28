"""Builds the Citi Self Invest iOS Screener as HTML boards.

Adds six 390 x 844 iPhone boards to src/cases/self-invest.boards.json, next to the web boards
that tools/screener_board.py writes:
  IOSResults    filtered results with two filter pills
  IOSFilters    fund filters as tiles, with the live results count
  IOSSheet      the Asset Class bottom sheet
  IOSSort       the Sort By sheet
  IOSQuestions  step 1 of the two pre-screen questions
  IOSTour       the first tour tooltip, on Filter
Fund data is illustrative, as the case study says. Run after screener_board.py.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 390, 844
BLUE, DARK, INK, INK2, RULE, BG = '#056DAE', '#002D72', '#0E1F3B', '#5A6B80', '#DCE3EC', '#F2F5F9'
GAIN, LOSS = '#1E7B34', '#D0312D'
FONT = "Overpass, 'Helvetica Neue', Arial, sans-serif"
SCRIM = 'rgba(14,31,59,.55)'


def icon(path, size=16, stroke=BLUE, sw=1.8, fill='none'):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')


BACK = '<path d="M15 5l-7 7 7 7"/>'
SEARCH = '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>'
INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 7.5v.5"/>'
CHEV_R = '<path d="M9 6l6 6-6 6"/>'
CHEV_L = '<path d="M15 6l-6 6 6 6"/>'
CHECK = '<path d="M5 12.5l4.5 4.5L19 7.5"/>'
CLOSE = '<path d="M6 6l12 12M18 6L6 18"/>'
SORT = '<path d="M4 6h10M4 12h7M4 18h4"/><path d="M18 5v14M15 16l3 3 3-3"/>'
FILTER = '<path d="M4 6h16M7 12h10M10 18h4"/>'
PULSE = '<path d="M3 12h4l2.5-6 4 12 2.5-6H21"/>'
PCT = '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>'

FUNDS = [
    # symbol, name, price, expense ratio, 1 year return, sparkline
    ('DBMF', 'iMGP DBi Managed Futures Strategy ETF', '$31.24', '0.89%', '+42.94%', [9, 8, 10, 7, 9, 6, 5, 3, 4, 2]),
    ('FTLS', 'First Trust Long/Short Equity ETF', '$50.05', '0.43%', '+8.32%', [7, 8, 6, 7, 5, 6, 4, 5, 4, 3]),
    ('MNA', 'IQ Merger Arbitrage ETF', '$31.24', '0.50%', '+14.14%', [8, 7, 8, 6, 7, 5, 6, 4, 3, 3]),
    ('QAI', 'IQ Hedge Multi-Strategy Tracker ETF', '$28.27', '0.79%', '+8.32%', [6, 7, 6, 5, 6, 5, 4, 5, 4, 4]),
    ('RLY', 'SPDR SSgA Multi-Asset Real Return ETF', '$29.14', '0.50%', '+6.71%', [8, 7, 8, 6, 7, 5, 6, 4, 5, 4]),
]


def spark(pts, up=True):
    w, h = 64, 24
    step = w / (len(pts) - 1)
    d = ' '.join(f'{i * step:.1f},{p * h / 10:.1f}' for i, p in enumerate(pts))
    c = GAIN if up else LOSS
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" style="display:block;overflow:visible">'
            f'<polyline points="{d}" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/></svg>')


def status(dark_bg=True):
    c = '#fff' if dark_bg else INK
    return (
        f'<div style="position:relative;height:50px;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0 34px;color:{c};font-size:15px;font-weight:600">'
        f'<span>9:41</span>'
        f'<span style="position:absolute;left:50%;top:11px;width:120px;height:34px;margin-left:-60px;border-radius:20px;background:#000"></span>'
        f'<span style="display:flex;align-items:center;gap:6px">'
        f'<svg width="18" height="11" viewBox="0 0 18 11" aria-hidden="true"><g fill="{c}"><rect x="0" y="7" width="3" height="4" rx=".8"/><rect x="5" y="5" width="3" height="6" rx=".8"/><rect x="10" y="2.5" width="3" height="8.5" rx=".8"/><rect x="15" y="0" width="3" height="11" rx=".8"/></g></svg>'
        f'<svg width="16" height="11" viewBox="0 0 16 11" aria-hidden="true"><path d="M8 10.5l2.2-2.6a3.2 3.2 0 0 0-4.4 0zM3.6 5.8a6.4 6.4 0 0 1 8.8 0l1.5-1.7a8.7 8.7 0 0 0-11.8 0zM.5 2.4a11 11 0 0 1 15 0" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/></svg>'
        f'<svg width="26" height="12" viewBox="0 0 26 12" aria-hidden="true"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="{c}" opacity=".45"/><rect x="2" y="2" width="19" height="8" rx="1.8" fill="{c}"/><rect x="24" y="4" width="1.6" height="4" rx=".8" fill="{c}" opacity=".45"/></svg>'
        f'</span></div>'
    )


def navbar(title, right=None):
    r = icon(right, 22, '#fff', 1.8) if right else '<span style="width:22px"></span>'
    return (f'<div style="height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;color:#fff">'
            f'{icon(BACK, 22, "#fff", 2)}<span style="font-size:17px;font-weight:700">{title}</span>{r}</div>')


def top(title, right=None):
    return f'<div style="background:{BLUE}">' + status() + navbar(title, right) + '</div>'


def home_bar(c=INK):
    return f'<span style="position:absolute;left:50%;bottom:8px;width:134px;height:5px;margin-left:-67px;border-radius:3px;background:{c}"></span>'


def screen(inner, bg='#fff'):
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};'
            f'font-family:{FONT};color:{INK};-webkit-font-smoothing:antialiased;display:flex;flex-direction:column">{inner}</div>')


def pill(t):
    return (f'<span style="display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 8px 0 13px;border-radius:15px;background:{BLUE};color:#fff;font-size:13px;font-weight:600">'
            f'{t}<span style="width:16px;height:16px;border-radius:50%;background:#fff;display:grid;place-items:center">{icon(CLOSE, 10, BLUE, 3.2)}</span></span>')


def fund_row(f, first=False):
    sym, name, price, er, r1, pts = f
    up = r1.startswith('+')
    return (
        f'<div{" id=\"row\"" if first else ""} style="display:grid;grid-template-columns:minmax(0,1fr) 64px 92px 18px;grid-template-rows:auto auto;column-gap:12px;row-gap:12px;align-items:center;padding:16px 16px 16px 18px;border-bottom:1px solid {RULE};background:#fff">'
        f'<span style="display:flex;flex-direction:column;gap:3px;min-width:0"><b style="font-size:15px;font-weight:700;color:{BLUE}">{sym}</b>'
        f'<span style="font-size:12px;color:{INK2};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</span></span>'
        f'<span>{spark(pts, up)}</span>'
        f'<span style="font-size:17px;font-weight:600;text-align:right">{price}</span>'
        f'<span style="grid-row:1 / span 2;grid-column:4">{icon(CHEV_R, 18, BLUE, 2)}</span>'
        f'<span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:13px;font-weight:600">{er}</b><span style="font-size:11.5px;color:{INK2}">Expense Ratio</span></span>'
        f'<span></span>'
        f'<span style="display:flex;flex-direction:column;gap:2px;text-align:right"><b style="font-size:13px;font-weight:700;color:{GAIN if up else LOSS}">{r1}</b><span style="font-size:11.5px;color:{INK2}">1 Year Return</span></span>'
        f'</div>'
    )


def results(title='Filtered Funds', pills=True, rows=5):
    p = (f'<div style="display:flex;gap:8px;padding:0 16px 14px">{pill("Asset Class")}{pill("Equity Style")}</div>' if pills else '')
    return (
        top('Fund Screener', SEARCH) +
        f'<div style="padding:18px 16px 6px"><span style="font-size:28px;line-height:1.15;font-weight:600">{title}</span></div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:0 16px 14px;font-size:12px;color:{INK2}">'
        f'<span>Refinitiv&nbsp;&nbsp;·&nbsp;&nbsp;As of May 20, 2023</span><span style="color:{BLUE};font-weight:600;text-decoration:underline">Disclosures</span></div>'
        f'<div id="controls" style="background:#fff">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 16px 14px">'
        f'<span style="display:flex;align-items:center;gap:7px;font-size:15px;font-weight:700;color:{BLUE}">{icon(SORT, 18, BLUE, 1.8)}Sort by</span>'
        f'<span id="filterbtn" style="display:flex;align-items:center;gap:7px;font-size:15px;font-weight:700;color:{BLUE}">{icon(FILTER, 18, BLUE, 2)}Filter</span></div>'
        + p + '</div>'
        f'<div style="border-top:1px solid {RULE}">' + ''.join(fund_row(f, i == 0) for i, f in enumerate(FUNDS[:rows])) + '</div>'
    )


def tile(name, n=0):
    if n:
        return (f'<span style="height:104px;border-radius:8px;background:{BLUE};color:#fff;display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:16px 8px 12px;text-align:center;box-shadow:0 2px 6px rgba(0,45,114,.18)">'
                f'<b style="font-size:13.5px;line-height:1.3;font-weight:700">{name}</b><span style="display:flex;align-items:center;gap:4px;font-size:11.5px;font-weight:600">{icon(CHECK, 12, "#fff", 3)}{n} Selected</span></span>')
    return (f'<span style="height:104px;border-radius:8px;background:#fff;border:1px solid {RULE};box-shadow:0 1px 4px rgba(0,45,114,.08);display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:16px 8px 12px;text-align:center">'
            f'<b style="font-size:13.5px;line-height:1.3;font-weight:600;color:{INK}">{name}</b><span style="font-size:11.5px;color:{INK2}">No Selection</span></span>')


def filters_body():
    def group(title, tiles, link=False):
        l = f'<span style="font-size:13px;font-weight:700;color:{BLUE};text-decoration:underline">Clear Filters</span>' if link else ''
        return (f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:18px 16px 10px">'
                f'<span style="font-size:14px;font-weight:700;color:{INK}">{title}</span>{l}</div>'
                f'<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding:0 16px">{"".join(tiles)}</div>')
    return (
        top('Fund Filters', INFO) +
        f'<div style="flex:1;background:{BG};position:relative">'
        f'<div id="tiles">' + group('Fund Categories', [tile('Asset Class', 1), tile('Equity Style', 2), tile('Market Cap'), tile('Target Asset Mix'), tile('Target Date'), tile('US Equity Sectors')], True) + '</div>'
        + group('Management and Expenses', [tile('Active vs. Passive'), tile('Benchmark Index'), tile('Expense Ratio')])
        + group('Additional Filters', [tile('Asset Style'), tile('Fund Type')]) +
        f'<div style="position:absolute;left:0;right:0;bottom:0;padding:26px 16px 30px;background:linear-gradient(rgba(242,245,249,0),{BG} 34%)">'
        f'<span id="viewbtn" style="height:50px;border-radius:8px;background:{BLUE};color:#fff;display:grid;place-items:center;font-size:16px;font-weight:700;box-shadow:0 4px 12px rgba(5,109,174,.3)">View 1,786 Results</span></div>'
        f'</div>'
    )


def sheet(inner, top_px):
    return (f'<div style="position:absolute;inset:0;background:{SCRIM}"></div>'
            f'<div style="position:absolute;left:0;right:0;top:{top_px}px;bottom:0;background:#fff;border-radius:16px 16px 0 0;box-shadow:0 -10px 30px rgba(0,0,0,.18);display:flex;flex-direction:column">'
            f'<span style="width:40px;height:5px;border-radius:3px;background:#C3CDDA;margin:8px auto 0;flex:none"></span>{inner}</div>')


def checkbox(label, on=False):
    box = (f'<span style="width:22px;height:22px;border-radius:5px;background:{BLUE};display:grid;place-items:center">{icon(CHECK, 15, "#fff", 3)}</span>'
           if on else f'<span style="width:22px;height:22px;box-sizing:border-box;border-radius:5px;border:2px solid #6F8197;background:#fff"></span>')
    return (f'<span style="display:flex;align-items:center;gap:14px;height:50px;border-bottom:1px solid {RULE};font-size:16px;color:{INK}">{box}{label}</span>')


def asset_sheet():
    opts = [('Alternatives', False), ('Bonds', False), ('Commodity', False), ('Equity', True), ('Mixed Assets', False), ('Money Market', False)]
    inner = (
        f'<div style="padding:14px 20px 0"><span style="display:block;font-size:20px;font-weight:700">Asset Class</span>'
        f'<span style="display:block;font-size:12.5px;color:{INK2};padding-top:4px">Choose one or more. Data provided by Refinitiv.</span></div>'
        f'<div style="padding:10px 20px 0">' + ''.join(checkbox(t, on) for t, on in opts) + '</div>'
        f'<div style="padding:22px 20px 0;display:flex;flex-direction:column;align-items:center;gap:16px">'
        f'<span style="width:100%;height:50px;border-radius:8px;background:{BLUE};color:#fff;display:grid;place-items:center;font-size:16px;font-weight:700">Apply</span>'
        f'<span style="font-size:15px;font-weight:700;color:{BLUE};text-decoration:underline">Deselect All</span></div>'
    )
    return screen(filters_body() + sheet(inner, 258) + home_bar(), BG)


def sort_sheet():
    def opt(t, on=False):
        right = (f'<span style="width:22px;height:22px;border-radius:50%;background:{BLUE};display:grid;place-items:center">{icon(CHECK, 13, "#fff", 3)}</span>'
                 if on else f'<span style="width:22px;height:22px;box-sizing:border-box;border-radius:50%;border:2px solid #A9B6C6"></span>')
        return (f'<span style="display:flex;justify-content:space-between;align-items:center;height:46px;border-top:1px solid {RULE};font-size:15px;font-weight:{700 if on else 500};color:{BLUE if on else INK}">{t}{right}</span>')
    inner = (
        f'<div style="padding:14px 20px 0;text-align:center"><span style="font-size:20px;font-weight:700">Sort By</span></div>'
        f'<div style="padding:16px 16px 0;display:flex;flex-direction:column;gap:12px">'
        f'<div style="border:2px solid {BLUE};border-radius:10px;padding:14px 16px 2px">'
        f'<span style="display:flex;align-items:center;gap:10px;font-size:16px;font-weight:700;color:{BLUE}">{icon(PULSE, 20, BLUE, 1.8)}Performance</span>'
        f'<span style="display:block;font-size:13px;line-height:1.45;color:{INK2};padding:8px 0 12px">Rate of return over a period of time, sorted from highest to lowest.</span>'
        + opt('1 Year Return', True) + opt('3 Year Return') + opt('5 Year Return') + opt('10 Year Return') +
        f'</div>'
        f'<div style="border:1px solid {RULE};border-radius:10px;padding:14px 16px 16px">'
        f'<span style="display:flex;align-items:center;gap:10px;font-size:16px;font-weight:700;color:{INK}">{icon(PCT, 20, BLUE, 1.8)}Expense Ratio</span>'
        f'<span style="display:block;font-size:13px;line-height:1.45;color:{INK2};padding-top:8px">Percentage of a fund’s assets used to cover its expenses, sorted from lowest to highest.</span>'
        f'</div></div>'
    )
    return screen(results() + sheet(inner, 196) + home_bar())


def questions():
    cats = [('Asset Class', 'Funds that invest in groups of securities with similar financial characteristics.'),
            ('Equity Style', 'US, international and global funds, classified by growth, value and core.'),
            ('Market Cap', 'Funds that invest in companies with similar market values.'),
            ('Target Asset Mix', 'Funds that hold a set mix of stocks, bonds and short-term investments.')]
    cards = ''.join(
        f'<div style="border:1px solid {RULE};border-radius:10px;padding:14px 16px;background:#fff;box-shadow:0 1px 4px rgba(0,45,114,.08);display:flex;align-items:center;gap:12px">'
        f'<span style="flex:1;display:flex;flex-direction:column;gap:5px"><b style="font-size:16px;font-weight:700;color:{BLUE}">{t}</b>'
        f'<span style="font-size:12.5px;line-height:1.45;color:{INK2}">{d}</span></span>{icon(CHEV_R, 18, BLUE, 2)}</div>' for t, d in cats)
    inner = (
        f'<div style="background:{BLUE};height:250px;flex:none;color:#fff">' + status() +
        f'<div style="display:flex;justify-content:flex-end;padding:6px 16px 0">{icon(CLOSE, 24, "#fff", 2)}</div>'
        f'<div style="padding:18px 24px 0;font-size:26px;line-height:1.2;font-weight:600">Welcome to Screener</div>'
        f'<div style="padding:8px 24px 0;font-size:14px;line-height:1.45;color:#D6E6F3">Two quick questions to get you started.</div></div>'
        f'<div style="margin:-56px 12px 0;background:#fff;border-radius:14px;box-shadow:0 8px 24px rgba(0,45,114,.16);padding:16px 14px 18px;display:flex;flex-direction:column;gap:10px">'
        f'<div style="display:flex;align-items:center;gap:8px;padding:0 2px"><span style="flex:1;height:4px;border-radius:2px;background:{BLUE}"></span><span style="flex:1;height:4px;border-radius:2px;background:{RULE}"></span>'
        f'<span style="font-size:12px;font-weight:600;color:{INK2};padding-left:4px">Step 1 of 2</span></div>'
        f'<div style="font-size:18px;line-height:1.35;font-weight:600;padding:6px 2px 4px">Which fund category would you like to start filtering by?</div>'
        + cards + '</div>'
        f'<div style="text-align:center;padding:18px 0 0;font-size:15px;font-weight:700;color:{BLUE};text-decoration:underline">Set my own filters instead</div>'
    )
    return screen(inner + home_bar(), BG)


def tip(pos='position:absolute;left:96px;right:12px;top:226px'):
    return (
        f'<div id="tip" style="{pos};background:#fff;border-radius:10px;box-shadow:0 10px 30px rgba(14,31,59,.28);padding:16px 16px 12px">'
        f'<span style="position:absolute;right:40px;top:-7px;width:14px;height:14px;background:#fff;transform:rotate(45deg)"></span>'
        f'<span style="position:absolute;right:12px;top:12px">{icon(CLOSE, 18, INK2, 2)}</span>'
        f'<b style="display:block;font-size:15px;font-weight:700;padding-right:24px">Select Filter</b>'
        f'<span style="display:block;font-size:13px;line-height:1.45;color:{INK2};padding-top:6px">Narrow down your results by selecting from a variety of fund categories and additional criteria.</span>'
        f'<span style="display:flex;justify-content:space-between;align-items:center;padding-top:14px">'
        f'<span style="display:flex;align-items:center;gap:2px;font-size:13px;font-weight:600;color:#A9B6C6">{icon(CHEV_L, 14, "#A9B6C6", 2)}Prev</span>'
        f'<span style="display:flex;gap:6px"><i style="width:7px;height:7px;border-radius:50%;background:{BLUE}"></i><i style="width:7px;height:7px;border-radius:50%;background:#C3CDDA"></i></span>'
        f'<span style="display:flex;align-items:center;gap:2px;font-size:13px;font-weight:700;color:{BLUE}">Next{icon(CHEV_R, 14, BLUE, 2.2)}</span></span></div>'
    )


def tour():
    # spotlight around the Filter control in the results header
    spot = (f'<div style="position:absolute;left:300px;top:173px;width:84px;height:40px;border-radius:12px;background:#fff;'
            f'box-shadow:0 0 0 900px {SCRIM};display:flex;align-items:center;justify-content:center;gap:7px;font-size:15px;font-weight:700;color:{BLUE}">'
            f'{icon(FILTER, 18, BLUE, 2)}Filter</div>')
    return screen(results('All Funds', pills=False) + spot + tip() + home_bar('#fff'))


def board(bid, title, html):
    return {'id': bid, 'title': title, 'w': W, 'h': H, 'lang': 'en', 'dir': None,
            'css': ':host{margin:0}\n*{box-sizing:border-box}\n', 'html': html,
            'fonts': ['https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,300..800;1,400..600&display=swap']}


BOARDS = [
    ('IOSResults', 'Filtered results on iPhone', lambda: screen(results() + home_bar())),
    ('IOSFilters', 'Fund filters on iPhone', lambda: screen(filters_body() + home_bar(), BG)),
    ('IOSSheet', 'Asset Class sheet on iPhone', asset_sheet),
    ('IOSSort', 'Sort By sheet on iPhone', sort_sheet),
    ('IOSQuestions', 'Pre-screen questions on iPhone', questions),
    ('IOSTour', 'Tour tooltip on iPhone', tour),
]

if __name__ == '__main__':
    out = os.path.join(ROOT, 'src', 'cases', 'self-invest.boards.json')
    boards = [b for b in json.load(open(out, encoding='utf-8')) if not b['id'].startswith('IOS')]
    boards += [board(i, t, f()) for i, t, f in BOARDS]
    json.dump(boards, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('wrote', out, [b['id'] for b in boards])
