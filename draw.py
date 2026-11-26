#!/usr/bin/env python3
"""Draw the front page for news-image-20261126.

Build-time only: renders the 1024x1024 newspaper front page
'The World in One Picture - Thursday 26 November 2026' entirely in code
(Python PIL, no network, no photographs) and writes entry.png next to
this file. Deterministic: fixed palette, fixed fonts, no timestamps,
no randomness.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (179, 39, 30)
GREEN = (118, 185, 0)
DGREEN = (74, 124, 0)
GOLD = (217, 164, 65)
PALE_GREEN = (233, 242, 216)
GREY = (110, 110, 108)

FL = "/usr/share/fonts/truetype/liberation"
FD = "/usr/share/fonts/truetype/dejavu"


def f_serif(size, bold=False, italic=False):
    if bold and italic:
        return ImageFont.truetype(f"{FL}/LiberationSerif-BoldItalic.ttf", size)
    if bold:
        return ImageFont.truetype(f"{FL}/LiberationSerif-Bold.ttf", size)
    if italic:
        return ImageFont.truetype(f"{FL}/LiberationSerif-Italic.ttf", size)
    return ImageFont.truetype(f"{FL}/LiberationSerif-Regular.ttf", size)


def f_sans(size, bold=False):
    if bold:
        return ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", size)
    return ImageFont.truetype(f"{FD}/DejaVuSans.ttf", size)


def wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, lh, fill=INK, max_lines=None):
    lines = wrap(text, font, max_w, draw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, size=15):
    draw.text((x, y), text, font=f_sans(size, bold=True), fill=RED)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 26                      # margin
RX = W - MX                  # right edge

# ---------------------------------------------------------------- masthead
name = "THE WORLD IN ONE PICTURE"
nf = f_serif(56, bold=True)
while d.textlength(name, font=nf) > RX - MX and nf.size > 30:
    nf = f_serif(nf.size - 2, bold=True)
d.text(((W - d.textlength(name, font=nf)) / 2, 22), name, font=nf, fill=INK)
rule(d, MX, 96, RX, 3)
rule(d, MX, 101, RX, 1)
df = f_sans(15, bold=True)
d.text((MX, 108), "THURSDAY, 26 NOVEMBER 2026", font=df, fill=INK)
mid = "ONE DAY  ·  ONE PAGE  ·  ALL THE NEWS"
d.text(((W - d.textlength(mid, font=df)) / 2, 108), mid, font=df, fill=INK)
pr = "PRICE: FREE"
d.text((RX - d.textlength(pr, font=df), 108), pr, font=df, fill=INK)

# ---------------------------------------------------------------- lead story
LY = 136
kicker(d, MX, LY, "TECHNOLOGY  ·  THE AI CHIPMAKER", 15)
hf = f_serif(64, bold=True)
while d.textlength("HUANG IS BACK", font=hf) > RX - MX and hf.size > 40:
    hf = f_serif(hf.size - 2, bold=True)
d.text((MX, LY + 22), "HUANG IS BACK", font=hf, fill=INK)
rule(d, MX, LY + 100, RX, 2)

LX, LW = MX, 560
ty = LY + 116
deck = ("Nvidia's board votes unanimously to reinstate its founder as chief "
        "executive, 11 days after his resignation \u2014 the most abrupt "
        "U-turn of the AI boom.")
ty = para(d, LX, ty, deck, f_serif(21, italic=True), LW, 27)
ty += 8
body = ("Jensen Huang quit on 12 November after reports of affairs, one "
        "involving a woman US officials believe is a Chinese spy. Chief "
        "financial officer Colette Kress served as interim chief. On Monday "
        "the board reversed course and voted unanimously to bring him back. "
        "Shares whipsawed, falling about 5% on Wednesday as AI stocks "
        "bounced off morning lows.")
ty = para(d, LX, ty, body, f_sans(16), LW, 21)

# hero illustration: the chip, crowned (panel 604..998 x 244..462)
PX0, PY0, PX1, PY1 = 604, 244, RX, 462
d.rectangle([PX0, PY0, PX1, PY1], fill=PALE_GREEN, outline=INK, width=2)
cx = (PX0 + PX1) // 2
# crown, small and clean
cy0 = PY0 + 8
d.polygon([(cx - 48, cy0 + 28), (cx - 48, cy0 + 10), (cx - 24, cy0 + 22),
           (cx, cy0 + 4), (cx + 24, cy0 + 22), (cx + 48, cy0 + 10),
           (cx + 48, cy0 + 28)], fill=GOLD, outline=(150, 105, 20))
for ox, oy in ((-48, cy0 + 10), (0, cy0 + 4), (48, cy0 + 10)):
    d.ellipse([cx + ox - 4, oy - 4, cx + ox + 4, oy + 4], fill=GOLD,
              outline=(150, 105, 20))
# chip body, 112px
S = 112
chip_cy = PY0 + 108
x0, y0 = cx - S // 2, chip_cy - S // 2
x1, y1 = cx + S // 2, chip_cy + S // 2
for i in range(4):  # pins, 4 per side
    off = 12 + i * 26
    d.rectangle([x0 + off, y0 - 10, x0 + off + 12, y0], fill=(61, 61, 61))
    d.rectangle([x0 + off, y1, x0 + off + 12, y1 + 10], fill=(61, 61, 61))
    d.rectangle([x0 - 10, y0 + off, x0, y0 + off + 12], fill=(61, 61, 61))
    d.rectangle([x1, y0 + off, x1 + 10, y0 + off + 12], fill=(61, 61, 61))
d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=GREEN,
                    outline=DGREEN, width=3)
for tx in (x0 + 26, x0 + 56, x0 + 86):
    d.line([(tx, y0 + 34), (tx, y0 + 12)], fill=DGREEN, width=2)
    d.line([(tx, y1 - 34), (tx, y1 - 12)], fill=DGREEN, width=2)
dx0, dy0, dx1, dy1 = cx - 40, chip_cy - 30, cx + 40, chip_cy + 30
d.rectangle([dx0, dy0, dx1, dy1], fill=(78, 138, 0), outline=(255, 255, 255),
            width=2)
nv = f_sans(24, bold=True)
t = "NVDA"
d.text((cx - d.textlength(t, font=nv) / 2, chip_cy - 16), t, font=nv,
       fill=(255, 255, 255))
ai = f_sans(11, bold=True)
t2 = "AI INSIDE"
d.text((cx - d.textlength(t2, font=ai) / 2, chip_cy + 12), t2, font=ai,
       fill=(230, 245, 200))
cap = "The founder returns \u2014 Jensen Huang, back at Nvidia 11 days after he quit."
para(d, PX0 + 14, PY1 - 38, cap, f_serif(14, italic=True), PX1 - PX0 - 28, 17)

# ---------------------------------------------------------------- second row
RY = 486
rule(d, MX, RY - 8, RX, 2)
col_w = (RX - MX - 24) // 2


def story2(x, kick, head, body_text, thumb):
    kicker(d, x, RY, kick, 13)
    hy = RY + 20
    for ln in wrap(head, f_serif(23, bold=True), col_w - 190, d)[:3]:
        d.text((x + 190, hy), ln, font=f_serif(23, bold=True), fill=INK)
        hy += 26
    para(d, x + 190, hy + 4, body_text, f_sans(14), col_w - 190, 18,
         max_lines=3)
    thumb(d, x, RY + 20, 178, 132)


def thumb_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 235), outline=INK, width=2)
    # runway strip along the bottom
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(96, 96, 96))
    for i in range(5):
        d.line([(x + 12 + i * 34, y + h - 13), (x + 30 + i * 34, y + h - 13)],
               fill=(255, 255, 255), width=2)
    # smoke plume rising from the runway
    for i, r in enumerate((6, 9, 12)):
        d.ellipse([x + 34 + i * 10, y + h - 52 - i * 12 - r,
                   x + 34 + i * 10 + r * 2, y + h - 52 - i * 12 + r],
                  fill=(150, 150, 150))
    # jet in profile, flying right
    jx, jy = x + 62, y + 44
    d.polygon([(jx - 22, jy + 12), (jx + 58, jy + 4), (jx + 70, jy + 9),
               (jx + 58, jy + 15), (jx - 14, jy + 20), (jx - 22, jy + 12)],
              fill=(40, 40, 40))
    d.polygon([(jx - 14, jy + 12), (jx - 18, jy - 6), (jx - 6, jy + 10)],
              fill=(40, 40, 40))
    d.polygon([(jx + 18, jy + 16), (jx + 10, jy + 30), (jx + 28, jy + 18)],
              fill=(40, 40, 40))


def thumb_korea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 32), outline=INK, width=2)
    d.text((x + 10, y + 10), "PYONGYANG", font=f_sans(11, bold=True),
           fill=(220, 220, 220))
    d.ellipse([x + w - 78, y + 8, x + w - 8, y + 78], fill=RED)
    mx, my = x + 62, y + 96
    d.polygon([(mx - 8, my - 52), (mx + 2, my - 66), (mx + 12, my - 52),
               (mx + 10, my + 6), (mx - 6, my + 6)], fill=(200, 200, 200),
              outline=(120, 120, 120))
    d.polygon([(mx - 6, my + 6), (mx - 16, my + 18), (mx - 6, my + 14)],
              fill=(160, 160, 160))
    d.polygon([(mx + 10, my + 6), (mx + 20, my + 18), (mx + 10, my + 14)],
              fill=(160, 160, 160))
    d.polygon([(mx - 4, my + 18), (mx + 2, my + 30), (mx + 8, my + 18)],
              fill=(255, 170, 60))
    d.line([(x + 8, y + h - 12), (x + w - 8, y + h - 12)], fill=(120, 120, 120),
           width=3)


story2(MX, "WAR IN UKRAINE", "KYIV SAYS IT HIT A RUSSIAN AIR BASE",
       "Ukraine says it struck a major air base, damaging five planes. "
       "Moscow's toll nears 500,000.",
       thumb_ukraine)
story2(MX + col_w + 24, "NORTH KOREA", "KIM ORDERS MORE TACTICAL NUCLEAR ARMS",
       "Kim Jong Un calls for tactical nuclear weapons to be deployed more "
       "widely, state media reports.",
       thumb_korea)

# ---------------------------------------------------------------- third row
TY = 660
rule(d, MX, TY - 8, RX, 2)
tw = (RX - MX - 36) // 3
TH = 96  # thumbnail height


def thumb_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 226, 228), outline=INK, width=2)
    base = y + h
    d.rectangle([x + 14, base - 46, x + 120, base - 8], fill=(52, 52, 52))
    d.polygon([(x + 14, base - 46), (x + 40, base - 62), (x + 66, base - 46),
               (x + 92, base - 62), (x + 120, base - 46)], fill=(52, 52, 52))
    d.rectangle([x + 128, base - 72, x + 140, base - 8], fill=(52, 52, 52))
    for i in range(3):
        d.ellipse([x + 124 + i * 4, base - 88 + i * 10, x + 140 + i * 4,
                   base - 72 + i * 10], fill=(180, 180, 180))
    d.line([(x + 160, base - 20), (x + 200, base - 46), (x + 232, base - 32),
            (x + 268, base - 66)], fill=RED, width=4)
    d.polygon([(x + 268, base - 66), (x + 250, base - 68), (x + 264, base - 50)],
              fill=RED)


def thumb_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 18, 26), outline=INK, width=2)
    for sx, sy in ((30, 16), (90, 10), (240, 22), (270, 60), (60, 78), (200, 82)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    cx, cy, r = x + 112, y + h // 2 + 4, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(184, 168, 143),
              outline=(140, 126, 104), width=2)
    for crx, cry, cr in ((92, 44, 8), (132, 66, 10), (88, 72, 6), (142, 34, 5)):
        d.ellipse([x + crx - cr, y + cry - cr, x + crx + cr, y + cry + cr],
                  fill=(150, 136, 112))
    d.rectangle([x + 214, y + 26, x + 234, y + 44], fill=(220, 220, 220),
                outline=(120, 120, 120))
    d.rectangle([x + 192, y + 30, x + 214, y + 40], fill=(90, 130, 200))
    d.rectangle([x + 234, y + 30, x + 256, y + 40], fill=(90, 130, 200))
    d.line([(x + 224, y + 26), (x + 224, y + 14)], fill=(220, 220, 220), width=2)
    d.ellipse([x + 220, y + 8, x + 228, y + 16], fill=(255, 220, 100))


def thumb_cairo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 214, 170), outline=INK, width=2)
    base = y + h
    d.rectangle([x, base - 28, x + w, base], fill=(90, 90, 90))
    for i in range(6):
        d.line([(x + 10 + i * 48, base - 14), (x + 34 + i * 48, base - 14)],
               fill=(255, 220, 60), width=3)
    d.rounded_rectangle([x + 60, base - 62, x + 210, base - 28], radius=12,
                        fill=(200, 200, 200), outline=(80, 80, 80), width=2)
    d.ellipse([x + 60, base - 62, x + 92, base - 28], fill=(170, 170, 170),
              outline=(80, 80, 80), width=2)
    d.ellipse([x + 178, base - 62, x + 210, base - 28], fill=(170, 170, 170),
              outline=(80, 80, 80), width=2)
    for wx in (92, 172):
        d.ellipse([x + wx, base - 26, x + wx + 22, base - 4], fill=(30, 30, 30))
    d.polygon([(x + 96, base - 58), (x + 108, base - 92), (x + 120, base - 66),
               (x + 134, base - 96), (x + 146, base - 58)], fill=(255, 120, 20))
    d.polygon([(x + 108, base - 58), (x + 118, base - 74), (x + 130, base - 58)],
              fill=(255, 210, 60))


def story3(x, kick, head, body_text, thumb):
    thumb(d, x, TY, tw, TH)
    yy = TY + TH + 8
    kicker(d, x, yy, kick, 13)
    yy += 20
    for ln in wrap(head, f_serif(22, bold=True), tw, d)[:2]:
        d.text((x, yy), ln, font=f_serif(22, bold=True), fill=INK)
        yy += 26
    para(d, x, yy + 2, body_text, f_sans(14), tw, 18, max_lines=2)


story3(MX, "UNITED STATES", "WASHINGTON PLANS NEW TARIFFS",
       "New US tariffs target factory overcapacity; a second judge blocks "
       "the birthright order.",
       thumb_tariffs)
story3(MX + tw + 18, "SPACE", "EIGHT YEARS ON, A DATE WITH MERCURY",
       "BepiColombo reaches Mercury orbit after an eight-year journey.",
       thumb_mercury)
story3(MX + 2 * (tw + 18), "EGYPT", "AT LEAST 30 KILLED IN CAIRO TANKER FIRE",
       "A fuel tanker crashes and ignites on a highway outside Cairo, "
       "killing at least 30.",
       thumb_cairo)

# ---------------------------------------------------------------- in brief
BY = 884
rule(d, MX, BY - 8, RX, 2)
d.rectangle([MX, BY, RX, BY + 28], fill=INK)
d.text((MX + 10, BY + 5), "IN BRIEF", font=f_sans(17, bold=True),
       fill=(255, 255, 255))
rt = "AROUND THE WORLD IN EIGHT LINES"
d.text((RX - 10 - d.textlength(rt, font=f_sans(12, bold=True)), BY + 8), rt,
       font=f_sans(12, bold=True), fill=(200, 200, 200))

briefs = [
    ("COLOMBIA", "Police free 20 supermarket hostages held 17 hours."),
    ("NORWAY", "Court rules climate-disputed oil licences invalid."),
    ("LEBANON", "Second airport opens next month; Hezbollah sway fades."),
    ("EBOLA", "Kenya's last Ebola patient out; DRC toll tops 5,300."),
    ("EUROPE", "EU seeks a new ECB chief as Lagarde resigns."),
    ("SPORT", "Chess game 2 drawn in 20 moves; IPL auction draws 1,220."),
    ("OBITUARY", "Duran Duran guitarist Andy Taylor dies at 65."),
    ("ASIA", "Pakistan's first astronaut joins China's station crew."),
]
bf = f_sans(13)
bcol_w = (RX - MX - 24) // 2
for i, (tag, txt) in enumerate(briefs):
    col = i % 2
    row = i // 2
    bx = MX + col * (bcol_w + 24)
    by = BY + 38 + row * 19
    d.rectangle([bx, by + 3, bx + 8, by + 11], fill=RED)
    line = f"{tag} \u2014 {txt}"
    while d.textlength(line, font=bf) > bcol_w - 16 and " " in line:
        line = line.rsplit(" ", 1)[0] + " \u2026"
    d.text((bx + 14, by), line, font=bf, fill=INK)

# ---------------------------------------------------------------- footer
rule(d, MX, 1000, RX, 1)
ft = "Drawn entirely in code  ·  No photographs  ·  Headlines as reported on Thursday 26 November 2026"
ff = f_sans(12)
d.text(((W - d.textlength(ft, font=ff)) / 2, 1006), ft, font=ff, fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, format="PNG", optimize=True)
print(f"wrote {out} {img.size} {os.path.getsize(out)} bytes")
