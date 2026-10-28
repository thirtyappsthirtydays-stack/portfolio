"""Builds the Liv's Love Pool screens as HTML boards, from the original 2020 designs.

Writes src/cases/livs-love-pool.boards.json:
  LvSite                                           the desktop home page (1280 x 800)
  LvHome, LvHow                                    mobile home and How it Works (390 x 844)
  LvAcct20, LvAcct40, LvAcct60, LvAcct80,
  LvConduct, LvIn                                  the guided sign-up, 20% to 100%
  LvProfile, LvMatches, LvMatch                    My Account
  LvFeedback, LvThanks                             date feedback
Copy is transcribed from the original screens. The photo (img/lv-photo.jpg), the two drawn avatars
(img/lv-av-*.png) and the logo (img/lv-logo.png) are cut from the original designs; everything else is redrawn.
"""
import json, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 390, 844
HEAD = "'Abril Fatface', Georgia, serif"
BODY = "Quicksand, 'Avenir Next', Arial, sans-serif"
FONTS = ['https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Quicksand:wght@400..700&display=swap']
INK, INK2, MUTE = '#1E1E1E', '#3D3A3C', '#A09DA2'
PINK, PINK_D, PINK_I, PINK_L = '#EF93AE', '#DC4C7A', '#E8789C', '#F9D6E1'
YEL, GREEN, CHK = '#F8D84A', '#3E8E41', '#C2335F'
BLUE, LAV, CREAM, TAB = '#CFE7EE', '#DAD4EF', '#F8EDCA', '#F29CB5'


def A(x, y, html, style=''):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;{style}">{html}</div>'


def ico(p, size=24, col=INK, sw=1.6, fill='none'):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="display:block">{p}</svg>')


CLIP = '<rect x="4.5" y="4" width="12.5" height="17" rx="1.5"/><path d="M8.5 4V2.8h4.5V4"/><path d="M7.5 9h6.5M7.5 12.5h4.5M7.5 16h3"/><path d="M14.5 15.5l5-5.6 1.7 1.5-5 5.6-2.3.7z"/>'
CLOCK = '<circle cx="12" cy="12" r="9"/><path d="M12 6.8v5.6l3.6 2.1"/>'
HEARTS = '<path d="M8.5 19.5S2 15.2 2 10.4A3.6 3.6 0 0 1 8.5 8.2 3.6 3.6 0 0 1 15 10.4c0 4.8-6.5 9.1-6.5 9.1z"/><path d="M15.5 19.5S9 15.2 9 10.4a3.6 3.6 0 0 1 6.5-2.2 3.6 3.6 0 0 1 6.5 2.2c0 4.8-6.5 9.1-6.5 9.1z"/>'
PHONE = '<path d="M5.2 4.5h3.3l1.5 3.8-2.1 1.3a9.6 9.6 0 0 0 4.5 4.5l1.3-2.1 3.8 1.5V17a1.9 1.9 0 0 1-1.9 1.9A14 14 0 0 1 3.3 6.4a1.9 1.9 0 0 1 1.9-1.9z"/><path d="M14.5 3.5a6 6 0 0 1 6 6M14.5 6.8a2.7 2.7 0 0 1 2.7 2.7"/>'
THUMB = '<path d="M3 3.5h18v12.5H10.5L6 20.5V16H3z"/><path d="M9 13.8V9.6l2.4-3.4c.8 0 1.3.6 1.1 1.4l-.4 1.7h3.6a1 1 0 0 1 1 1.2l-.7 2.6a1 1 0 0 1-1 .7z"/><path d="M7 9.6h2v4.2H7z"/>'
HOME = '<path d="M3 11.2L12 4l9 7.2"/><path d="M5.5 9.6V20h13V9.6"/><path d="M10 20v-5h4v5"/>'
CASE = '<rect x="3" y="7.5" width="18" height="12" rx="1.5"/><path d="M9 7.5V5h6v2.5M3 12.5h18M11 12v2h2v-2"/>'
CAP = '<path d="M2 9.5 12 5l10 4.5-10 4.5z"/><path d="M6.5 11.5V16c3 2 8 2 11 0v-4.5M20.5 10v5"/>'
PENCIL = '<path d="M5 16.5 15.5 6l2.8 2.8L7.8 19.3H5z"/><path d="M13.5 8l2.8 2.8"/><path d="M4 22.5h1.6M8 22.5h1.6M12 22.5h1.6M16 22.5h1.6"/>'
MIC = '<rect x="8.5" y="2.5" width="7" height="12" rx="3.5"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3.5M8.5 21.5h7"/>'
CHEV = '<path d="M9 5l7 7-7 7"/>'
BACK = '<path d="M15.5 3.5 7 12l8.5 8.5"/>'
CART = '<circle cx="9" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/><path d="M2 3.5h3l2.3 11h11.2L21 7H6.3"/>'
PERSON = '<circle cx="12" cy="7.6" r="4.6"/><path d="M3.2 21.6c.5-5.2 4.3-8.2 8.8-8.2s8.3 3 8.8 8.2z"/>'
HEART = '<path d="M12 21.2S2.4 15.2 2.4 8.9A5 5 0 0 1 12 6.1a5 5 0 0 1 9.6 2.8c0 6.3-9.6 12.3-9.6 12.3z"/>'


def gear(cx, cy, ro, ri, n, hole):
    pts = []
    for k in range(n * 2):
        r = ro if k % 2 == 0 else ri
        for d in (-0.32, 0.32):
            a = (k + .5 + d) * math.pi / n
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p = 'M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'
    return p + f'M{cx + hole:.2f} {cy:.2f}a{hole} {hole} 0 1 0 {-2 * hole:.2f} 0a{hole} {hole} 0 1 0 {2 * hole:.2f} 0z'


GEARS = f'<path fill-rule="evenodd" d="{gear(9.5, 13.5, 7.6, 5.6, 8, 2.6)}"/><path fill-rule="evenodd" d="{gear(17.8, 6.4, 4.6, 3.3, 7, 1.5)}"/>'


# ---------- painted shapes ----------
def smooth(pts):
    """a closed Catmull-Rom curve through the points"""
    n = len(pts)
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + 'Z'


def blob(cx, cy, rx, ry, col, seed=1, n=9, jit=.16, rot=0, op=1):
    r = random.Random(seed)
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n + r.uniform(-.15, .15)
        f = 1 + r.uniform(-jit, jit)
        x, y = rx * f * math.cos(a), ry * f * math.sin(a)
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return f'<path d="{smooth(pts)}" fill="{col}" opacity="{op}"/>'


def swash(pts, w, col, op=.8, seed=3):
    """a dry-brush stroke: one broad pass and a thinner, offset second pass for a ragged edge"""
    r = random.Random(seed)
    line = ' '.join(f'{x},{y}' for x, y in pts)
    off = ' '.join(f'{x + r.uniform(-3, 3):.1f},{y + w * .22 + r.uniform(-2, 2):.1f}' for x, y in pts)
    return (f'<g fill="none" stroke="{col}" stroke-linecap="round" stroke-linejoin="round">'
            f'<polyline points="{line}" stroke-width="{w}" opacity="{op}"/>'
            f'<polyline points="{off}" stroke-width="{w * .62:.1f}" opacity="{op * .7:.2f}"/></g>')


def paint(*shapes, w=W, h=H):
    return f'<svg style="position:absolute;left:0;top:0" width="{w}" height="{h}" aria-hidden="true">{"".join(shapes)}</svg>'


def icon_blob(x, y, p, seed, size=34, col=PINK_L):
    """a line icon on a pink paint dab"""
    return A(x, y, f'<svg width="{size + 12}" height="{size + 8}" style="position:absolute;left:-4px;top:-2px" aria-hidden="true">{blob(size / 2 + 8, size / 2 + 4, size * .46, size * .42, col, seed)}</svg>'
                   f'<div style="position:relative">{ico(p, size, INK, 1.3)}</div>', f'width:{size}px;height:{size}px')


# ---------- the phone frame ----------
def status():
    c = '#111111'
    return (f'<div style="position:absolute;left:0;right:0;top:0;height:50px;z-index:8;display:flex;align-items:center;justify-content:space-between;padding:6px 26px 0 34px;color:{c};font:600 15px/1 -apple-system,\'SF Pro Text\',Inter,sans-serif">'
            f'<span>9:41</span><span style="position:absolute;left:50%;top:11px;width:120px;height:34px;margin-left:-60px;border-radius:20px;background:#000"></span>'
            f'<span style="display:flex;align-items:center;gap:6px"><svg width="18" height="11" viewBox="0 0 18 11" aria-hidden="true"><g fill="{c}"><rect x="0" y="7" width="3" height="4" rx=".8"/><rect x="5" y="5" width="3" height="6" rx=".8"/><rect x="10" y="2.5" width="3" height="8.5" rx=".8"/><rect x="15" y="0" width="3" height="11" rx=".8"/></g></svg>'
            f'<svg width="16" height="11" viewBox="0 0 16 11" aria-hidden="true"><path d="M8 10.5l2.2-2.6a3.2 3.2 0 0 0-4.4 0zM3.4 5.4a6.8 6.8 0 0 1 9.2 0l1.4-1.6a8.9 8.9 0 0 0-12 0z" fill="{c}"/></svg>'
            f'<svg width="25" height="12" viewBox="0 0 25 12" aria-hidden="true"><rect x=".5" y=".5" width="21" height="11" rx="3" fill="none" stroke="{c}" opacity=".5"/><rect x="2" y="2" width="17" height="8" rx="1.8" fill="{c}"/><rect x="22.5" y="4" width="1.8" height="4" rx=".9" fill="{c}" opacity=".5"/></svg></span></div>')


def avatar_btn():
    return ('<svg width="40" height="40" viewBox="0 0 40 40" aria-hidden="true" style="display:block"><circle cx="20" cy="20" r="20" fill="#F3A3BA"/>'
            '<clipPath id="avc"><circle cx="20" cy="20" r="20"/></clipPath><g clip-path="url(#avc)" fill="#FFFFFF"><circle cx="20" cy="15.5" r="7"/><ellipse cx="20" cy="36" rx="13.5" ry="11"/></g></svg>')


def header(title=None, back=False):
    left = ico(BACK, 30, PINK_I, 2.4) if back else ('<svg width="26" height="20" viewBox="0 0 26 20" aria-hidden="true" style="display:block"><g stroke="' + PINK_I + '" stroke-width="2.4" stroke-linecap="round">'
                                                    '<path d="M2 3h22M2 10h22M2 17h22"/></g></svg>')
    t = f'<span style="font:400 33px/1 {HEAD};color:#111;letter-spacing:-.005em">{title}</span>' if title else ''
    return (f'<div style="position:absolute;left:0;right:0;top:50px;height:56px;display:flex;align-items:center;justify-content:center;border-bottom:1px solid #E7E4E6;background:#FFFFFF;z-index:3">'
            f'<span style="position:absolute;left:{18 if back else 22}px;top:{13 if back else 18}px">{left}</span>{t}'
            f'<span style="position:absolute;right:16px;top:8px">{avatar_btn()}</span></div>')


def phone(content, paint_layer='', bg='#FFFFFF'):
    return (f'<div lang="en" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};font-family:{BODY};color:{INK};-webkit-font-smoothing:antialiased">'
            f'{paint_layer}<div style="position:absolute;inset:0;z-index:1">{content}</div>{status()}</div>')


def pill(x, y, w, h, text, size=22, bg=PINK, col='#FFFFFF'):
    return A(x, y, text, f'width:{w}px;height:{h}px;border-radius:{h}px;background:{bg};color:{col};display:flex;align-items:center;justify-content:center;'
                         f'font:600 {size}px/1 {BODY};letter-spacing:.03em;box-shadow:0 6px 14px rgba(226,120,152,.32)')


def label(x, y, text, size=15, wt=600, w=330):
    return A(x, y, text, f'width:{w}px;font:{wt} {size}px/1.62 {BODY};color:{INK}')


def field(x, y, w, h=40, text='', ph=True, size=15):
    t = f'<span style="color:{MUTE if ph else INK2}">{text}</span>' if text else ''
    return A(x, y, t, f'width:{w}px;height:{h}px;box-sizing:border-box;padding:{8 if h > 44 else 0}px 14px;display:flex;align-items:{"flex-start" if h > 44 else "center"};'
                      f'border:1.5px solid #DCD7EC;border-radius:5px;background:#FBFBFE;font:400 {size}px/1.65 {BODY}')


def check(x, y, on=False):
    tick = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 12.5l5 5 10-11" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>' if on else ''
    return A(x, y, tick, f'width:24px;height:24px;box-sizing:border-box;border-radius:3px;display:grid;place-items:center;'
                         f'{"background:" + CHK if on else "border:1.5px solid #D6D3D6;background:#FFFFFF"}')


def radio(x, y, on=False):
    dot = f'<i style="width:12px;height:12px;border-radius:50%;background:{CHK}"></i>' if on else ''
    return A(x, y, dot, f'width:26px;height:26px;box-sizing:border-box;border-radius:50%;display:grid;place-items:center;background:#FFFFFF;'
                        f'border:{"2px solid " + CHK if on else "1.5px solid #D6D3D6"};{"box-shadow:0 0 0 3px #F6D3DE" if on else ""}')


def progress(pct):
    return (A(33, 133, f'<i style="display:block;width:{pct}%;height:100%;background:{GREEN};border-radius:3px"></i>', 'width:324px;height:6px;border-radius:3px;background:#D3D3D3') +
            A(257, 146, f'{pct}%', f'width:100px;text-align:right;font:600 15px/1.4 {BODY};color:{INK}'))


def para(x, y, w, html, size=15.5, lh=1.62, col=INK2, align='left', wt=400):
    return A(x, y, html, f'width:{w}px;font:{wt} {size}px/{lh} {BODY};color:{col};text-align:{align}')


TITLE_GLOW = 'color:#FFFFFF;text-shadow:0 0 18px rgba(255,255,255,.6),0 3px 16px rgba(60,105,122,.35)'


# ---------- website ----------
def site():
    SW, SH = 1280, 800
    nav_l = ''.join(f'<span>{t}</span>' for t in ['How it Works', 'Pool Club', 'Pool Party', 'All About Liv', 'Stories', 'Press', 'Shop'])
    nav = (f'<div style="position:absolute;left:0;right:0;top:0;height:72px;background:#FFFFFF;display:flex;align-items:center;padding:0 28px;gap:30px;z-index:3;box-shadow:0 1px 0 rgba(0,0,0,.06)">'
           f'<img src="img/lv-logo.png" alt="" style="height:52px;width:auto;display:block">'
           f'<nav style="display:flex;gap:26px;font:600 15px/1 {BODY};color:#333">{nav_l}</nav>'
           f'<span style="margin-left:auto;display:flex;align-items:center;gap:26px;font:500 15px/1 {BODY};color:#666">{ico(CART, 26, "#777", 1.5)}<span>Tip Jar</span><span>Podcast</span><span>Sign In</span>'
           f'<span style="padding:11px 26px;border-radius:30px;background:{YEL};color:#222;font-weight:700">Sign Up</span></span></div>')
    ghosts = ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;font:400 {s}px/1 {HEAD};color:rgba(255,255,255,.34);letter-spacing:.02em;white-space:nowrap">{t}</div>'
                     for x, y, s, t in [(640, -40, 300, 'LIV’S'), (930, 250, 300, 'LOVE'), (660, 600, 300, 'POOL')])
    hero = (f'<div style="position:absolute;left:0;right:0;top:72px;bottom:0;overflow:hidden;background:linear-gradient(180deg,#DCEFF5,#C8DFE6)">'
            f'{ghosts}'
            f'<img src="img/lv-photo.jpg" alt="" style="position:absolute;left:0;top:0;height:100%;width:auto;display:block;'
            f'-webkit-mask-image:linear-gradient(90deg,#000 88%,transparent);mask-image:linear-gradient(90deg,#000 88%,transparent)">'
            f'<div style="position:absolute;left:640px;width:460px;top:78px;text-align:center;font:400 108px/1.14 {HEAD};letter-spacing:.06em;{TITLE_GLOW}">LIV’S<br>LOVE<br>POOL</div>'
            f'<div style="position:absolute;left:640px;width:460px;top:488px;text-align:center;font:500 36px/1.2 {BODY};color:#3F4A4E;letter-spacing:.02em">A new way to date.</div>'
            f'<div style="position:absolute;left:770px;width:200px;top:566px;height:62px;border-radius:40px;background:linear-gradient(180deg,#FBE36A,{YEL} 60%,#EFC93A);'
            f'display:flex;align-items:center;justify-content:center;font:700 26px/1 {BODY};color:#222;box-shadow:0 8px 18px rgba(170,140,30,.25)">Dive In</div></div>')
    return (f'<div lang="en" style="position:relative;width:{SW}px;height:{SH}px;overflow:hidden;background:#FFFFFF;font-family:{BODY};-webkit-font-smoothing:antialiased">'
            f'{nav}{hero}</div>')


# ---------- mobile screens ----------
def home():
    steps = ''.join(
        A(30 + k * 68, 742, f'<div style="text-align:center;font:600 15px/1 {BODY};margin-bottom:6px">{k + 1}</div>'
                            f'<div style="position:relative;width:46px;height:46px;margin:0 auto">'
                            f'<svg width="56" height="50" style="position:absolute;left:-4px;top:0" aria-hidden="true">{blob(30, 28, 22, 19, PINK_L if k % 2 else "#F6C3D2", 11 + k)}</svg>'
                            f'<div style="position:relative;padding:4px">{ico(p, 38, INK, 1.25)}</div></div>', 'width:56px')
        for k, p in enumerate([CLIP, CLOCK, HEARTS, PHONE, THUMB]))
    c = (header() +
         A(0, 107, f'<img src="img/lv-photo.jpg" alt="" style="position:absolute;left:-36px;top:-10px;height:470px;width:auto;'
                   f'-webkit-mask-image:linear-gradient(90deg,#000 84%,transparent);mask-image:linear-gradient(90deg,#000 84%,transparent)">'
                   f'<div style="position:absolute;left:150px;width:240px;top:60px;text-align:center;font:400 52px/1.18 {HEAD};letter-spacing:.05em;{TITLE_GLOW}">LIV’S<br>LOVE<br>POOL</div>'
                   f'<div style="position:absolute;left:186px;top:294px;width:164px;height:52px;border-radius:30px;background:linear-gradient(180deg,#FBE36A,{YEL} 60%,#EFC93A);'
                   f'display:flex;align-items:center;justify-content:center;font:600 22px/1 {BODY};color:#222;box-shadow:0 6px 14px rgba(170,140,30,.25)">Dive in</div>',
           f'width:390px;height:384px;overflow:hidden;background:linear-gradient(180deg,#DCEFF5,#C9E1E8)') +
         para(0, 518, 390, 'Dive in to see who might be<br>waiting just for YOU!', 18, 1.45, INK, 'center', 500) +
         A(0, 646, 'How It Works', f'width:390px;text-align:center;font:400 34px/1 {HEAD};color:#111') +
         steps +
         para(0, 832, 390, 'Fill out the form, sit tight, and let Liv', 15.5, 1.4, INK2, 'center'))
    return phone(c)


def how():
    c = (header('How it Works') +
         A(26, 142, '1', f'font:400 92px/1 {HEAD};color:#111') +
         A(90, 168, 'Fill out the form', f'font:400 25px/1 {HEAD};color:#111') + A(325, 158, ico(CLIP, 36, INK, 1.3)) +
         para(92, 208, 270, 'Okay so here’s the SCOOP: the first thing you do is <b style="font-weight:700;color:#222">fill out this cute little form! Then you fly onto my waitlist. Entering the pool is totally free.</b> '
                            'Don’t overthink it; you’re perfect and I love you. You’ll also have to sign my <b style="font-weight:700;color:#222">Code of Conduct</b>: I just wanna protect all my noodles and make sure everyone is being nice.', 15, 1.66) +
         pill(68, 492, 256, 50, 'Create Account', 21) +
         A(26, 610, '2', f'font:400 84px/1 {HEAD};color:#111') +
         A(90, 630, 'Get on the Waitlist', f'font:400 25px/1 {HEAD};color:#111') + A(330, 622, ico(CLOCK, 34, INK, 1.3)) +
         para(92, 668, 278, '<b style="font-weight:700;color:#222">Congrats: you’re on my Waitlist! Now you just sit back and relax!</b> Have some juice! Get a snack! '
                            'Because I’m a one-lady matchmaking machine, it takes a minute for me to read over everyone’s entries and start my', 15, 1.66))
    p = paint(blob(36, 190, 64, 66, CREAM, 4, rot=-8), blob(30, 640, 58, 62, BLUE, 7, rot=10))
    return phone(c, p)


def acct20():
    c = (header('Create Account') + progress(20) +
         A(33, 196, 'Already have an account? Sign In', f'width:324px;text-align:right;font:500 15px/1.4 {BODY};color:{INK2};text-decoration:underline;text-underline-offset:3px') +
         label(33, 266, 'First name') + field(33, 294, 324) +
         label(33, 402, 'Last name') + field(33, 428, 324) +
         label(33, 536, 'Phone number') + field(33, 562, 324, text='(___) ___ - ____') +
         para(33, 610, 326, 'I think phone calls are the best way to really get to know someone you meet over a dating app. That means I’ll share your number with your match, and no one else.', 14.5, 1.68) +
         label(33, 772, 'How old are you? (Must be 21+)') + field(33, 800, 324))
    p = paint(swash([(-30, 330), (120, 370), (300, 450), (430, 520)], 74, CREAM, .85, 2), swash([(330, 480), (380, 560)], 46, CREAM, .8, 5),
              swash([(-30, 860), (180, 800), (430, 700)], 52, BLUE, .75, 8))
    return phone(c, p)


def opt(x, y, text, on=False, blank=False):
    return check(x, y, on) + (field(x + 34, y - 10, 284, 40) if blank else A(x + 34, y + 2, text, f'font:500 16px/1.25 {BODY};color:{INK2}'))


def acct40():
    c = (header('Create Account') + progress(40) +
         label(33, 182, 'Location / Major city') + field(33, 210, 324) +
         label(36, 298, 'Gender identity? (Check all that apply)') +
         opt(48, 338, 'Woman') + opt(48, 371, 'Man') + opt(48, 404, 'Nonbinary', True) + opt(48, 442, '', blank=True) +
         label(36, 524, 'Who would you like to meet? (Check all that apply)', w=320) +
         opt(48, 590, 'Women') + opt(48, 623, 'Men', True) + opt(48, 656, 'Everyone') + opt(48, 694, '', blank=True) +
         label(36, 790, 'Are you interested in ~possibly~ being featured on my podcast?', w=320))
    p = paint(swash([(-30, 400), (200, 300), (430, 200)], 46, PINK_L, .9, 3), swash([(-30, 510), (200, 515), (430, 548)], 40, LAV, .85, 6),
              swash([(-30, 676), (200, 760), (430, 850)], 62, CREAM, .85, 9))
    return phone(c, p)


def acct60():
    c = (header('Create Account') + progress(60) +
         label(33, 182, 'Tell me a fact about yourself:') +
         field(33, 210, 324, 122, 'I was a birthday party clown for a time and I once went on a date with a cannibalistic clown.') +
         label(33, 400, 'Tell me ANOTHER fact about yourself') +
         field(33, 428, 324, 122, 'If I’m not wearing high heels in some form, it’s absolutely safe to assume my body has been taken over by goddamn aliens.') +
         label(33, 618, 'OKAY ONE MORE FACT') +
         field(33, 646, 324, 122, 'If you can make me laugh until I can’t breathe and I have tears streaming down my face, I will be yours forever.') +
         label(33, 822, 'What would you say is your MOST'))
    p = paint(swash([(-30, 190), (200, 270), (360, 330), (380, 380)], 56, BLUE, .85, 1), swash([(-30, 670), (200, 600), (430, 528)], 44, PINK_L, .9, 4),
              blob(30, 830, 90, 60, LAV, 12, op=.9))
    return phone(c, p)


def acct80():
    c = (header('Create Account') + progress(80) +
         label(36, 182, 'Is this your first time doing Liv’s Love Pool?', w=320) +
         radio(46, 252) + para(82, 246, 280, 'This is my first time (and they say you NEVER forget your first)', 15.5, 1.6) +
         radio(46, 318, True) + para(82, 310, 280, 'I did it before I’m BACK FOR MORE BISH', 15.5, 1.6) +
         label(36, 418, 'Who referred you? Or maybe you just FOUND me? That’s totally cool, just let a sister know so I don’t accidentally match you with YOUR sister', w=326) +
         field(36, 527, 322) +
         label(36, 636, 'ANYTHING ELSE??!!??!?!') + field(36, 662, 322) +
         A(36, 780, 'Back', f'font:500 21px/1 {BODY};color:{INK}') + pill(196, 766, 164, 46, 'Next', 21))
    p = paint(swash([(-30, 210), (200, 196), (430, 212)], 44, CREAM, .85, 2), swash([(-30, 540), (200, 600), (430, 664)], 54, BLUE, .8, 7))
    return phone(c, p)


def conduct():
    lorem = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce scelerisque imperdiet lorem, eget malesuada lacus rutrum sed. Duis commodo et felis commodo dignissim. '
             'Duis quam arcu, sagittis eget erat ac, tempus mattis velit. Vivamus tincidunt nisi ut auctor malesuada. Nunc dignissim tincidunt justo bibendum suscipit.')
    c = (header('Create Account') + progress(85) +
         A(0, 180, 'Code of Conduct', f'width:390px;text-align:center;font:400 26px/1 {HEAD};color:#111') +
         para(33, 262, 330, 'Before you join up, don’t forget to read and sign the LLP Code of Conduct!', 18, 1.45, INK, 'left', 500) +
         A(33, 356, lorem, f'width:326px;box-sizing:border-box;padding:18px 20px;border-radius:8px;background:#FFFFFF;box-shadow:0 2px 12px rgba(0,0,0,.13);font:400 14.5px/1.72 {BODY};color:{INK2}') +
         label(33, 692, 'Electronic Signature') + field(33, 718, 324, 42, 'Catherine Combs') +
         A(33, 805, 'Back', f'font:500 21px/1 {BODY};color:{INK}') + pill(194, 790, 166, 46, 'Next', 21))
    p = paint(swash([(-10, 196), (130, 192), (260, 200), (400, 190)], 64, BLUE, .9, 5), blob(350, 205, 50, 30, BLUE, 3, op=.9))
    return phone(c, p)


def confetti():
    r = random.Random(42)
    cols = ['#F2A0B8', '#F8D84A', '#8FCBDD', '#B6A5E6', '#F48A6A', '#8FD19E', '#E8789C']
    out = ''
    while out.count('<circle') < 260:
        x, y = r.uniform(0, 390), r.uniform(170, 600)
        centre = 70 < x < 320 and 300 < y < 570
        if centre and r.random() < .75:
            continue
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(.7, 1.8):.1f}" fill="{r.choice(cols)}" opacity="{r.uniform(.5, .95):.2f}"/>'
    return out


def youre_in():
    c = (header() + progress(100) +
         A(0, 200, 'YOU’RE IN', f'width:390px;text-align:center;font:400 27px/1 {HEAD};color:#111;letter-spacing:.01em') +
         para(0, 312, 390, 'Wow omg you did it<br>welcome to the Pool!', 19, 1.38, INK, 'center', 500) +
         para(0, 414, 390, 'I love you and you’re<br>perfect.', 19, 1.38, INK, 'center', 500) +
         para(0, 488, 390, 'I’ll shoot ya a text as<br>soon as I find someone<br>amazing!!', 19, 1.38, INK, 'center', 500) +
         pill(94, 616, 202, 46, 'My Account', 21))
    p = paint(confetti(), swash([(-20, 214), (120, 206), (190, 196), (260, 206), (410, 210)], 66, LAV, .95, 1))
    return phone(c, p)


# ---------- My Account ----------
def tabs(active):
    cells = ''
    for k, (p, name) in enumerate([(PERSON, 'Profile'), (HEART, 'Matches'), (GEARS, 'Settings')]):
        on = k == active
        cells += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center">'
                  f'<div style="width:100%;height:78px;display:grid;place-items:center;background:{BLUE if on else TAB};{"box-shadow:inset 0 -3px 0 rgba(0,0,0,.06)" if on else ""}">'
                  f'{ico(p, 46, "none", 0, PINK_D if on else "#FFFFFF")}</div>'
                  f'<span style="margin-top:12px;font:{600 if on else 500} {19 if on else 17}px/1 {BODY};color:{INK if on else "#5E5A5D"}">{name}</span></div>')
    return A(0, 107, cells, 'width:390px;display:flex')


def av(src, size=84):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#FFFFFF;box-shadow:0 2px 10px rgba(0,0,0,.14);overflow:hidden;display:grid;place-items:center">'
            f'<img src="{src}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>')


def info_rows(x, y, items, seed=20):
    out = ''
    for k, (p, t) in enumerate(items):
        out += A(x, y + k * 26, f'<span style="position:relative;width:24px;height:22px;flex:none">'
                                f'<svg width="30" height="28" style="position:absolute;left:-4px;top:-3px" aria-hidden="true">{blob(15, 14, 12, 11, PINK_L, seed + k)}</svg>'
                                f'<span style="position:relative">{ico(p, 22, "#5E5A5D", 1.3)}</span></span><span>{t}</span>',
                 f'display:flex;align-items:center;gap:10px;font:500 17px/1 {BODY};color:#4A4648;white-space:nowrap')
    return out


def phone_line(x, y, size=25):
    return A(x, y, f'<span style="display:block;color:{PINK_I}">{ico(PHONE, 26, PINK_I, 1.4)}</span><span>555-555-5555</span>',
             f'display:flex;align-items:center;gap:8px;font:500 {size}px/1 {BODY};color:{INK}')


def profile():
    c = (header('My Account') + tabs(0) +
         A(37, 276, '', 'width:314px;height:290px;border-radius:6px;background:#FFFFFF;box-shadow:0 2px 12px rgba(0,0,0,.13)') +
         A(304, 296, ico(PENCIL, 30, '#444', 1.3)) +
         f'<svg style="position:absolute;left:0;top:0" width="390" height="844" aria-hidden="true">{blob(214, 386, 128, 64, CREAM, 31, rot=-4)}</svg>' +
         A(150, 235, av('img/lv-av-catherine.png', 86)) +
         A(0, 346, 'Catherine, 26', f'width:372px;text-align:center;font:500 24px/1 {BODY};color:{INK}') +
         phone_line(104, 392) +
         info_rows(70, 464, [(HOME, 'New York City'), (CASE, 'Marketing Manager'), (CAP, 'Penn State')], 40) +
         A(0, 588, 'Upgrade to Premium', f'width:390px;text-align:center;font:600 19px/1 {BODY};color:{PINK_D};text-decoration:underline;text-underline-offset:4px') +
         A(52, 656, 'Fun Fact #1', f'font:500 23px/1 {BODY};color:{INK}') +
         A(52, 690, 'I was a backup dancer<br>for Beyonce once', f'width:282px;height:150px;box-sizing:border-box;padding:12px 14px;border:1.5px solid #E1DDE8;border-radius:4px;background:rgba(255,255,255,.85);font:400 17px/1.5 {BODY};color:{INK2}') +
         A(300, 702, ico(PENCIL, 28, '#444', 1.3)))
    p = paint(swash([(-20, 740), (180, 690), (380, 640)], 48, BLUE, .85, 4), blob(10, 840, 70, 40, PINK_L, 6))
    return phone(c, p)


def matches():
    c = (header('My Account') + tabs(1) +
         A(31, 282, '', f'width:322px;height:127px;border-radius:3px;background:{LAV};box-shadow:0 3px 8px rgba(0,0,0,.14)') +
         A(42, 300, av('img/lv-av-james.png', 90)) +
         A(142, 306, 'James<br>Age 27<br>555-555-5555', f'font:500 20px/1.3 {BODY};color:{INK}') +
         A(286, 352, ico(PHONE, 24, PINK_I, 1.4)) + A(322, 330, ico(CHEV, 26, INK, 2)) +
         A(31, 445, '', 'width:322px;height:129px;border-radius:3px;background:#D0D0D0;box-shadow:0 3px 8px rgba(0,0,0,.14)') +
         A(42, 462, '?', f'width:90px;height:90px;border-radius:50%;background:#FFFFFF;display:grid;place-items:center;font:300 64px/1 {BODY};color:#222') +
         para(150, 466, 190, 'To unlock your next match, fill out the <b style="font-weight:700;color:#222">Date Feedback</b> form', 17, 1.45, '#4A4648') +
         pill(66, 610, 256, 48, 'Date Feedback', 21) +
         A(66, 826, '', 'width:70px;height:70px;border-radius:50%;background:#6CC56F') +
         A(160, 826, '', 'width:72px;height:70px;border-radius:18px;border:5px solid #7B4FC9;box-sizing:border-box') +
         A(258, 826, '', 'width:70px;height:70px;border-radius:50%;background:#A86BE8'))
    p = paint(swash([(-20, 742), (200, 760), (420, 790)], 64, CREAM, .9, 2))
    return phone(c, p)


def match_detail():
    c = (header('My Account', back=True) + tabs(1) +
         A(38, 276, '', 'width:313px;height:290px;border-radius:6px;background:#FFFFFF;box-shadow:0 2px 12px rgba(0,0,0,.13)') +
         f'<svg style="position:absolute;left:0;top:0" width="390" height="844" aria-hidden="true">{blob(214, 388, 132, 64, LAV, 52, rot=6)}</svg>' +
         A(150, 235, av('img/lv-av-james.png', 86)) +
         A(0, 346, 'James, age 27', f'width:420px;text-align:center;font:500 24px/1 {BODY};color:{INK}') +
         phone_line(124, 392, 24) +
         info_rows(80, 464, [(HOME, 'New York City'), (CASE, 'Software Engineer'), (CAP, 'University of Washington')], 60) +
         para(0, 598, 390, 'To unlock your next match, tell me how<br>your date went with James', 15.5, 1.55, '#4A4648', 'center') +
         pill(66, 660, 256, 48, 'Date Feedback', 21) +
         A(38, 748, '', 'width:313px;height:120px;border-radius:6px;background:#FFFFFF;box-shadow:0 2px 12px rgba(0,0,0,.13)') +
         f'<svg style="position:absolute;left:0;top:0" width="390" height="844" aria-hidden="true">{blob(104, 778, 64, 22, CREAM, 70)}</svg>' +
         A(60, 764, 'Fun Fact #1', f'font:500 23px/1 {BODY};color:{INK}') +
         para(60, 806, 260, 'I’ve met the king of<br>Spain', 17, 1.5))
    return phone(c)


def feedback():
    shape = smooth([(-10, 106), (150, 112), (330, 136), (372, 190), (390, 280), (392, 360), (330, 330), (220, 270), (90, 240), (40, 200), (-10, 190)])
    c = (header('Feedback', back=True) +
         para(49, 172, 300, 'Let me know how your date went<br>to unlock your next match!', 16, 1.6, '#4A4648') +
         A(53, 256, 'Who was the date with?', f'font:500 19px/1 {BODY};color:{INK}') +
         A(53, 280, '<i style="display:block;width:1px;height:18px;background:#999"></i>', 'width:284px;height:36px;box-sizing:border-box;padding:9px 14px;border:1.5px solid #E2DEE6;border-radius:5px;background:#FFFFFF') +
         A(53, 352, 'How did your date go?', f'font:500 19px/1 {BODY};color:{INK}') +
         A(53, 382, '<i style="display:block;width:1px;height:18px;background:#999"></i>', 'width:278px;height:414px;box-sizing:border-box;padding:12px 14px;border:1.5px solid #E2DEE6;border-radius:5px;background:#FFFFFF'))
    return phone(c, paint(f'<path d="{shape}" fill="{PINK_L}" opacity=".95"/>'))


def thanks():
    shape = smooth([(-10, 106), (200, 110), (350, 150), (392, 230), (392, 360), (300, 300), (200, 250), (90, 230), (-10, 220)])
    act = lambda x, p, t, seed: (A(x - 46, 628, f'<svg width="92" height="84" style="position:absolute;left:0;top:0" aria-hidden="true">{blob(50, 44, 38, 36, "#F6BFD0", seed)}</svg>'
                                              f'<div style="position:relative;left:16px;top:8px">{ico(p, 62, "#555", 1.1)}</div>', 'width:92px;height:84px') +
                                 A(x - 70, 722, t, f'width:140px;text-align:center;font:500 17px/1.5 {BODY};color:#3D3A3C;text-decoration:underline;text-underline-offset:3px'))
    c = (header('Feedback') +
         A(0, 176, 'THANKS!', f'width:390px;text-align:center;font:400 40px/1 {HEAD};color:#111;letter-spacing:.02em') +
         para(0, 340, 390, 'Thank you for letting me know<br>how your date went!', 16.5, 1.55, '#4A4648', 'center') +
         para(0, 416, 390, 'You have unlocked your next<br>match and will be hearing back<br>from me soon!', 16.5, 1.55, '#4A4648', 'center') +
         para(0, 544, 390, 'In the meantime you can:', 16.5, 1.55, '#4A4648', 'center') +
         act(124, MIC, 'Listen to<br>my podcast', 81) + act(272, HEARTS, 'Read match<br>stories', 83))
    return phone(c, paint(f'<path d="{shape}" fill="{PINK_L}" opacity=".95"/>'))


def board(bid, title, html, w=W, h=H):
    return {'id': bid, 'title': title, 'w': w, 'h': h, 'lang': 'en', 'dir': None,
            'css': ':host{margin:0}\n*{box-sizing:border-box}\n', 'html': html, 'fonts': FONTS}


def build():
    out = [board('LvSite', 'Website home page', site(), 1280, 800),
           board('LvHome', 'Mobile home page', home()),
           board('LvHow', 'How it Works', how()),
           board('LvAcct20', 'Create Account, 20%', acct20()),
           board('LvAcct40', 'Create Account, 40%', acct40()),
           board('LvAcct60', 'Create Account, 60%', acct60()),
           board('LvAcct80', 'Create Account, 80%', acct80()),
           board('LvConduct', 'Code of Conduct, 85%', conduct()),
           board('LvIn', 'You’re in, 100%', youre_in()),
           board('LvProfile', 'My Account: profile', profile()),
           board('LvMatches', 'My Account: matches', matches()),
           board('LvMatch', 'My Account: match details', match_detail()),
           board('LvFeedback', 'Date feedback', feedback()),
           board('LvThanks', 'Thanks', thanks())]
    path = os.path.join(ROOT, 'src', 'cases', 'livs-love-pool.boards.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path, len(out), 'boards')


if __name__ == '__main__':
    build()
