#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: 'THE WORLD — Monday 23 November 2026'.

Fresh code written in this session (2026-11-23). Draws a one-page newspaper
front page for Monday 23 November 2026 from live reporting of that morning:
COP31 collapse fallout, the Gulf war, India closing in on New Zealand,
Modi-Shah talks in Delhi, South Korea's minister quitting over AI exam
cheating, and BepiColombo at Mercury. All vector art, Pillow only.
Run:  python3 draw.py [v1|v2|v3] [outfile.png]   (default v1 entry.png)
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (20, 32, 46)
INK_SOFT = (52, 66, 84)
RED = (179, 38, 30)
WHITE = (255, 253, 246)
GREY = (120, 116, 108)

FDIR = "/usr/share/fonts/truetype"
SERIF = f"{FDIR}/noto/NotoSerif-Bold.ttf"
SERIF_BLACK = f"{FDIR}/noto/NotoSerif-Black.ttf"
SERIF_IT = f"{FDIR}/noto/NotoSerif-Italic.ttf"
SANS = f"{FDIR}/noto/NotoSans-Regular.ttf"
SANS_B = f"{FDIR}/noto/NotoSans-Bold.ttf"
SANS_XB = f"{FDIR}/noto/NotoSans-ExtraBold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading=None):
    """Draw wrapped paragraph; returns y after last line."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def bullets(draw, x, y, items, fnt, color, max_w, leading=None, mark="\u2022"):
    leading = leading or int(fnt.size * 1.35)
    for it in items:
        lines = wrap(draw, it, fnt, max_w - 18)
        for i, line in enumerate(lines):
            draw.text((x, y), mark if i == 0 else "", font=fnt, fill=RED)
            draw.text((x + 18, y), line, font=fnt, fill=color)
            y += leading
    return y


def stamp(draw, cx, cy, text, fnt, color, angle=-12, pad=10, lw=4):
    """Rotated bordered stamp label centred at (cx, cy)."""
    tw = int(draw.textlength(text, font=fnt))
    th = fnt.size
    layer = Image.new("RGBA", (tw + pad * 2 + 8, th + pad * 2 + 8), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([2, 2, tw + pad * 2 + 4, th + pad * 2 + 4],
                 outline=color + (255,), width=lw)
    ld.text((pad + 4, pad + 2), text, font=fnt, fill=color + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img = draw._image
    img.paste(layer, (int(cx) - layer.width // 2, int(cy) - layer.height // 2),
              layer)


def panel(draw, x, y, w, h, fill=WHITE, outline=INK, lw=2):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=lw)


def kicker(draw, x, y, text, color):
    f = font(SANS_XB, 15)
    draw.text((x, y), text, font=f, fill=color)
    return y + 21


def headline(draw, x, y, text, max_w, size=25, color=INK):
    f = font(SERIF_BLACK, size)
    return para(draw, x, y, text, f, color, max_w, leading=int(size * 1.08))


def place_ill(img, fn, x, y, w, h):
    """Render an illustration onto its own layer (clips spill) and paste it."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    fn(ld, 0, 0, w, h)
    img.paste(layer, (x, y), layer)


# ---------------------------------------------------------------- illustrations
def ill_cop31(d, x, y, w, h):
    """Antalya hall: cracked globe, empty desks, NO DEAL stamp."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 94, 82))
    d.ellipse([x + w * 0.30, y - h * 0.35, x + w * 0.95, y + h * 0.75],
              fill=(43, 122, 106))
    cx, cy, r = x + w * 0.52, y + h * 0.44, min(w, h) * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(66, 135, 190),
              outline=(246, 241, 231), width=3)
    for (lx, ly, lr) in [(0.42, 0.36, 0.16), (0.60, 0.55, 0.13),
                         (0.38, 0.58, 0.09), (0.66, 0.33, 0.07)]:
        d.ellipse([cx + (lx - 0.5) * 2 * r - lr * r, cy + (ly - 0.5) * 2 * r - lr * r,
                   cx + (lx - 0.5) * 2 * r + lr * r, cy + (ly - 0.5) * 2 * r + lr * r],
                  fill=(96, 160, 90))
    pts = [(cx - r * 0.55, cy - r * 0.85), (cx - r * 0.15, cy - r * 0.35),
           (cx - r * 0.45, cy - r * 0.05), (cx + r * 0.05, cy + r * 0.30),
           (cx - r * 0.20, cy + r * 0.62), (cx + r * 0.30, cy + r * 0.90)]
    d.line(pts, fill=(20, 32, 46), width=5, joint="curve")
    for i in range(5):
        dx = x + 12 + i * (w - 24) / 5
        dw = (w - 24) / 5 - 8
        d.rectangle([dx, y + h - 34, dx + dw, y + h - 12], fill=(20, 32, 46))
        d.rectangle([dx + dw * 0.5 - 2, y + h - 52, dx + dw * 0.5 + 2, y + h - 34],
                    fill=(246, 241, 231))
    for fx, col, sgn in [(x + 16, (30, 80, 160), 1), (x + w - 16, (200, 40, 40), -1)]:
        d.line([fx, y + 14, fx, y + 62], fill=(246, 241, 231), width=3)
        d.rectangle([min(fx, fx + 26 * sgn), y + 14,
                     max(fx, fx + 26 * sgn), y + 30], fill=col)
    stamp(d, cx, cy + r * 0.55, "NO DEAL", font(SANS_XB, 26), (255, 80, 66))


def ill_gulf(d, x, y, w, h):
    """Night over Riyadh: skyline, intercept bursts, tanker at sea."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    for (sx, sy) in [(0.08, 0.15), (0.22, 0.08), (0.38, 0.18), (0.55, 0.07),
                      (0.70, 0.16), (0.86, 0.09), (0.93, 0.22), (0.47, 0.26)]:
        d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5],
                  fill=(255, 253, 246))
    for (ax, ay, bx, by) in [(0.12, 0.62, 0.45, 0.30), (0.88, 0.66, 0.58, 0.34)]:
        pts = []
        for t in range(21):
            tt = t / 20
            px = x + (ax + (bx - ax) * tt) * w
            py = y + (ay + (by - ay) * tt - 0.18 * math.sin(tt * math.pi)) * h
            pts.append((px, py))
        d.line(pts, fill=(255, 190, 90), width=3)
        d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                  fill=(255, 220, 130))
    for (bx, by) in [(0.45, 0.30), (0.58, 0.34)]:
        cx, cy = x + bx * w, y + by * h
        for k in range(8):
            ang = k * math.pi / 4
            d.line([cx, cy, cx + 16 * math.cos(ang), cy + 16 * math.sin(ang)],
                   fill=(255, 160, 60), width=3)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 220, 130))
    base = y + h * 0.72
    for (bx, bw, bh) in [(0.02, 0.10, 0.22), (0.14, 0.08, 0.30), (0.24, 0.12, 0.18),
                         (0.62, 0.09, 0.26), (0.73, 0.11, 0.20), (0.86, 0.10, 0.32)]:
        d.rectangle([x + bx * w, base - bh * h, x + (bx + bw) * w, base],
                    fill=(8, 12, 26))
    d.rectangle([x + 0.44 * w, base - 0.52 * h, x + 0.52 * w, base], fill=(8, 12, 26))
    for wy in range(6):
        d.rectangle([x + 0.455 * w, base - 0.48 * h + wy * 0.07 * h,
                     x + 0.505 * w, base - 0.46 * h + wy * 0.07 * h],
                    fill=(255, 190, 90))
    d.rectangle([x, base, x + w, y + h], fill=(24, 52, 84))
    d.rectangle([x + 0.30 * w, y + h * 0.84, x + 0.72 * w, y + h * 0.93],
                fill=(10, 16, 30))
    for i in range(4):
        d.rectangle([x + (0.33 + i * 0.09) * w, y + h * 0.78,
                     x + (0.40 + i * 0.09) * w, y + h * 0.84],
                    fill=(180, 60, 40) if i % 2 else (60, 120, 90))
    d.polygon([(x + 0.74 * w, y + h * 0.84), (x + 0.78 * w, y + h * 0.70),
               (x + 0.82 * w, y + h * 0.84)], fill=(255, 140, 40))
    d.ellipse([x + 0.76 * w, y + h * 0.66, x + 0.80 * w, y + h * 0.72],
              fill=(255, 200, 90))


def ill_cricket(d, x, y, w, h):
    """Basin Reserve: green outfield, pitch, stumps, bat, ball, scoreboard."""
    d.rectangle([x, y, x + w, y + h], fill=(46, 110, 60))
    d.ellipse([x + w * 0.05, y + h * 0.10, x + w * 0.95, y + h * 0.95],
              fill=(64, 140, 78))
    d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.58, y + h * 0.92],
                fill=(198, 168, 118))
    for sx in (0.46, 0.49, 0.52):
        d.rectangle([x + sx * w, y + h * 0.24, x + sx * w + 3, y + h * 0.38],
                    fill=(240, 220, 150))
    # bat: rotated rectangle drawn directly, sized to the box
    bx, by = x + w * 0.74, y + h * 0.72
    ang = math.radians(32)
    ca, sa = math.cos(ang), math.sin(ang)
    bl, bw = h * 0.42, w * 0.075  # blade length / width
    hl = h * 0.20  # handle length
    def _rect(cx, cy, length, width, along):
        pts = []
        for s1, s2 in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            u = s1 * length / 2
            v = s2 * width / 2
            pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
        return pts
    d.polygon(_rect(bx, by, bl, bw, ang), fill=(232, 206, 150),
              outline=(150, 110, 60))
    hx = bx - (bl / 2 + hl / 2) * ca
    hy = by - (bl / 2 + hl / 2) * sa
    d.polygon(_rect(hx, hy, hl, bw * 0.45, ang), fill=(222, 196, 140))
    d.ellipse([x + w * 0.30, y + h * 0.66, x + w * 0.38, y + h * 0.74],
              fill=(178, 32, 28), outline=(255, 253, 246), width=2)
    d.rectangle([x + 6, y + 6, x + w * 0.62, y + 40], fill=(20, 32, 46))
    f = font(SANS_B, 13)
    d.text((x + 12, y + 9), "IND 720/9 dec", font=f, fill=(255, 220, 130))
    d.text((x + 12, y + 24), "NZ 157-4  day 5", font=f, fill=(255, 253, 246))


def ill_nepal(d, x, y, w, h):
    """Delhi + Himalayas: India Gate, snowy peaks, two flags."""
    d.rectangle([x, y, x + w, y + h], fill=(142, 178, 214))
    for (px, pw, ph) in [(0.0, 0.42, 0.55), (0.30, 0.46, 0.68), (0.62, 0.42, 0.58)]:
        d.polygon([(x + px * w, y + h * 0.78),
                   (x + (px + pw / 2) * w, y + h * (0.78 - ph)),
                   (x + (px + pw) * w, y + h * 0.78)], fill=(96, 116, 140))
        d.polygon([(x + (px + pw / 2 - 0.07) * w, y + h * (0.78 - ph)),
                   (x + (px + pw / 2) * w, y + h * (0.78 - ph)),
                   (x + (px + pw / 2 + 0.07) * w, y + h * (0.78 - ph + 0.10))],
                  fill=(255, 253, 246))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(120, 150, 90))
    gx, gw = x + w * 0.36, w * 0.28
    gy = y + h * 0.44
    d.rectangle([gx, gy, gx + gw, y + h * 0.80], fill=(176, 132, 84))
    d.pieslice([gx + gw * 0.18, gy + h * 0.10, gx + gw * 0.82, gy + h * 0.62],
               180, 360, fill=(142, 178, 214))
    d.rectangle([gx - 6, gy - 8, gx + gw + 6, gy], fill=(150, 110, 66))
    for fx, cols in [(x + w * 0.08, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (x + w * 0.84, [(220, 20, 60), (220, 20, 60)])]:
        d.line([fx, y + h * 0.30, fx, y + h * 0.80], fill=(60, 50, 40), width=3)
        if len(cols) == 3:
            for i, c in enumerate(cols):
                d.rectangle([fx, y + h * (0.30 + i * 0.055), fx + 34,
                             y + h * (0.355 + i * 0.055)], fill=c)
        else:
            d.polygon([(fx, y + h * 0.30), (fx + 30, y + h * 0.36),
                       (fx, y + h * 0.42)], fill=cols[0])
            d.polygon([(fx, y + h * 0.42), (fx + 26, y + h * 0.48),
                       (fx, y + h * 0.54)], fill=cols[1])


def ill_korea(d, x, y, w, h):
    """Exam hall: desk, CSAT paper, phone with lens, red arrow down."""
    d.rectangle([x, y, x + w, y + h], fill=(43, 76, 126))
    d.rectangle([x + w * 0.06, y + h * 0.62, x + w * 0.94, y + h * 0.70],
                fill=(120, 84, 52))
    d.rectangle([x + w * 0.10, y + h * 0.70, x + w * 0.16, y + h * 0.96],
                fill=(96, 66, 40))
    d.rectangle([x + w * 0.84, y + h * 0.70, x + w * 0.90, y + h * 0.96],
                fill=(96, 66, 40))
    px, py, pw, ph = x + w * 0.10, y + h * 0.14, w * 0.44, h * 0.50
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 253, 246),
                outline=(20, 32, 46), width=2)
    f = font(SANS_XB, 17)
    d.text((px + 10, py + 8), "CSAT", font=f, fill=(20, 32, 46))
    for i in range(4):
        ly = py + 36 + i * 14
        d.line([px + 10, ly, px + pw - 10, ly], fill=(150, 150, 145), width=2)
        d.ellipse([px + pw - 26, ly - 6, px + pw - 14, ly + 6],
                  outline=(46, 140, 70), width=2)
    d.line([px + pw - 23, ly - 2, px + pw - 19, ly + 3, px + pw - 12, ly - 6],
           fill=(46, 140, 70), width=2)
    qx, qy, qw, qh = x + w * 0.62, y + h * 0.20, w * 0.26, h * 0.44
    d.rounded_rectangle([qx, qy, qx + qw, qy + qh], radius=8, fill=(16, 20, 30),
                        outline=(200, 200, 195), width=2)
    d.ellipse([qx + qw * 0.28, qy + qh * 0.14, qx + qw * 0.72, qy + qh * 0.44],
              fill=(40, 60, 100), outline=(120, 180, 255), width=2)
    d.ellipse([qx + qw * 0.40, qy + qh * 0.24, qx + qw * 0.60, qy + qh * 0.36],
              fill=(10, 14, 24))
    ax = x + w * 0.90
    d.line([ax, y + h * 0.16, ax, y + h * 0.52], fill=(255, 80, 66), width=6)
    d.polygon([(ax - 10, y + h * 0.50), (ax + 10, y + h * 0.50),
               (ax, y + h * 0.62)], fill=(255, 80, 66))
    d.rectangle([x + w * 0.60, y + h * 0.66, x + w * 0.92, y + h * 0.70],
                fill=(240, 200, 60))


def ill_space(d, x, y, w, h):
    """Mercury orbit: cratered planet, probe, stars."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 22, 52))
    for (sx, sy) in [(0.06, 0.12), (0.18, 0.06), (0.30, 0.20), (0.55, 0.08),
                      (0.72, 0.18), (0.88, 0.07), (0.94, 0.30), (0.10, 0.42)]:
        d.ellipse([x + sx * w - 1.5, y + sy * h - 1.5, x + sx * w + 1.5, y + sy * h + 1.5],
                  fill=(255, 253, 246))
    d.ellipse([x - w * 0.10, y - h * 0.55, x + w * 0.75, y + h * 1.15],
              outline=(120, 120, 170), width=2)
    cx, cy, r = x + w * 0.34, y + h * 0.52, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 158, 148),
              outline=(220, 212, 200), width=2)
    for (ox, oy, orr) in [(0.30, 0.40, 0.10), (0.55, 0.62, 0.13), (0.68, 0.35, 0.08),
                          (0.42, 0.70, 0.07), (0.60, 0.48, 0.06)]:
        d.ellipse([cx + (ox - 0.5) * 2 * r - orr * r, cy + (oy - 0.5) * 2 * r - orr * r,
                   cx + (ox - 0.5) * 2 * r + orr * r, cy + (oy - 0.5) * 2 * r + orr * r],
                  fill=(130, 122, 112))
    px, py = x + w * 0.70, y + h * 0.30
    d.rectangle([px - 8, py - 6, px + 8, py + 6], fill=(220, 220, 210),
                outline=(20, 32, 46), width=1)
    d.rectangle([px - 46, py - 4, px - 10, py + 4], fill=(40, 80, 180))
    d.rectangle([px + 10, py - 4, px + 46, py + 4], fill=(40, 80, 180))
    d.polygon([(px - 5, py + 8), (px + 5, py + 8), (px, py + 26)],
              fill=(255, 160, 40))
    f = font(SANS_B, 11)
    d.text((x + 8, y + h - 18), "BepiColombo", font=f, fill=(255, 253, 246))


# ---------------------------------------------------------------- shared chrome
def masthead(d):
    d.rectangle([0, 0, W, H], fill=PAPER)
    d.line([28, 8, W - 28, 8], fill=INK, width=3)
    d.line([28, 14, W - 28, 14], fill=INK, width=1)
    f = font(SERIF_BLACK, 74)
    t = "THE WORLD"
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, 20), t, font=f, fill=INK)
    f2 = font(SANS_B, 15)
    d.text((28, 56), "WORLD NEWS", font=f2, fill=INK_SOFT)
    r = "ONE DAY  \u2022  ONE PICTURE"
    d.text((W - 28 - d.textlength(r, font=f2), 56), r, font=f2, fill=INK_SOFT)
    d.rectangle([28, 100, W - 28, 136], fill=INK)
    f3 = font(SANS_XB, 21)
    t3 = "MONDAY  \u2022  23 NOVEMBER 2026"
    d.text(((W - d.textlength(t3, font=f3)) / 2, 107), t3, font=f3,
           fill=(255, 253, 246))


def footer(d, y=956):
    f = font(SANS, 14)
    d.text((28, y), "Drawn from Monday's reporting: Reuters \u2022 AP \u2022 BBC \u2022 AFP \u2022 IANS",
           font=f, fill=GREY)
    r = "make.fun \u2014 news-image-20261123"
    d.text((W - 28 - d.textlength(r, font=f), y), r, font=f, fill=GREY)


def ticker(d, y, h):
    d.rectangle([28, y, W - 28, y + h], fill=INK)
    f = font(SANS_B, 15)
    lines = [
        "GAZA \u2014 9 killed in 48 hours; ceasefire toll 1,661  \u2022  "
        "UKRAINE \u2014 Drone flattens Kyiv-region block, 14 feared trapped",
        "LISBON \u2014 Thousands march over living costs  \u2022  "
        "SOUTH SUDAN \u2014 24 civilians killed in fresh violence",
    ]
    yy = y + 8
    for line in lines:
        d.text((44, yy), line, font=f, fill=(255, 253, 246))
        yy += 22


# ---------------------------------------------------------------- variant v1
def build_v1():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    # ---- lead: COP31 hero (y 148..428)
    x, y, w, h = 28, 148, 968, 280
    panel(d, x, y, w, h)
    place_ill(img, ill_cop31, x + 14, y + 14, 430, h - 28)
    tx, tw = x + 458, w - 458 - 18
    yy = y + 16
    yy = kicker(d, tx, yy, "CLIMATE \u2014 ANTALYA, TURKEY", RED)
    yy = headline(d, tx, yy, "COP31 COLLAPSES", tw, size=44)
    yy = para(d, tx, yy + 2, "No deal as the longest climate talks in history end in failure",
              font(SERIF_IT, 20), INK_SOFT, tw, leading=25)
    yy = bullets(d, tx, yy + 8, [
        "194 nations reject the \u201cAntalya Pact\u201d \u2014 it never even names fossil fuels",
        "EU: the talks were \u201chijacked by oil states\u201d",
        "UN chief Guterres: \u201cdeeply disappointed\u201d",
    ], font(SANS, 18), INK, tw, leading=24)
    d.text((tx, y + h - 24), "Talks fell apart on Sunday \u2014 leaders reacted on Monday.",
           font=font(SERIF_IT, 15), fill=GREY)
    # ---- row 2: three panels (y 440..684)
    ry, rh = 440, 244
    pw, gap = 314, 13
    cols = [
        ("GULF WAR \u2014 RIYADH", RED, "Missiles over Riyadh, tankers hit at Hormuz",
         "Saudi defences intercept Houthi missiles over the capital; two tankers hit off Oman within the hour. Oil prices tick up.",
         ill_gulf),
        ("SPORT \u2014 WELLINGTON", (46, 110, 60), "India six wickets from victory",
         "NZ 157\u20134 at lunch on day five, still 195 behind after India's record 720\u20139 \u2014 the biggest Test total ever in NZ.",
         ill_cricket),
        ("DIPLOMACY \u2014 NEW DELHI", (176, 122, 18), "Modi meets Nepal's Shah",
         "Talks in Delhi on his first trip abroad since taking office in March. Energy and flood aid on the agenda.",
         ill_nepal),
    ]
    for i, (kick, col, head, body, ill) in enumerate(cols):
        px = 28 + i * (pw + gap)
        panel(d, px, ry, pw, rh)
        place_ill(img, ill, px + 10, ry + 10, pw - 20, 96)
        yy = ry + 114
        yy = kicker(d, px + 12, yy, kick, col)
        yy = headline(d, px + 12, yy, head, pw - 24, size=21)
        para(d, px + 12, yy + 2, body, font(SANS, 14), INK_SOFT, pw - 24,
             leading=17)
    # ---- row 3: two wide panels (y 696..892)
    ry, rh = 696, 196
    pw2 = 477
    for i, (kick, col, head, body, ill) in enumerate([
        ("ASIA \u2014 SEOUL", (43, 76, 126), "Minister quits over AI exam-cheating row",
         "Choi Kyo-jin resigns after last-minute anti-cheating rules sow confusion at the CSAT exam. Lee accepts within the hour.",
         ill_korea),
        ("SPACE \u2014 MERCURY", (61, 58, 110), "BepiColombo reaches Mercury \u2014 with a glitch",
         "The ESA\u2013JAXA probe slips into orbit after an eight-year journey \u2014 only the second mission ever to orbit Mercury. Its thruster burn ran short.",
         ill_space),
    ]):
        px = 28 + i * (pw2 + 14)
        panel(d, px, ry, pw2, rh)
        place_ill(img, ill, px + 12, ry + 12, 160, rh - 24)
        tx = px + 184
        tw = pw2 - 196
        yy = ry + 14
        yy = kicker(d, tx, yy, kick, col)
        yy = headline(d, tx, yy, head, tw, size=22)
        para(d, tx, yy + 2, body, font(SANS, 15), INK_SOFT, tw, leading=19)
    ticker(d, 904, 52)
    footer(d)
    return img


# ---------------------------------------------------------------- variant v2
def build_v2():
    """Split hero: COP31 and Gulf side by side, then a 2x2 grid."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    y, h = 148, 244
    hw = 477
    panel(d, 28, y, hw, h)
    place_ill(img, ill_cop31, 28 + 10, y + 10, 180, h - 20)
    tx, tw = 28 + 202, hw - 214
    yy = y + 14
    yy = kicker(d, tx, yy, "CLIMATE \u2014 ANTALYA", RED)
    yy = headline(d, tx, yy, "COP31 COLLAPSES", tw, size=32)
    para(d, tx, yy + 2, "No deal as the longest climate talks ever end in failure. 194 nations reject a pact that never names fossil fuels; the EU says talks were \u201chijacked by oil states\u201d.",
         font(SANS, 15), INK_SOFT, tw, leading=19)
    d.text((tx, y + h - 22), "Talks fell apart on Sunday.",
           font=font(SERIF_IT, 13), fill=GREY)
    panel(d, 519, y, hw, h)
    place_ill(img, ill_gulf, 519 + 10, y + 10, 180, h - 20)
    tx = 519 + 202
    yy = y + 14
    yy = kicker(d, tx, yy, "GULF WAR \u2014 RIYADH", RED)
    yy = headline(d, tx, yy, "Missiles over Riyadh, tankers hit at Hormuz", tw, size=28)
    para(d, tx, yy + 2, "Saudi defences intercept Houthi missiles over the capital; two tankers hit off Oman within the hour. Oil prices tick up.",
         font(SANS, 15), INK_SOFT, tw, leading=19)
    gy, gh = 404, 236
    gw = 477
    cells = [
        ("SPORT \u2014 WELLINGTON", (46, 110, 60), "India six wickets from victory",
         "NZ 157\u20134 at lunch on day five, still 195 behind after India's record 720\u20139 \u2014 the biggest Test total ever in NZ.",
         ill_cricket),
        ("DIPLOMACY \u2014 NEW DELHI", (176, 122, 18), "Modi meets Nepal's Shah",
         "Talks in Delhi on his first trip abroad since taking office in March. Energy and flood aid on the agenda.",
         ill_nepal),
        ("ASIA \u2014 SEOUL", (43, 76, 126), "Minister quits over AI exam-cheating row",
         "Choi Kyo-jin resigns after last-minute anti-cheating rules sow confusion at the CSAT exam. Lee accepts within the hour.",
         ill_korea),
        ("SPACE \u2014 MERCURY", (61, 58, 110), "BepiColombo reaches Mercury \u2014 with a glitch",
         "The ESA\u2013JAXA probe slips into orbit after an eight-year journey \u2014 only the second mission ever to orbit Mercury. Its thruster burn ran short.",
         ill_space),
    ]
    for i, (kick, col, head, body, ill) in enumerate(cells):
        px = 28 + (i % 2) * (gw + 14)
        py = gy + (i // 2) * (gh + 12)
        panel(d, px, py, gw, gh)
        place_ill(img, ill, px + 12, py + 12, 160, gh - 24)
        tx = px + 184
        tw = gw - 196
        yy = py + 14
        yy = kicker(d, tx, yy, kick, col)
        yy = headline(d, tx, yy, head, tw, size=22)
        para(d, tx, yy + 2, body, font(SANS, 15), INK_SOFT, tw, leading=19)
    ticker(d, 904, 52)
    footer(d)
    return img


# ---------------------------------------------------------------- variant v3
def build_v3():
    """Mosaic: six equal panels under a big date banner, no single lead."""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    d.rectangle([28, 148, W - 28, 190], fill=RED)
    f = font(SANS_XB, 23)
    t = "SIX STORIES THAT MADE MONDAY  \u2014  23 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 160), t, font=f, fill=WHITE)
    cells = [
        ("CLIMATE \u2014 ANTALYA", RED, "COP31 collapses: no deal",
         "The longest climate talks ever end in failure. 194 nations reject a pact that never names fossil fuels; the EU says talks were \u201chijacked by oil states\u201d.",
         ill_cop31),
        ("GULF WAR \u2014 RIYADH", (180, 85, 31), "Missiles over Riyadh, tankers hit at Hormuz",
         "Saudi defences intercept Houthi missiles over the capital; two tankers hit off Oman within the hour.",
         ill_gulf),
        ("SPORT \u2014 WELLINGTON", (46, 110, 60), "India six wickets from victory",
         "NZ 157\u20134 at lunch on day five, still 195 behind after India's record 720\u20139 \u2014 the biggest Test total ever in NZ.",
         ill_cricket),
        ("DIPLOMACY \u2014 NEW DELHI", (176, 122, 18), "Modi meets Nepal's Shah",
         "Talks in Delhi on his first trip abroad since taking office in March. Energy and flood aid on the agenda.",
         ill_nepal),
        ("ASIA \u2014 SEOUL", (43, 76, 126), "Minister quits over AI exam-cheating row",
         "Choi Kyo-jin resigns after last-minute anti-cheating rules sow confusion at the CSAT exam. Lee accepts within the hour.",
         ill_korea),
        ("SPACE \u2014 MERCURY", (61, 58, 110), "BepiColombo reaches Mercury \u2014 with a glitch",
         "The ESA\u2013JAXA probe slips into orbit after an eight-year journey \u2014 only the second mission ever to orbit Mercury.",
         ill_space),
    ]
    gy, gh = 202, 336
    gw, gap = 314, 13
    for i, (kick, col, head, body, ill) in enumerate(cells):
        px = 28 + (i % 3) * (gw + gap)
        py = gy + (i // 3) * (gh + 12)
        panel(d, px, py, gw, gh)
        place_ill(img, ill, px + 10, py + 10, gw - 20, 150)
        yy = py + 168
        yy = kicker(d, px + 12, yy, kick, col)
        yy = headline(d, px + 12, yy, head, gw - 24, size=21)
        para(d, px + 12, yy + 2, body, font(SANS, 15), INK_SOFT, gw - 24,
             leading=19)
    ticker(d, 904, 52)
    footer(d)
    return img


BUILDERS = {"v1": build_v1, "v2": build_v2, "v3": build_v3}

if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "v1"
    out = sys.argv[2] if len(sys.argv) > 2 else "entry.png"
    BUILDERS[variant]().save(out, optimize=True)
    print(f"wrote {out} ({variant})")
