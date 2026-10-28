"""Builds the FlexIt onboarding screens as HTML boards (390 x 844), from the original 2020 designs.

Writes src/cases/flexit.boards.json:
  FxWelcome, FxDiscover, FxCheckIn, FxWorkOut, FxCheckOut   the five-screen welcome carousel
  FxModalPhone, FxModalGender, FxModalBirth                 "Why am I being asked for this?" on Create Account
  FxTipMap, FxTipFilter, FxTipCheckIn                       onboarding tooltips 1/5, 2/5 and 4/5 over the map
Copy is transcribed from the original screens. Photos are cropped from the original designs (img/fx-photo-*.jpg);
the map of Manhattan is redrawn as a vector.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 390, 844
FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONTS = ['https://fonts.googleapis.com/css2?family=Inter:wght@400..800&display=swap']
NAVY, PIN = '#1E2A44', '#3B8BB5'


def status(time='9:41', light=True):
    c = '#FFFFFF' if light else '#2B3445'
    return (f'<div style="position:absolute;left:0;right:0;top:0;height:50px;z-index:8;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0 34px;color:{c};font-size:15px;font-weight:600">'
            f'<span>{time}</span><span style="position:absolute;left:50%;top:11px;width:120px;height:34px;margin-left:-60px;border-radius:20px;background:#000"></span>'
            f'<span style="display:flex;align-items:center;gap:6px"><svg width="18" height="11" viewBox="0 0 18 11" aria-hidden="true"><g fill="{c}"><rect x="0" y="7" width="3" height="4" rx=".8"/><rect x="5" y="5" width="3" height="6" rx=".8"/><rect x="10" y="2.5" width="3" height="8.5" rx=".8"/><rect x="15" y="0" width="3" height="11" rx=".8"/></g></svg>'
            f'<svg width="16" height="11" viewBox="0 0 16 11" aria-hidden="true"><path d="M8 10.5l2.2-2.6a3.2 3.2 0 0 0-4.4 0zM3.4 5.4a6.8 6.8 0 0 1 9.2 0l1.4-1.6a8.9 8.9 0 0 0-12 0z" fill="{c}"/></svg>'
            f'<svg width="25" height="12" viewBox="0 0 25 12" aria-hidden="true"><rect x=".5" y=".5" width="21" height="11" rx="3" fill="none" stroke="{c}" opacity=".5"/><rect x="2" y="2" width="17" height="8" rx="1.8" fill="{c}"/><rect x="22.5" y="4" width="1.8" height="4" rx=".9" fill="{c}" opacity=".5"/></svg></span></div>')


LOGO_MARK = ('<svg width="40" height="38" viewBox="0 0 40 38" aria-hidden="true" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="square">'
             '<path d="M2 9V2h7M31 2h7v7M2 29v7h7M38 29v7h-7"/>'
             '<path d="M10 12h20M10 19h14M10 26h7" stroke-width="3.6" stroke-linecap="round"/></svg>')


def logo(top=74):
    return (f'<div style="position:absolute;left:0;right:0;top:{top}px;display:flex;align-items:center;justify-content:center;gap:12px">'
            f'{LOGO_MARK}<span style="font-size:40px;line-height:1;font-weight:500;letter-spacing:.22em;margin-right:-.22em;color:#FFFFFF">FLEXIT</span></div>')


def dots(active):
    return ''.join(f'<i style="width:9px;height:9px;border-radius:50%;box-sizing:border-box;{"background:#FFFFFF" if i == active else "border:1.5px solid rgba(255,255,255,.8)"}"></i>' for i in range(5))


# ---------- the map of Manhattan ----------
# Drawn in a local frame where the street grid is upright (x east, y south; 1 unit ~ 1/76 mile),
# then turned 29 degrees, the angle of the Manhattan grid. Central Park sits at x -22..8, y -75..75.
ROT = math.radians(29)
CS, SN = math.cos(ROT), math.sin(ROT)
LAND, MLAND, WATER, PARK, ROAD, HWY, HWY_EDGE = '#E9E8E4', '#F1F0EC', '#AED3E6', '#C9E6C3', '#FFFFFF', '#F8DA7A', '#E2BD55'
YS = list(range(-270, 481, 5))  # the stretch of shoreline that is ever on screen


def street(n):
    """local y of a numbered street"""
    return 75 - (n - 59) * 2.94


def xw(y):  # Hudson shore of Manhattan
    return -70 + 3 * math.sin(y / 23) + 1.4 * math.sin(y / 12) + (-(y - 300) * 0.05 if y > 300 else 0)


def xe(y):  # East River / Harlem River shore of Manhattan
    v = 62 + 2.6 * math.sin(y / 19) + 1.2 * math.sin(y / 11)
    if y < -95:
        v -= (-95 - y) * 0.42
    if y > 300:
        v -= (y - 300) * 0.10
    return v


def xnj(y):  # New Jersey shore
    return xw(y) - 62 + 5 * math.sin(y / 31)


def xq(y):  # Queens and Bronx shore
    if y > -60:
        return xe(y) + 42 + 4 * math.sin(y / 17)
    if y > -185:
        return xe(y) + 42 + (-60 - y) * 0.9
    return xe(y) + 20


def path(pts, close=True):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + (' Z' if close else '')


def lines(pts):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def to_screen(p, o, s):
    x, y = p
    return (o[0] + s * (x * CS - y * SN), o[1] + s * (x * SN + y * CS))


def pin(x, y, r, price=False, op=1):
    hy = r * 1.75
    d = f'M0 0C{-r * .25:.1f} {-r * .7:.1f} {-r} {-r * 1.15:.1f} {-r} {-hy:.1f}A{r} {r} 0 1 1 {r} {-hy:.1f}C{r} {-r * 1.15:.1f} {r * .25:.1f} {-r * .7:.1f} 0 0Z'
    inner = (f'<text x="0" y="{-hy + 4:.1f}" fill="#FFFFFF" font-size="11.5" font-weight="700" text-anchor="middle">$0.12</text>' if price
             else f'<circle cx="0" cy="{-hy:.1f}" r="{r * .32:.1f}" fill="#FFFFFF"/>')
    return (f'<g transform="translate({x:.1f} {y:.1f})" opacity="{op}"><ellipse cx="0" cy="1" rx="{r * .45:.1f}" ry="{r * .16:.1f}" fill="#0B1F33" opacity=".22"/>'
            f'<path d="{d}" fill="{PIN}" stroke="#2F7BA3" stroke-width=".8"/>{inner}</g>')


def map_svg(w, h, o, s, pins=(), pin_r=14, price=False, labels=True, city=None, uid='m'):
    island = [(xw(y), y) for y in YS] + [(xe(y), y) for y in reversed(YS)]
    hudson = [(xnj(y), y) for y in YS] + [(xw(y), y) for y in reversed(YS)]
    east = [(xe(y), y) for y in YS] + [(xq(y), y) for y in reversed(YS)]
    nj = [(-600, YS[0]), (-600, YS[-1])] + [(xnj(y), y) for y in reversed(YS)]
    qn = [(xq(y), y) for y in YS] + [(600, YS[-1]), (600, YS[0])]
    # Manhattan streets: every other street thin, the wide crosstown streets heavier, avenues in between
    minor = ''.join(f'<line x1="-120" y1="{street(n):.1f}" x2="120" y2="{street(n):.1f}"/>' for n in range(2, 190, 2))
    major = ''.join(f'<line x1="-120" y1="{street(n):.1f}" x2="120" y2="{street(n):.1f}"/>' for n in (14, 23, 34, 42, 57, 72, 79, 86, 96, 110, 116, 125, 135, 145, 155))
    aves = ''.join(f'<line x1="{x}" y1="-700" x2="{x}" y2="900"/>' for x in (-63, -55, -44, -33, -22, -12, -2, 8, 16, 24, 31, 38, 46, 53))
    bway = lines([(20, street(14)), (8, street(23)), (-2, street(34)), (-12, street(42)), (-22, street(59)), (-38, street(72)), (-47, street(96)), (-49, street(125)), (-46, street(180))])

    # the other boroughs: their own grids at their own angles
    def grid(step, ang, cx, cy=100, half=420):
        a = math.radians(ang)
        c, s_ = math.cos(a), math.sin(a)
        out = ''
        for k in range(-int(half / step), int(half / step) + 1):
            d = k * step
            out += f'<line x1="{cx + d * c - half * s_:.0f}" y1="{cy + d * s_ + half * c:.0f}" x2="{cx + d * c + half * s_:.0f}" y2="{cy + d * s_ - half * c:.0f}"/>'
            out += f'<line x1="{cx - half * c - d * s_:.0f}" y1="{cy - half * s_ + d * c:.0f}" x2="{cx + half * c - d * s_:.0f}" y2="{cy + half * s_ + d * c:.0f}"/>'
        return out
    whs = [(xw(y) + 3.5, y) for y in YS]
    fdr = [(xe(y) - 3.5, y) for y in YS]
    roads = [
        [(xe(street(60)) - 20, street(60)), (xq(street(60)) + 10, street(60) - 2), (xq(street(60)) + 140, street(60) - 14)],  # Queensboro Bridge
        [(xe(street(125)) - 3, street(125)), (100, -126), (190, -134), (300, -120), (460, -96)],                              # RFK Bridge
        [(100, -126), (102, -200), (98, -330)],
        [(xnj(street(40)) - 4, street(40)), (-200, street(40) + 22), (-320, street(40) + 16), (-470, street(40) + 40)],      # to the Lincoln Tunnel
        [(xnj(y) - 125 + 6 * math.sin(y / 60), y) for y in YS],                                                             # through New Jersey
        [(xq(y) + 55 + 10 * math.sin(y / 90), y) for y in YS if y > -60],                                                   # through Queens
    ]
    hwy = ''.join(f'<polyline points="{lines(r)}"/>' for r in [whs, fdr] + roads)
    park = (f'<rect x="-22" y="-75" width="30" height="150" fill="{PARK}"/>'
            f'<ellipse cx="-7" cy="-22" rx="11" ry="13" fill="{WATER}"/><ellipse cx="-10" cy="33" rx="6" ry="4" fill="{WATER}"/>'
            f'<path d="{path([(xw(y), y) for y in YS if -170 < y < 50] + [(xw(y) + 5, y) for y in reversed(YS) if -170 < y < 50])}" fill="{PARK}"/>')
    rand = f'<ellipse cx="96" cy="-128" rx="30" ry="40" fill="{LAND}"/><ellipse cx="98" cy="-120" rx="18" ry="24" fill="{PARK}"/>'
    roosevelt = f'<rect x="{xe(90) + 17:.1f}" y="10" width="7" height="165" rx="3.5" fill="{LAND}"/>'
    rot = f'translate({o[0]:.1f} {o[1]:.1f}) scale({s}) rotate(29)'
    g = (f'<g transform="{rot}">'
         f'<g clip-path="url(#{uid}nj)" stroke="{ROAD}" stroke-width="1" fill="none">{grid(9, -12, -330)}</g>'
         f'<g clip-path="url(#{uid}qn)" stroke="{ROAD}" stroke-width="1" fill="none">{grid(8, 16, 330)}</g>'
         f'<path d="{path(hudson)}" fill="{WATER}"/><path d="{path(east)}" fill="{WATER}"/>{rand}{roosevelt}'
         f'<use href="#{uid}is" fill="{MLAND}"/>'
         f'<g clip-path="url(#{uid}mn)" fill="none" stroke="{ROAD}"><g stroke-width=".9">{minor}</g><g stroke-width="1.5">{aves}</g>'
         f'<g stroke-width="2.4">{major}</g><polyline points="{bway}" stroke-width="1.8"/>{park}</g>'
         f'<g fill="none" stroke-linecap="round" stroke-linejoin="round"><use href="#{uid}hw" stroke="{HWY_EDGE}" stroke-width="{4.6 / s:.2f}"/><use href="#{uid}hw" stroke="{HWY}" stroke-width="{3 / s:.2f}"/></g>'
         f'</g>')
    defs = (f'<defs><clipPath id="{uid}nj"><path d="{path(nj)}"/></clipPath><clipPath id="{uid}qn"><path d="{path(qn)}"/></clipPath>'
            f'<path id="{uid}is" d="{path(island)}"/><g id="{uid}hw">{hwy}</g><clipPath id="{uid}mn"><use href="#{uid}is"/></clipPath></defs>')
    lab = ''
    if labels:
        def t(p, words, size=11, ang=0, col='#868B91', wt=600, sp='.14em'):
            x, y = to_screen(p, o, s)
            out = ''
            for k, wd in enumerate(words):
                dy = (k - (len(words) - 1) / 2) * size * 1.25
                out += (f'<text x="{x:.1f}" y="{y + dy + size * .35:.1f}" transform="rotate({ang} {x:.1f} {y:.1f})" fill="{col}" stroke="{MLAND}" stroke-width="3" paint-order="stroke" '
                        f'font-size="{size}" font-weight="{wt}" letter-spacing="{sp}" text-anchor="middle">{wd}</text>')
            return out
        lab += t((-16, -66), ['MANHATTAN'], 12.5)
        lab += t((36, 22), ['UPPER', 'EAST SIDE'], 10)
        lab += t((6, 142), ['MIDTOWN', 'MANHATTAN'], 10)
        lab += t((-5, -128), ['HARLEM'], 11)
        lab += t((-109, 96), ['NEW JERSEY'], 9.5, -61) + t((-93, 96), ['NEW YORK'], 9.5, -61)
        lab += t((xe(-60) - 3.5, -60), ['FDR'], 8.5, -61, '#A98B33', 700, '.06em')
        sx, sy = to_screen((xw(205) + 3.5, 205), o, s)
        lab += (f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="10" fill="#FFFFFF" stroke="#9AA0A6" stroke-width="1.1"/>'
                f'<text x="{sx:.1f}" y="{sy + 3.5:.1f}" fill="#6E737A" font-size="9.5" font-weight="600" text-anchor="middle">9A</text>')
        if city:
            lab += f'<text x="{city[0]}" y="{city[1]}" fill="#7C8188" stroke="{LAND}" stroke-width="3" paint-order="stroke" font-size="26" font-weight="500">New York</text>'
    pins_svg = ''.join(pin(*to_screen(p, o, s), pin_r, price) for p in pins)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true" style="display:block;font-family:{FONT}">{defs}'
            f'<rect width="{w}" height="{h}" fill="{LAND}"/>{g}{lab}{pins_svg}</svg>')


# ---------- 1 · welcome carousel ----------
WELCOME = [
    ('FxWelcome', 'Welcome: pay-by-the-minute gym access', 'Pay-By-The-Minute<br>Gym Access', False, 'img/fx-photo-welcome.jpg',
     'No more monthly or yearly membership.<br>Only pay for the time you use!'),
    ('FxDiscover', 'Welcome: discover', 'DISCOVER', True, None,
     'Find a gym near you.<br>Choose from thousands of<br>gyms nationwide.'),
    ('FxCheckIn', 'Welcome: check in', 'CHECK IN', True, 'img/fx-photo-checkin.jpg',
     'Scan the QR code at the front<br>desk and you’re ready to start<br>your workout.'),
    ('FxWorkOut', 'Welcome: work out', 'WORK OUT', True, 'img/fx-photo-workout.jpg',
     'Lift some weights, take a class,<br>it’s up to you.'),
    ('FxCheckOut', 'Welcome: check out', 'CHECK OUT', True, 'img/fx-photo-checkout.jpg',
     'Scan the same QR code on<br>your way out. Only pay for the<br>time you use.'),
]
CARD_PINS = [(36, -40), (-48, 40), (20, 92), (-62, 104), (30, 186), (-36, 196), (6, 252)]


def welcome(i, title, caps, photo, body):
    bg = 'radial-gradient(130% 62% at 50% 58%, #1D93BF 0%, #1A71A2 20%, #18487F 45%, #152F64 72%, #142A5C 100%)'
    head = (f'<div style="position:absolute;left:0;right:0;top:146px;text-align:center;font-size:{22 if caps else 25}px;line-height:1.25;'
            f'font-weight:{500 if caps else 400};letter-spacing:{".02em" if caps else "0"};color:#F2F7FB">{title}</div>')
    top = 212 if caps else 226
    art = (f'<img src="{photo}" alt="" style="display:block;width:100%;height:100%;object-fit:cover">' if photo else
           map_svg(300, 330, (196, 112), .82, pins=CARD_PINS, pin_r=13, uid='wc'))
    card = (f'<div style="position:absolute;left:45px;top:{top}px;width:300px;height:330px;border-radius:14px;overflow:hidden;'
            f'box-shadow:0 12px 30px rgba(4,12,34,.45);background:#E9EEF3">{art}</div>')
    txt = (f'<div style="position:absolute;left:24px;right:24px;top:{top + 352}px;text-align:center;font-size:19px;line-height:1.32;'
           f'font-weight:500;color:#EAF3FA">{body}</div>')
    foot = (f'<div style="position:absolute;left:0;right:0;top:690px;display:flex;justify-content:center;gap:9px">{dots(i)}</div>'
            f'<div style="position:absolute;left:20px;right:20px;top:718px;height:58px;border-radius:12px;background:#F6F8FA;display:flex;align-items:center;justify-content:center;'
            f'font-size:17px;font-weight:700;color:#1F2A44;box-shadow:0 4px 14px rgba(4,12,34,.2)">Create New Account</div>'
            f'<div style="position:absolute;left:0;right:0;top:796px;text-align:center;font-size:14px;font-weight:500;color:#E6EEF6">'
            f'Already have an account? <b style="font-weight:700;text-decoration:underline;text-underline-offset:2px">Sign In</b></div>')
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};font-family:{FONT};-webkit-font-smoothing:antialiased">'
            f'{status()}{logo()}{head}{card}{txt}{foot}</div>')


# ---------- 2 · Create Account with information modals ----------
X = '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#1E2A44" stroke-width="2.4" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"/></svg>'
Q = '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#9AA3AF" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M9.4 9.3a2.7 2.7 0 1 1 3.6 2.6c-.6.3-1 .8-1 1.5v.7"/><circle cx="12" cy="17.2" r=".4" fill="#9AA3AF"/></svg>'
FIELDS = [('Phone Number', 352), ('Gender', 414), ('Date of Birth', 476)]
MODALS = [
    ('FxModalPhone', 'Why we ask for a phone number', 396,
     ['Great question!', 'Most FlexIt partner gyms require the contact information of individuals who use their facilities.',
      'They might need to reach out to you regarding lost and found, or in response to a customer service inquiry.'], None),
    ('FxModalGender', 'Why we ask about gender', 458,
     ['We’re glad you asked.', 'Most FlexIt partner gyms assign locker rooms by binary gender.',
      'If you would like to tell us more about your gender identity, please click the link below. FlexIt is committed to making sure every member feels safe, welcome and respected.'],
     '+ Add gender information'),
    ('FxModalBirth', 'Why we ask for a date of birth', 516,
     ['We thought you’d never ask!', 'We require this information because you need to be at least 18 years old to exercise at FlexIt partner gyms.'], None),
]


def create_account(top, paras, link):
    rows = ''.join(f'<div style="position:absolute;left:20px;right:20px;top:{y - 24}px;height:48px;display:flex;align-items:center;justify-content:space-between;'
                   f'border-bottom:1px solid #D5DAE1"><span style="font-size:16px;color:#9AA3AF">{label}</span>{Q}</div>' for label, y in FIELDS)
    base = (f'<div style="position:absolute;left:0;right:0;top:80px;text-align:center;font-size:28px;font-weight:600;letter-spacing:-.01em;color:#4A5568">Create Account</div>'
            f'<div style="position:absolute;left:125px;top:134px;width:140px;height:2px;background:#D5DAE1"></div>'
            f'<div style="position:absolute;left:125px;top:134px;width:94px;height:2px;background:#6B7686"></div>'
            f'<i style="position:absolute;left:153px;top:131px;width:8px;height:8px;border-radius:50%;background:#6B7686"></i>'
            f'<i style="position:absolute;left:215px;top:131px;width:8px;height:8px;border-radius:50%;background:#6B7686"></i>'
            f'<div style="position:absolute;left:28px;top:172px;font-size:18px;line-height:1.35;font-weight:700;color:#4A5568">You’re one step closer<br>to your fitness goals!</div>'
            f'<div style="position:absolute;left:28px;top:236px;font-size:15px;line-height:1.45;color:#8A94A3">Complete your profile now and<br>save time at your first gym check-in.</div>'
            f'{rows}'
            f'<div style="position:absolute;left:20px;right:20px;top:580px;height:58px;border-radius:12px;background:#4E95B5;display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:700;color:#FFFFFF">Continue</div>')
    veil = '<div style="position:absolute;inset:0;background:rgba(150,156,163,.55);z-index:4"></div>'
    body = ''.join(f'<p style="margin:0">{p}</p>' for p in paras)
    lk = f'<p style="margin:0;text-align:right;font-weight:600;text-decoration:underline;text-underline-offset:3px;color:#1E2A44">{link}</p>' if link else ''
    card = (f'<div style="position:absolute;left:34px;width:310px;top:{top}px;z-index:5;box-sizing:border-box;padding:20px 22px 26px;background:#F6F7F9;border-radius:2px;'
            f'box-shadow:0 10px 30px rgba(20,28,44,.25)">'
            f'<span style="position:absolute;right:0;top:-25px;width:0;height:0;border-left:26px solid transparent;border-bottom:26px solid #F6F7F9"></span>'
            f'<span style="position:absolute;right:14px;top:12px">{X}</span>'
            f'<p style="margin:26px 0 14px;font-size:15.5px;font-weight:700;color:#1E2A44">Why am I being asked for this?</p>'
            f'<div style="display:flex;flex-direction:column;gap:14px;font-size:15px;line-height:1.38;color:#2E3646">{body}{lk}</div></div>')
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:#F3F5F8;font-family:{FONT};-webkit-font-smoothing:antialiased">'
            f'{status(light=False)}{base}{veil}{card}</div>')


# ---------- 3 · onboarding tooltips over the map ----------
def ico(p, size=24, col='#8A929C', sw=1.8, fill='none'):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'


SEARCH = '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5l5 5"/>'
SLIDERS = '<path d="M3 6h18M3 12h18M3 18h18"/><circle cx="15" cy="6" r="2" fill="#FFFFFF"/><circle cx="8" cy="12" r="2" fill="#FFFFFF"/><circle cx="17" cy="18" r="2" fill="#FFFFFF"/>'
LIST = '<path d="M5 6h14M5 10h14M5 14h14M5 18h14"/>'
QR = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true" fill="none" stroke="{c}" stroke-width="1.8">'
      '<path d="M2 9V2h7M25 2h7v7M2 25v7h7M32 25v7h-7" stroke-linecap="round"/>'
      '<g fill="{c}" stroke="none"><rect x="8" y="8" width="7" height="7" rx="1"/><rect x="19" y="8" width="7" height="7" rx="1"/><rect x="8" y="19" width="7" height="7" rx="1"/>'
      '<rect x="19" y="19" width="3" height="3"/><rect x="23" y="23" width="3" height="3"/><rect x="19" y="23" width="2" height="3"/><rect x="23" y="19" width="3" height="2"/></g></svg>')
# where the map sits on the tooltip screens, and its gyms
MAP_O, MAP_S = (258, 262), 1.3
MAP_PINS = [(25, -28), (-50, 92), (22, 176), (-36, 236), (18, 290)]


def search_bar(bright):
    bg = '#FFFFFF' if bright else '#F7F8FA'
    sh = 'box-shadow:0 4px 14px rgba(20,28,44,.18);' if bright else ''
    col = '#4A5260' if bright else '#9AA1AA'
    return (f'<div style="position:absolute;left:66px;width:258px;top:62px;height:46px;border-radius:23px;background:{bg};border:1px solid #D9DDE2;{sh}box-sizing:border-box;'
            f'display:flex;align-items:center;gap:10px;padding:0 14px">{ico(SEARCH, 22, col, 2)}<span style="flex:1;font-size:16px;color:{col}">Search...</span>'
            f'{ico(SLIDERS, 24, "#2F7FB0", 1.8)}</div>')


def qr_button(bright):
    c = '#2F7FB0' if bright else '#6E7680'
    return (f'<div style="position:absolute;left:160px;top:707px;width:70px;height:70px;border-radius:50%;background:#FFFFFF;'
            f'box-shadow:0 4px 14px rgba(20,28,44,{.25 if bright else .12});display:grid;place-items:center">{QR.format(c=c)}</div>')


def tab_bar(map_on=True):
    def item(p, t, on=False):
        c = '#2F7FB0' if on else '#7A828C'
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px;width:62px;font-size:10.5px;font-weight:500;color:{"#2F7FB0" if on else "#8A929C"}">'
                f'{ico(p, 26, c, 0, c)}<span>{t}</span></div>')
    PIN_I = '<path d="M12 22s-7-7.2-7-12.5a7 7 0 0 1 14 0C19 14.8 12 22 12 22z"/><circle cx="12" cy="9.5" r="2.6" fill="#FFFFFF"/>'
    USER = '<circle cx="12" cy="7.5" r="4.5"/><path d="M3.5 21c.6-4.6 4.2-7.5 8.5-7.5s7.9 2.9 8.5 7.5z"/>'
    WALLET = '<rect x="3" y="6" width="17" height="14" rx="2.5"/><rect x="14" y="10.5" width="8" height="5" rx="1.5" fill="#FFFFFF"/><path d="M5 6l9-3 2 3z"/>'
    STATS = '<rect x="4" y="13" width="3" height="8"/><rect x="10.5" y="9" width="3" height="12"/><rect x="17" y="5" width="3" height="16"/><path d="M3 10l6-5 4 3 8-6" fill="none" stroke="#7A828C" stroke-width="1.8"/>'
    return (f'<div style="position:absolute;left:0;right:0;top:756px;height:88px;background:#F8F9FB;border-top:1px solid #E1E4E8;display:flex;justify-content:space-around;align-items:flex-start;padding-top:12px;box-sizing:border-box">'
            f'{item(PIN_I, "Map", map_on)}{item(USER, "Profile")}<div style="width:62px;padding-top:34px;text-align:center;font-size:10.5px;font-weight:600;color:#6E7680;letter-spacing:.02em">CHECK-IN</div>'
            f'{item(WALLET, "Wallet")}{item(STATS, "Stats")}</div>')


def tri(x, w, h, up):
    """the speech-bubble tail: a right triangle whose upright side lines up with the thing it points at"""
    d = f'M0 {h}L{w} 0L{w} {h}Z' if up else f'M0 0L{w} 0L{w} {h}Z'
    pos = f'top:{-h + 1}px' if up else f'bottom:{-h + 1}px'
    return f'<svg style="position:absolute;left:{x - w}px;{pos}" width="{w}" height="{h}" aria-hidden="true"><path d="{d}" fill="#F6F7F9"/></svg>'


def map_screen(step, lines_, buttons, card_top, tail, bright):
    base = (f'<div style="position:absolute;left:0;top:0">{map_svg(W, 760, MAP_O, MAP_S, pins=MAP_PINS, pin_r=20, price=True, city=(22, 668), uid="tm")}</div>'
            f'<div style="position:absolute;left:12px;top:62px;width:46px;height:46px;border-radius:9px;background:#F7F8FA;border:1px solid #D9DDE2;box-sizing:border-box;display:grid;place-items:center;font-size:22px;font-weight:600;color:#7A828C">?</div>'
            f'{search_bar(False)}'
            f'<div style="position:absolute;right:12px;top:62px;width:46px;height:46px;border-radius:9px;background:#F7F8FA;border:1px solid #D9DDE2;box-sizing:border-box;display:grid;place-items:center">{ico(LIST, 24, "#7A828C", 2)}</div>'
            f'<div style="position:absolute;left:30px;right:30px;top:120px;height:28px;border-radius:7px;background:#DDE2E7;display:flex;padding:2px;box-sizing:border-box;font-size:12px;font-weight:600">'
            f'<span style="flex:1;border-radius:6px;background:#BCD6E6;color:#3A6E8F;display:grid;place-items:center">Prices</span><span style="flex:1;color:#8A929C;display:grid;place-items:center">Fitness Clubs</span></div>'
            f'{tab_bar(bright != "qr")}{qr_button(False)}')
    veil = '<div style="position:absolute;inset:0;background:rgba(198,201,206,.6);z-index:4"></div>'
    hi = ''
    if bright == 'pin':
        x, y = to_screen(MAP_PINS[0], MAP_O, MAP_S)
        hi = f'<svg style="position:absolute;left:0;top:0;z-index:5" width="{W}" height="760" aria-hidden="true" font-family="Inter, sans-serif">{pin(x, y, 20, True)}</svg>'
    elif bright == 'search':
        hi = f'<div style="position:relative;z-index:5">{search_bar(True)}</div>'
    elif bright == 'qr':
        hi = f'<div style="position:relative;z-index:5">{qr_button(True)}</div>'
    btns = ''
    if 'back' in buttons:
        btns += '<span style="padding:9px 18px;border:1.6px solid #1F2D4D;border-radius:4px;font-size:16px;font-weight:600;color:#1F2D4D;background:#FFFFFF">Back</span>'
    btns += '<span style="margin-left:auto;padding:10px 18px;border-radius:4px;background:#1F2D4D;font-size:16px;font-weight:600;color:#FFFFFF">Got it</span>'
    body = ''.join(f'<p style="margin:0;white-space:nowrap">{t}</p>' for t in lines_)
    card = (f'<div style="position:absolute;left:51px;width:290px;top:{card_top}px;z-index:6;box-sizing:border-box;padding:20px 26px 24px 22px;background:#F6F7F9;border-radius:2px;'
            f'box-shadow:0 12px 32px rgba(20,28,44,.22)">{tri(*tail)}'
            f'<div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:18px;color:#1E2A44">{step}</b>{X}</div>'
            f'<div style="margin:18px 0 24px 18px;display:flex;flex-direction:column;gap:20px;font-size:18px;line-height:1.38;color:#2B3445">{body}</div>'
            f'<div style="display:flex;align-items:center">{btns}</div></div>')
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{LAND};font-family:{FONT};-webkit-font-smoothing:antialiased">'
            f'{base}{status("7:54", light=False)}{veil}{hi}{card}</div>')


pin_tip = to_screen(MAP_PINS[0], MAP_O, MAP_S)
TIPS = [
    ('FxTipMap', 'Tooltip 1 of 5: the map', '1/5', ['Use the map to<br>explore gyms in your<br>area.', 'Gym pins show<br>by-the-minute rates.'], [], 318,
     (round(pin_tip[0]) - 51, 54, round(318 - pin_tip[1] - 4), True), 'pin'),
    ('FxTipFilter', 'Tooltip 2 of 5: filters', '2/5', ['Filter gyms by price,<br>proximity and<br>amenities.'], ['back'], 182, (239, 54, 64, True), 'search'),
    ('FxTipCheckIn', 'Tooltip 4 of 5: check in', '4/5', ['Check in by scanning<br>the QR code at the<br>front desk.', 'Only pay for the time<br>you use.'], ['back'], 330, (146, 28, 34, False), 'qr'),
]


def board(bid, title, html):
    return {'id': bid, 'title': title, 'w': W, 'h': H, 'lang': 'en', 'dir': None,
            'css': ':host{margin:0}\n*{box-sizing:border-box}\n', 'html': html, 'fonts': FONTS}


def build():
    out = []
    for i, (bid, t, head, caps, photo, body) in enumerate(WELCOME):
        out.append(board(bid, t, welcome(i, head, caps, photo, body)))
    for bid, t, top, paras, link in MODALS:
        out.append(board(bid, t, create_account(top, paras, link)))
    for bid, t, step, text, btns, top, tail, bright in TIPS:
        out.append(board(bid, t, map_screen(step, text, btns, top, tail, bright)))
    path_ = os.path.join(ROOT, 'src', 'cases', 'flexit.boards.json')
    json.dump(out, open(path_, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path_, len(out), 'boards')


if __name__ == '__main__':
    build()
