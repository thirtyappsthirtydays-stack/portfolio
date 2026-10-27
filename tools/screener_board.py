"""Builds the Citi Self Invest web Screener as HTML boards.

Writes src/cases/self-invest.boards.json with two states of the same page:
  ScreenerWeb         results with the row actions menu open
  ScreenerWebFilters  the Add Filters dialog open over the results
Fund data is illustrative, as the case study says.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 800
BLUE, DARK, INK, INK2, RULE, BG = '#056DAE', '#002D72', '#0E1F3B', '#5A6B80', '#DCE3EC', '#F2F5F9'
GAIN, LOSS = '#1E7B34', '#D0312D'
FONT = "Overpass, 'Helvetica Neue', Arial, sans-serif"


def icon(path, size=16, stroke=BLUE, sw=1.8, fill='none'):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')


SEARCH = '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>'
CHEV_D = '<path d="M6 9l6 6 6-6"/>'
CHEV_R = '<path d="M9 6l6 6-6 6"/>'
INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 7.5v.5"/>'
PLUS_C = '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'
CHECK = '<path d="M5 12.5l4.5 4.5L19 7.5"/>'
CLOSE = '<path d="M6 6l12 12M18 6L6 18"/>'
USER = '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>'
PIN = '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>'
CHART = '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M6 16l4-5 3 3 5-6"/>'
CAL = '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'
GEAR = '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M5.6 18.4l1.8-1.8M16.6 7.4l1.8-1.8"/>'

FUNDS = [
    # symbol, name, price, expense, 1y, 3y, 5y, 10y
    ('ABL', 'AllianceBernstein…', '$302.76', '0.40%', '-13.68%', '+7.23%', '+5.21%', '+13.50%'),
    ('DFA', 'Dimensional…', '$48.12', '0.19%', '-10.37%', '-10.37%', '-10.37%', '-10.37%'),
    ('DSI', 'Domini Social…', '$73.37', '1.71%', '-5.75%', '+16.13%', '+9.02%', '+11.84%'),
    ('GSPX', 'S&P 500 UCIT…', '$6.85', '0.12%', '-12.68%', '-12.68%', '+6.40%', '+12.15%'),
    ('IVN', 'iShares S&P 5…', '$140.21', '0.18%', '-2.94%', '+16.79%', '+13.94%', '+13.94%'),
    ('MML', 'MML Investme…', '$51.25', '0.12%', '+3.98%', '-1.57%', '+8.41%', '+8.41%'),
    ('NTI', 'Northern Trus…', '$72.67', '0.69%', '-34.42%', '+1.57%', '+3.56%', '+3.56%'),
]
COLS = '86px 96px 98px 90px 90px 90px 90px 1fr'


def pct(v):
    c = GAIN if v.startswith('+') else LOSS
    return f'<span style="color:{c};text-align:right">{v}</span>'


def header():
    nav = ['Accounts', 'Payments &amp; Transfers', 'Services', 'Explore Products', 'Rewards &amp; Offers']
    items = ''.join(f'<span>{n}</span>' for n in nav)
    return (
        f'<div style="height:62px;background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 48px">'
        f'<span style="font-size:30px;line-height:1;font-weight:800;letter-spacing:-.04em;color:{BLUE}">citi</span>'
        f'<span style="display:flex;gap:28px;color:{INK2};font-size:9px;font-weight:600;letter-spacing:.06em">'
        f'<span style="display:flex;flex-direction:column;align-items:center;gap:3px">{icon(USER,20,INK2,1.5)}PROFILE</span>'
        f'<span style="display:flex;flex-direction:column;align-items:center;gap:3px">{icon(PIN,20,INK2,1.5)}ATM / BRANCH</span></span></div>'
        f'<div style="height:42px;background:{DARK};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 48px;font-size:12.5px;font-weight:600">'
        f'<span style="display:flex;gap:30px;align-items:center">{items}<span style="display:flex;align-items:center;gap:4px">Open an Account {icon(CHEV_R,13,"#fff",2.2)}</span></span>'
        f'<span style="display:flex;gap:22px;align-items:center"><span style="display:flex;align-items:center;gap:7px">{icon(SEARCH,15,"#fff",2)}How can we help?</span>'
        f'<span style="width:1px;height:18px;background:rgba(255,255,255,.35)"></span><span>Sign Off</span></span></div>'
    )


def checkbox(label, on=False):
    box = (f'<span style="width:15px;height:15px;border-radius:3px;background:{BLUE};display:grid;place-items:center">{icon(CHECK,12,"#fff",3)}</span>'
           if on else f'<span style="width:15px;height:15px;box-sizing:border-box;border-radius:3px;border:1.5px solid #6F8197;background:#fff"></span>')
    return f'<span style="display:flex;align-items:center;gap:10px;height:28px;font-size:13px;color:{INK}">{box}{label}</span>'


def left_panel():
    return (
        f'<div style="width:300px;flex:none;box-sizing:border-box;background:#fff;border:1px solid {RULE};border-radius:6px;padding:20px 22px 24px;display:flex;flex-direction:column">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:14px;border-bottom:1px solid {RULE}">'
        f'<span style="font-size:24px;line-height:1.2;font-weight:400;color:{INK}">Screener</span>{icon(INFO,20,BLUE,1.6)}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:18px 0 10px">'
        f'<span style="font-size:15px;font-weight:700;color:{INK}">Fund Categories</span><span style="font-size:11.5px;color:#9AA8B8">Clear Filters</span></div>'
        f'<span style="font-size:10.5px;font-weight:700;color:{INK2};padding-bottom:4px">Asset Class</span>'
        + ''.join(checkbox(x) for x in ['Alternatives', 'Bonds', 'Commodity', 'Equity', 'Mixed Assets', 'Money Market']) +
        f'<div style="border-top:1px solid {RULE};margin-top:14px;padding-top:18px;font-size:15px;font-weight:700;color:{INK}">Additional Filters</div>'
        f'<span style="font-size:10.5px;font-weight:700;color:{INK2};padding:12px 0 4px">Fund Type</span>'
        + checkbox('ETFs', True) + checkbox('Mutual Funds', True) +
        f'<span style="display:flex;align-items:center;gap:8px;margin-top:18px;font-size:13px;font-weight:700;color:{BLUE}">{icon(PLUS_C,18,BLUE,1.6)}Add Filters</span>'
        f'</div>'
    )


def lookup():
    return (
        f'<div style="background:#fff;border:1px solid {RULE};border-radius:6px;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:20px">'
        f'<span style="display:flex;align-items:center;gap:14px;font-size:13.5px;font-weight:600;color:{INK}">{icon(CHART,30,BLUE,1.4)}Investment Lookup</span>'
        f'<span style="width:440px;height:38px;box-sizing:border-box;border:1px solid {RULE};border-radius:4px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:12.5px;font-weight:600;color:{BLUE}">'
        f'Enter a Symbol or Name to Look Up{icon(SEARCH,17,BLUE,2)}</span></div>'
    )


def results(menu=True):
    head = ''.join(f'<span style="text-align:{"left" if i == 0 else "right"}">{h}</span>' for i, h in enumerate(
        ['Symbol', 'Last Price', 'Expense Ratio', '1Y Return', '3Y Return', '5Y Return', '10Y Return', '']))
    rows = ''
    for i, (sym, name, price, er, y1, y3, y5, y10) in enumerate(FUNDS):
        bg = '#F4F8FC' if (menu and i == 1) else '#fff'
        rows += (
            f'<div style="display:grid;grid-template-columns:{COLS};align-items:center;height:52px;padding:0 16px;border-top:1px solid {RULE};background:{bg};font-size:13px;color:{INK}">'
            f'<span style="display:flex;flex-direction:column;gap:2px"><b style="font-weight:700;color:{BLUE}">{sym}</b><span style="font-size:10.5px;color:{INK2}">{name}</span></span>'
            f'<span style="text-align:right">{price}</span><span style="text-align:right">{er}</span>'
            f'{pct(y1)}{pct(y3)}{pct(y5)}{pct(y10)}'
            f'<span style="text-align:right;color:{BLUE};font-size:18px;line-height:1;letter-spacing:1px">•••</span></div>'
        )
    tooltip = ''
    actions = ''
    if menu:
        tooltip = (f'<span style="position:absolute;left:96px;top:226px;padding:7px 12px;background:#fff;border:1px solid {RULE};border-radius:4px;'
                   f'box-shadow:0 4px 12px rgba(0,45,114,.12);font-size:11.5px;color:{INK}">Dimensional ETF Trust Dimension</span>')
        sec = lambda t: f'<span style="font-size:10.5px;font-weight:700;color:{INK2};padding:2px 0 6px">{t}</span>'
        link = lambda ic, t: f'<span style="display:flex;align-items:center;gap:9px;height:30px;font-size:12.5px;font-weight:700;color:{BLUE}">{icon(ic,17,BLUE,1.7)}{t}</span>'
        actions = (
            f'<div style="position:absolute;right:14px;top:244px;width:250px;box-sizing:border-box;background:#fff;border:1px solid {RULE};border-radius:6px;'
            f'box-shadow:0 10px 28px rgba(0,45,114,.16);padding:14px 16px 10px;display:flex;flex-direction:column">'
            + sec('Trade') +
            f'<span style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding-bottom:12px">'
            f'<span style="height:34px;border-radius:4px;background:{BLUE};color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700">Buy</span>'
            f'<span style="height:34px;border-radius:4px;background:{BLUE};color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700">Sell</span></span>'
            + sec('Auto Invest') + link(CAL, 'Set up Auto Invest') + link(GEAR, 'Manage Auto Investments') +
            f'<span style="height:1px;background:{RULE};margin:8px 0 10px"></span>' + sec('Watchlist') + link(PLUS_C, 'Add to Watchlist') +
            f'</div>'
        )
    field = lambda label, text, ic: (
        f'<span style="display:flex;flex-direction:column;gap:5px;flex:1"><span style="font-size:10.5px;font-weight:700;color:{INK2}">{label}</span>'
        f'<span style="height:38px;box-sizing:border-box;border:1px solid {RULE};border-radius:4px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:12.5px;font-weight:700;color:{BLUE}">{text}{ic}</span></span>')
    return (
        f'<div style="position:relative;background:#fff;border:1px solid {RULE};border-radius:6px;flex:1;min-height:0;display:flex;flex-direction:column;overflow:visible">'
        f'<div style="padding:16px 16px 0;display:flex;gap:16px">{field("Sort by", "Select", icon(CHEV_D,18,BLUE,2))}{field("Search", "Search within results", icon(SEARCH,17,BLUE,2))}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 16px 12px">'
        f'<span style="display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 12px 0 6px;border-radius:13px;background:{BLUE};color:#fff;font-size:11.5px;font-weight:700">'
        f'<span style="width:16px;height:16px;border-radius:50%;background:#fff;display:grid;place-items:center">{icon(CLOSE,10,BLUE,3)}</span>Fund Type</span>'
        f'<span style="display:flex;flex-direction:column;align-items:flex-end;gap:2px;font-size:10.5px;color:{INK2}"><span>As of Jul 08, 2020 at 10:50 AM ET</span><span>1,377 Results</span></span></div>'
        f'<div style="display:grid;grid-template-columns:{COLS};padding:10px 16px;font-size:10.5px;font-weight:700;color:{INK2}">{head}</div>'
        f'{rows}{tooltip}{actions}</div>'
    )


def filters_dialog():
    def chip(t, on=False):
        if on:
            return (f'<span style="height:34px;box-sizing:border-box;border-radius:4px;background:{BLUE};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 10px 0 14px;font-size:12px;font-weight:600">'
                    f'{t}<span style="width:18px;height:18px;border-radius:50%;background:#fff;display:grid;place-items:center">{icon(CHECK,12,BLUE,3)}</span></span>')
        return (f'<span style="height:34px;box-sizing:border-box;border-radius:4px;border:1px solid {RULE};box-shadow:0 1px 3px rgba(0,45,114,.08);display:flex;align-items:center;justify-content:space-between;padding:0 10px 0 14px;font-size:12px;font-weight:600;color:{INK}">'
                f'{t}<svg width="19" height="19" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="{BLUE}"/><path d="M12 7.5v9M7.5 12h9" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg></span>')

    def group(title, chips):
        return (f'<span style="font-size:10.5px;font-weight:700;letter-spacing:.12em;color:{INK2};padding:18px 0 10px">{title}</span>'
                f'<span style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 24px">{"".join(chips)}</span>')
    return (
        f'<div style="position:absolute;inset:0;background:rgba(14,31,59,.55);display:flex;justify-content:center;align-items:flex-start;padding-top:76px">'
        f'<div style="width:720px;box-sizing:border-box;background:#fff;border-radius:4px;box-shadow:0 24px 60px rgba(0,0,0,.3);padding:34px 40px 34px;position:relative;display:flex;flex-direction:column">'
        f'<span style="position:absolute;right:26px;top:24px">{icon(CLOSE,24,BLUE,1.8)}</span>'
        f'<span style="font-size:30px;line-height:1.2;font-weight:600;color:{INK}">Add Filters</span>'
        f'<span style="font-size:12.5px;color:{INK2};padding-top:6px">Your selected filters will display on the left side of the page.</span>'
        + group('FUND CATEGORIES', [chip('Asset Class', True), chip('Equity Style'), chip('Market Cap'), chip('Target Asset Mix'), chip('Target Date'), chip('US Equity Sectors')])
        + group('MANAGEMENT AND EXPENSES', [chip('Active vs. Passive'), chip('Benchmark Index'), chip('Expense Ratio')])
        + group('ADDITIONAL FILTERS', [chip('Asset Class'), chip('Fund Type', True)]) +
        f'<span style="display:flex;align-items:center;gap:8px;padding-top:22px;font-size:12.5px;color:{INK}">{icon(INFO,17,BLUE,1.6)}Not sure which filter to choose? <span style="color:{BLUE};font-weight:600;text-decoration:underline">Go to our Glossary.</span></span>'
        f'<span style="display:flex;align-items:center;gap:22px;padding-top:28px">'
        f'<span style="height:38px;padding:0 22px;border-radius:4px;background:{BLUE};color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700">Apply</span>'
        f'<span style="font-size:13px;font-weight:700;color:{BLUE};text-decoration:underline">Reset</span></span>'
        f'</div></div>'
    )


def page(menu=True, dialog=False):
    body = (
        f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{BG};font-family:{FONT};color:{INK};-webkit-font-smoothing:antialiased">'
        + header() +
        f'<div style="padding:16px 48px 0;font-size:12px;color:{BLUE}">Overview <span style="color:{INK2}">&nbsp;›&nbsp; Screener</span></div>'
        f'<div style="display:flex;gap:20px;padding:16px 48px 0;align-items:flex-start;height:{H - 62 - 42 - 32}px;box-sizing:border-box">'
        + left_panel() +
        f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:16px;height:100%">' + lookup() + results(menu) + '</div></div>'
        + (filters_dialog() if dialog else '') +
        '</div>'
    )
    return body


def board(bid, title, html):
    return {'id': bid, 'title': title, 'w': W, 'h': H, 'lang': 'en', 'dir': None,
            'css': ':host{margin:0}\n*{box-sizing:border-box}\n', 'html': html,
            'fonts': ['https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,300..800;1,400..600&display=swap']}


if __name__ == '__main__':
    boards = [board('ScreenerWeb', 'Screener on the web', page(menu=True)),
              board('ScreenerWebFilters', 'Add Filters on the web', page(menu=False, dialog=True))]
    out = os.path.join(ROOT, 'src', 'cases', 'self-invest.boards.json')
    json.dump(boards, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('wrote', out)
