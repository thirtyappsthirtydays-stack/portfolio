"""Builds the Citi Self Invest greyscale (mid-fidelity) Screener designs as HTML boards.

Adds five 960 x 500 boards to src/cases/self-invest.boards.json, one per carousel slide in Develop:
  GreyAddFilters  the Add Filters dialog, grouped chips
  GreyPills       results with the active-filter pills called out
  GreyRowMenu     the actions menu open on a row
  GreyTour        tour steps 1 and 2 of 4, on the left panel
  GreyQuestions   welcome, then the two pre-screen questions
Fund data is illustrative, as the case study says. Run after screener_board.py.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 960, 500
INK, INK2, INK3, RULE, PAGE, CANVAS, DARK, MID = '#1C1C1C', '#5C5C5C', '#8A8A8A', '#D9D9D9', '#F4F4F4', '#E3E6E9', '#262626', '#4A4A4A'
ACC = '#056DAE'  # annotation colour, not part of the greyscale UI
FONT = "Overpass, 'Helvetica Neue', Arial, sans-serif"


def icon(path, size=16, stroke=INK, sw=1.8, fill='none'):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')


CLOSE = '<path d="M6 6l12 12M18 6L6 18"/>'
CHECK = '<path d="M5 12.5l4.5 4.5L19 7.5"/>'
SEARCH = '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>'
INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 7.5v.5"/>'
CHEV_D = '<path d="M6 9l6 6 6-6"/>'
CHEV_R = '<path d="M9 6l6 6-6 6"/>'
PLUS_C = '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>'
BULB = '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.1v.1h5v-.1c0-.8.4-1.6 1.1-2.1A6 6 0 0 0 12 3z"/>'
CAL = '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'
GEAR = '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.5M12 18.5V21M3 12h2.5M18.5 12H21M5.6 5.6l1.8 1.8M16.6 16.6l1.8 1.8M5.6 18.4l1.8-1.8M16.6 7.4l1.8-1.8"/>'
CHART = '<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M6 16l4-5 3 3 5-6"/>'
ARROW = '<path d="M4 12h15M14 6l6 6-6 6"/>'

FUNDS = [
    ('ABL', 'AllianceBernstein…', '$302.76', '0.40%', '-13.68%', '+7.23%', '+5.21%', '+13.50%'),
    ('DFA', 'Dimensional F…', '$23.91', '0.19%', '-10.37%', '-10.37%', '-10.37%', '-10.37%'),
    ('DSI', 'Domini Social…', '$73.37', '1.71%', '-5.75%', '+16.13%', '+11.00%', '+11.00%'),
    ('GSPX', 'S&amp;P 500 UCIT…', '$6.85', '0.12%', '-12.68%', '-12.68%', '-12.68%', '-12.68%'),
    ('IVW', 'iShares S&amp;P 5…', '$140.21', '0.18%', '-2.94%', '+16.79%', '+13.94%', '+13.94%'),
    ('MML', 'MML Investme…', '$51.25', '0.12%', '+3.98%', '-1.57%', '+8.41%', '+10.41%'),
    ('NTI', 'Northern Trus…', '$72.67', '0.69%', '-34.42%', '+1.57%', '+3.56%', '+3.56%'),
]


def frame(inner, bg=CANVAS):
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};'
            f'font-family:{FONT};color:{INK};-webkit-font-smoothing:antialiased">{inner}</div>')


def callout(x, y, w, h, label, lx, ly, r=22):
    """A dashed ring around part of the design, with a short label."""
    return (f'<span style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:2px dashed {ACC};border-radius:{r}px"></span>'
            f'<span style="position:absolute;left:{lx}px;top:{ly}px;padding:4px 10px;border-radius:6px;background:{ACC};color:#fff;font-size:12px;font-weight:700;white-space:nowrap">{label}</span>')


def checkbox(label, on=False, size=15, fs=13.5, h=27):
    box = (f'<span style="width:{size}px;height:{size}px;border-radius:3px;background:{MID};display:grid;place-items:center;flex:none">{icon(CHECK, size - 4, "#fff", 3)}</span>'
           if on else f'<span style="width:{size}px;height:{size}px;box-sizing:border-box;border-radius:3px;border:1.5px solid {INK2};background:#fff;flex:none"></span>')
    return f'<span style="display:flex;align-items:center;gap:10px;height:{h}px;font-size:{fs}px;color:{INK}">{box}{label}</span>'


# 1 ------------------------------------------------------------------ Add Filters dialog
def add_filters():
    def chip(t, on=False):
        if on:
            return (f'<span style="height:36px;border-radius:5px;background:{DARK};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 10px 0 14px;font-size:13px;font-weight:600">'
                    f'{t}<span style="width:20px;height:20px;border-radius:50%;background:#fff;display:grid;place-items:center">{icon(CHECK, 13, DARK, 3)}</span></span>')
        return (f'<span style="height:36px;border-radius:5px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.14);display:flex;align-items:center;justify-content:space-between;padding:0 10px 0 14px;font-size:13px;font-weight:600;color:{INK}">'
                f'{t}<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10.5" fill="{DARK}"/><path d="M12 7.5v9M7.5 12h9" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg></span>')

    def group(title, chips):
        return (f'<span style="display:block;font-size:11px;font-weight:700;letter-spacing:.14em;color:{INK2};padding:16px 0 9px">{title}</span>'
                f'<span style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 26px">{"".join(chips)}</span>')
    dialog = (
        f'<div style="position:absolute;left:150px;top:14px;width:660px;height:472px;background:#fff;border-radius:6px;box-shadow:0 10px 34px rgba(0,0,0,.16);display:flex;flex-direction:column">'
        f'<div style="padding:24px 34px 0;position:relative;flex:1">'
        f'<span style="position:absolute;right:24px;top:20px">{icon(CLOSE, 22, INK, 1.8)}</span>'
        f'<span style="display:block;font-size:28px;line-height:1.15;font-weight:700">Add Filters</span>'
        f'<span style="display:block;font-size:13px;color:{INK2};padding:6px 0 12px;border-bottom:1px solid {RULE}">Your selected filters will display on the left side of the page.</span>'
        + group('FUND CATEGORIES', [chip('Asset Class'), chip('Equity Style'), chip('Market Cap'), chip('Target Asset Mix'), chip('Target Date'), chip('US Equity Sectors')])
        + group('MANAGEMENT AND EXPENSES', [chip('Active vs. Passive'), chip('Benchmark Index'), chip('Expense Ratio')])
        + group('ADDITIONAL FILTERS', [chip('Asset Style'), chip('Fund Type', True)]) +
        f'<span style="display:flex;align-items:center;justify-content:center;gap:8px;padding-top:16px;font-size:13px;color:{INK}">{icon(BULB, 18, INK2, 1.6)}Not sure which filter to choose? <span style="text-decoration:underline">Go to our Glossary.</span></span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:24px;padding:14px 34px;border-top:1px solid {RULE}">'
        f'<span style="height:38px;padding:0 20px;border-radius:5px;background:{DARK};color:#fff;display:grid;place-items:center;font-size:14px;font-weight:700">Apply</span>'
        f'<span style="font-size:14px;font-weight:700;text-decoration:underline">Reset</span></div></div>'
    )
    return frame(dialog)


# shared page parts for slides 2 and 3
def left_panel(x, y, w, h):
    return (
        f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:14px 18px;box-sizing:border-box;overflow:hidden">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid {RULE}"><span style="font-size:21px">Screener</span>{icon(INFO, 18, INK2, 1.6)}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:12px 0 6px"><span style="font-size:14px;font-weight:700">Fund Categories</span><span style="font-size:11.5px;font-weight:700;text-decoration:underline">Clear Filters</span></div>'
        f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:2px">Asset Class</span>'
        + ''.join(checkbox(t, on, 14, 12.5, 24) for t, on in [('Alternatives', True), ('Bonds', False), ('Commodity', True), ('Equity', True), ('Mixed Assets', False), ('Money Market', False)]) +
        f'<div style="border-top:1px solid {RULE};margin-top:8px;padding-top:10px"><span style="display:block;font-size:14px;font-weight:700;padding-bottom:6px">Additional Filters</span>'
        f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:2px">Fund Type</span>'
        + checkbox('ETFs', True, 14, 12.5, 24) + checkbox('Mutual Funds', True, 14, 12.5, 24) +
        f'<span style="display:flex;align-items:center;gap:8px;padding-top:10px;font-size:13px;font-weight:700">{icon(PLUS_C, 18, INK2, 1.5)}Add Filters</span></div></div>'
    )


COLS = 'minmax(0,1.2fr) repeat(6,minmax(0,1fr)) 30px'


def table_rows(funds, highlight=None):
    rows = ''
    for i, f in enumerate(funds):
        sym, name = f[0], f[1]
        cells = ''.join(f'<span style="text-align:right;font-size:13.5px">{v}</span>' for v in f[2:])
        dots = (f'<span style="justify-self:end;width:26px;height:26px;border-radius:50%;background:{INK if highlight == i else "transparent"};display:grid;place-items:center">'
                f'<svg width="18" height="6" viewBox="0 0 18 6" aria-hidden="true"><g fill="none" stroke="{"#fff" if highlight == i else INK2}" stroke-width="1.3"><circle cx="3" cy="3" r="2"/><circle cx="9" cy="3" r="2"/><circle cx="15" cy="3" r="2"/></g></svg></span>')
        rows += (f'<div style="display:grid;grid-template-columns:{COLS};gap:0 10px;align-items:center;height:52px;border-top:1px solid {RULE}">'
                 f'<span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:13.5px;font-weight:600;text-decoration:underline;text-decoration-color:{INK3}">{sym}</b><span style="font-size:11px;color:{INK2}">{name}</span></span>{cells}{dots}</div>')
    return rows


def table_head():
    labels = ['Last Price', 'Expense Ratio', '1Y Return', '3Y Return', '5Y Return', '10Y Return']
    return (f'<div style="display:grid;grid-template-columns:{COLS};gap:0 10px;align-items:center;height:34px;font-size:11.5px;font-weight:700;color:{INK}">'
            f'<span>Symbol</span>' + ''.join(f'<span style="text-align:right;white-space:nowrap">{l}</span>' for l in labels) + '<span></span></div>')


# 2 ------------------------------------------------------------------ pills called out
def pills():
    def pill(t):
        return (f'<span style="display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 12px 0 6px;border-radius:13px;background:{MID};color:#fff;font-size:12px;font-weight:600">'
                f'<span style="width:15px;height:15px;border-radius:50%;background:#fff;display:grid;place-items:center">{icon(CLOSE, 9, MID, 3.4)}</span>{t}</span>')
    x0 = 286
    right = (
        f'<div style="position:absolute;left:{x0}px;top:40px;right:20px;height:58px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.08);display:flex;align-items:center;justify-content:space-between;padding:0 16px">'
        f'<span style="display:flex;align-items:center;gap:12px;font-size:14px;font-weight:600">{icon(CHART, 26, INK2, 1.4)}Investment Lookup</span>'
        f'<span style="width:300px;height:36px;border:1px solid {RULE};border-radius:5px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:12.5px;font-weight:600">Enter a Symbol or Name to Look Up{icon(SEARCH, 16, INK2, 1.6)}</span></div>'
        f'<div style="position:absolute;left:{x0}px;top:110px;right:20px;bottom:-10px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:12px 16px 0">'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">'
        f'<span style="display:flex;flex-direction:column;gap:4px"><span style="font-size:11px;font-weight:600">Sort by</span><span style="height:34px;border:1px solid {RULE};border-radius:5px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:13px;font-weight:700">Select{icon(CHEV_D, 16, INK2, 1.6)}</span></span>'
        f'<span style="display:flex;flex-direction:column;gap:4px"><span style="font-size:11px;font-weight:600">Search</span><span style="height:34px;border:1px solid {RULE};border-radius:5px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;font-size:13px;font-weight:700">Search within results{icon(SEARCH, 16, INK2, 1.6)}</span></span></div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:14px 0 10px">'
        f'<span style="display:flex;gap:8px">{pill("Asset Class")}{pill("Fund Type")}</span>'
        f'<span style="text-align:right;font-size:11px;line-height:1.5;color:{INK2}">As of Jul 08, 2020 at 10:50 AM ET<br>1,377 Results</span></div>'
        + table_head() + table_rows(FUNDS[:4]) + '</div>'
    )
    crumb = f'<span style="position:absolute;left:20px;top:12px;font-size:12.5px;color:{INK2}">Overview &nbsp;›&nbsp; Screener</span>'
    note = callout(x0 + 8, 185, 222, 38, 'One pill per active filter', x0 + 242, 193)
    return frame(crumb + left_panel(20, 40, 252, 470) + right + note, PAGE)


# 3 ------------------------------------------------------------------ row actions menu
def row_menu():
    tbl = (f'<div style="position:absolute;left:20px;top:16px;right:20px;bottom:-10px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:4px 18px 0">'
           + table_head() + table_rows(FUNDS, highlight=1) + '</div>')
    item = lambda ic, t: f'<span style="display:flex;align-items:center;gap:10px;height:36px;font-size:14.5px;font-weight:700">{icon(ic, 20, INK2, 1.5)}{t}</span>'
    head = lambda t: f'<span style="display:block;font-size:11.5px;font-weight:600;color:{INK2};padding:12px 0 6px">{t}</span>'
    menu = (f'<div style="position:absolute;right:26px;top:140px;width:300px;background:#fff;border-radius:8px;box-shadow:0 8px 28px rgba(0,0,0,.22);padding:4px 18px 12px">'
            + head('Trade') +
            f'<span style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><span style="height:38px;border-radius:5px;background:{MID};color:#fff;display:grid;place-items:center;font-size:15px;font-weight:700">Buy</span>'
            f'<span style="height:38px;border-radius:5px;background:{MID};color:#fff;display:grid;place-items:center;font-size:15px;font-weight:700">Sell</span></span>'
            + head('Auto Invest') + item(CAL, 'Set up Auto Invest') + item(GEAR, 'Manage Auto Investments')
            + head('Watchlist') + item(PLUS_C, 'Add to Watchlist') + '</div>')
    return frame(tbl + menu, PAGE)


# 4 ------------------------------------------------------------------ tour, steps 1 and 2
def tooltip(title, body, step, x, y, w, arrow_y, back=False, tid=None):
    dots = ''.join(f'<i style="display:block;width:{18 if k == step else 6}px;height:6px;border-radius:3px;background:{INK if k == step else "#C4C4C4"}"></i>' for k in range(4))
    return (f'<div{f" id={chr(34)}{tid}{chr(34)}" if tid else ""} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:#F0F0F0;border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:16px 18px 14px">'
            f'<span style="position:absolute;left:-7px;top:{arrow_y}px;width:14px;height:14px;background:#F0F0F0;transform:rotate(45deg)"></span>'
            f'<span style="position:absolute;right:16px;top:14px;font-size:12px;font-weight:700;text-decoration:underline">Exit</span>'
            f'<b style="display:block;font-size:17px;font-weight:700;padding-right:40px">{title}</b>'
            f'<span style="display:block;font-size:13px;line-height:1.5;color:{INK2};padding-top:8px">{body}</span>'
            f'<span style="display:flex;align-items:center;justify-content:space-between;padding-top:14px">'
            f'<span style="display:flex;align-items:center;gap:5px">{dots}</span>'
            f'<span style="display:flex;align-items:center;gap:14px">{"<span style=\"font-size:12.5px;font-weight:700;text-decoration:underline\">Back</span>" if back else ""}'
            f'<span style="height:28px;padding:0 20px;border-radius:14px;background:{DARK};color:#fff;display:grid;place-items:center;font-size:12.5px;font-weight:700">Next</span></span></span></div>')


def histogram(w=208, h=70):
    import math
    n = 64
    bars = []
    for i in range(n):
        t = i / (n - 1)
        v = 0.12 + 0.88 * math.exp(-t * 9) + (0.05 * math.sin(i * 1.7))
        if i < 2:
            v = 0.55 + 0.25 * i
        if i == n - 1:
            v = 0.42
        bars.append(max(0.08, min(1, v)))
    bw = w / n
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" style="display:block">'
            + ''.join(f'<rect x="{i * bw:.2f}" y="{h - v * h:.1f}" width="{bw * .72:.2f}" height="{v * h:.1f}" fill="{INK3}"/>' for i, v in enumerate(bars)) + '</svg>')


def range_block(rid=None):
    return (f'<div{f" id={chr(34)}{rid}{chr(34)}" if rid else ""} style="padding:10px 0 4px;background:#fff">'
            f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:8px">Expense Ratio</span>'
            f'<span style="display:flex;align-items:center;justify-content:center;gap:12px">'
            f'<span style="width:72px;height:30px;border:1px solid {RULE};border-radius:5px;display:grid;place-items:center;font-size:12px;font-weight:600">0.00%</span>{icon(ARROW, 18, INK2, 1.5)}'
            f'<span style="width:72px;height:30px;border:1px solid {RULE};border-radius:5px;display:grid;place-items:center;font-size:12px;font-weight:600">2.00%</span></span>'
            f'<span style="display:block;text-align:center;font-size:11.5px;font-weight:700;padding:8px 0 6px">Matching Funds: 1,786</span>'
            f'<span style="display:block;position:relative;width:208px;margin:0 auto;padding-bottom:12px">{histogram()}'
            f'<span style="position:absolute;left:0;right:0;bottom:6px;height:3px;background:{INK}"></span>'
            f'<span style="position:absolute;left:-7px;bottom:0;width:15px;height:15px;border-radius:50%;background:{INK}"></span>'
            f'<span style="position:absolute;right:-7px;bottom:0;width:15px;height:15px;border-radius:50%;background:{INK}"></span></span></div>')


def tour():
    sec_head = lambda t: f'<span style="display:block;font-size:14px;font-weight:700;padding:12px 0 6px">{t}</span>'
    panel1 = (
        f'<div style="position:absolute;left:24px;top:44px;width:230px;height:420px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.1);padding:14px 16px;overflow:hidden">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:1px solid {RULE}"><span style="font-size:20px">Screener</span>{icon(INFO, 18, INK2, 1.6)}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:12px 0 4px"><span style="font-size:13.5px;font-weight:700">Fund Categories</span><span style="font-size:11px;font-weight:700;color:{INK3};text-decoration:underline">Clear Filters</span></div>'
        f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:2px">Asset Class</span>'
        + ''.join(checkbox(t, True, 14, 12.5, 25) for t in ['Alternatives', 'Bonds', 'Commodity', 'Equity', 'Mixed Assets', 'Money Market']) +
        f'<div style="border-top:1px solid {RULE};margin-top:8px">' + sec_head('Additional Filters') +
        f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:6px">Asset Style</span>'
        f'<span style="height:32px;border:1px solid {RULE};border-radius:5px;display:flex;align-items:center;justify-content:space-between;padding:0 10px;font-size:12.5px;font-weight:700">Search{icon(SEARCH, 15, INK2, 1.6)}</span>'
        f'<span style="display:block;text-align:right;font-size:11px;font-weight:700;text-decoration:underline;padding:8px 0 4px">Select All</span>'
        + checkbox('Core Bond Funds', False, 14, 12.5, 25) + checkbox('Large-Cap Value Funds', False, 14, 12.5, 25) + '</div></div>'
    )
    panel2 = (
        f'<div style="position:absolute;left:500px;top:44px;width:230px;height:420px;background:#fff;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.1);padding:4px 16px 14px;overflow:hidden">'
        + range_block('range') +
        f'<div style="border-top:1px solid {RULE};margin-top:10px;padding-top:12px">'
        f'<span style="display:block;font-size:11px;font-weight:600;color:{INK2};padding-bottom:2px">Fund Type</span>'
        + checkbox('ETFs', True, 14, 12.5, 26) + checkbox('Mutual Funds', True, 14, 12.5, 26) + '</div>'
        f'<div style="border-top:1px solid {RULE};margin-top:10px;padding-top:14px">'
        f'<span style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700">{icon(PLUS_C, 18, INK2, 1.5)}Add Filters</span></div></div>'
    )
    labels = (f'<span style="position:absolute;left:24px;top:14px;font-size:11px;font-weight:700;letter-spacing:.12em;color:{INK2}">TOUR · STEP 1 OF 4</span>'
              f'<span style="position:absolute;left:500px;top:14px;font-size:11px;font-weight:700;letter-spacing:.12em;color:{INK2}">TOUR · STEP 2 OF 4</span>')
    t1 = tooltip('Select Filters', 'Use the checkboxes to add or remove your selections.', 0, 266, 112, 226, 34, tid='tip')
    t2 = tooltip('Add Filters', 'Narrow down your results even further by selecting from a variety of fund categories and additional criteria.', 1, 744, 282, 206, 58, back=True)
    return frame(labels + panel1 + panel2 + t1 + t2)


# 5 ------------------------------------------------------------------ welcome, step 1, step 2
def questions():
    card = lambda x, y, w, h, inner, pad='18px 18px': (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:8px;'
                                                        f'box-shadow:0 2px 10px rgba(0,0,0,.1);padding:{pad};display:flex;flex-direction:column">{inner}</div>')
    welcome = card(16, 116, 262, 268,
                   f'<span style="align-self:flex-end">{icon(CLOSE, 18, INK, 1.8)}</span>'
                   f'<span style="font-size:22px;line-height:1.2;font-weight:600;padding-top:4px">Welcome to Screener</span>'
                   f'<span style="font-size:12.5px;line-height:1.5;color:{INK2};padding-top:10px">We’ve got a couple of preliminary questions about your fund filtering preferences. Your answers will help narrow down your results.</span>'
                   f'<span style="font-size:12.5px;line-height:1.5;color:{INK2};padding-top:8px">You’ll also have the option to add more filters afterwards.</span>'
                   f'<span style="margin-top:auto;align-self:flex-start;height:34px;padding:0 20px;border-radius:5px;background:{DARK};color:#fff;display:grid;place-items:center;font-size:13px;font-weight:700">Let’s Begin</span>')
    cats = [('Asset Class', 'Funds that invest in groups of securities with similar financial characteristics.'),
            ('Equity Style', 'US, international and global funds classified by growth, value and core.'),
            ('Market Cap', 'Funds that tend to invest in companies with similar market values.'),
            ('Target Asset Mix', 'A set mix of stocks, bonds and short-term investments that varies by risk.')]
    opts = ''.join(f'<span style="border:1px solid {RULE};border-radius:6px;padding:8px 12px;display:flex;flex-direction:column;gap:2px{";outline:2px solid " + INK + ";outline-offset:-1px" if t == "Equity Style" else ""}">'
                   f'<b style="font-size:13px;font-weight:700">{t}</b><span style="font-size:10.5px;line-height:1.4;color:{INK2}">{d}</span></span>' for t, d in cats)
    step1 = card(318, 36, 322, 428,
                 f'<span style="text-align:right;font-size:11px;color:{INK2};padding-bottom:8px;border-bottom:1px solid {RULE}">Step 1 of 2</span>'
                 f'<span style="font-size:14.5px;line-height:1.4;font-weight:600;text-align:center;padding:12px 0">Which fund category would you like to start filtering by?</span>'
                 f'<span style="display:flex;flex-direction:column;gap:8px">{opts}</span>'
                 f'<span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:12.5px;font-weight:700;padding-top:12px">Set my own filters instead{icon(CHEV_R, 14, INK, 2)}</span>'
                 f'<span style="margin:auto -18px -18px;padding:10px;background:#EFEFEF;border-radius:0 0 8px 8px;display:flex;align-items:center;justify-content:center;gap:6px;font-size:11.5px">{icon(BULB, 15, INK2, 1.6)}Not sure which filter to choose? <b>Go to our Glossary.</b></span>')
    eq = ['Global / International Core', 'Global / International Growth', 'Global / International Value', 'US Core', 'US Growth', 'US Value']
    step2 = card(680, 76, 264, 348,
                 f'<span style="display:flex;justify-content:space-between;font-size:12px;padding-bottom:8px;border-bottom:1px solid {RULE}"><b style="font-weight:700">Equity Style</b><span style="font-size:11px;color:{INK2}">Step 2 of 2</span></span>'
                 f'<span style="font-size:12.5px;line-height:1.45;text-align:center;padding:10px 0">Great! Narrow down your results by selecting an option below.</span>'
                 f'<span style="display:flex;flex-direction:column;gap:7px">' + ''.join(f'<span style="height:32px;border:1px solid {RULE};border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,.06);display:grid;place-items:center;font-size:12px;font-weight:700">{o}</span>' for o in eq) + '</span>')
    arrow = lambda x, y: f'<span style="position:absolute;left:{x}px;top:{y}px;width:28px;height:28px;border-radius:50%;background:{ACC};display:grid;place-items:center">{icon(ARROW, 16, "#fff", 2.4)}</span>'
    return frame(welcome + step1 + step2 + arrow(284, 236) + arrow(646, 236))


def board(bid, title, html):
    return {'id': bid, 'title': title, 'w': W, 'h': H, 'lang': 'en', 'dir': None,
            'css': ':host{margin:0}\n*{box-sizing:border-box}\n', 'html': html,
            'fonts': ['https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,300..800;1,400..600&display=swap']}


BOARDS = [
    ('GreyAddFilters', 'Add Filters, greyscale', add_filters),
    ('GreyPills', 'Active filter pills, greyscale', pills),
    ('GreyRowMenu', 'Row actions menu, greyscale', row_menu),
    ('GreyTour', 'Tour steps 1 and 2, greyscale', tour),
    ('GreyQuestions', 'Pre-screen questions, greyscale', questions),
]

if __name__ == '__main__':
    out = os.path.join(ROOT, 'src', 'cases', 'self-invest.boards.json')
    boards = [b for b in json.load(open(out, encoding='utf-8')) if not b['id'].startswith('Grey')]
    boards += [board(i, t, f()) for i, t, f in BOARDS]
    json.dump(boards, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('wrote', out, [b['id'] for b in boards])
