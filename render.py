#!/usr/bin/env python3
"""Render the news-image-20261117 round-2 entry poster (1024x1024).

Draws a newspaper front page summing up Tuesday 17 November 2026:
masthead + date, lead story (Kerch Bridge) with a hand-drawn bridge
graphic, three illustrated panels, six region boxes with ~40 verified
headlines, and an "Also today" strip. Deterministic: no network, no
clock, no randomness. Requires Pillow only for the local render step;
the submitted main.py copies the finished entry.png instead.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 0, 0)
DARKRED = (120, 0, 0)
GREY = (90, 86, 78)
LINE = (40, 40, 40)
BLUE = (24, 68, 120)
TEAL = (0, 110, 105)
ORANGE = (214, 110, 0)
GOLD = (176, 132, 0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w, max_lines=2):
    """Greedy word wrap; truncate with ellipsis past max_lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines:
        # check if text was cut
        joined = " ".join(lines)
        if len(joined) < len(text):
            while lines and draw.textlength(lines[-1] + " ...", font=font) > max_w:
                lines[-1] = lines[-1][:-1]
            lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def draw_bridge(d, x0, y0, x1, y1):
    """Stylised Kerch Bridge: sea, deck, towers, collapsed arch, blast."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 240))
    # sky band
    d.rectangle([x0, y0, x1, y0 + 26], fill=(190, 214, 228))
    # sun
    d.ellipse([x1 - 52, y0 + 8, x1 - 26, y0 + 34], fill=(240, 196, 90))
    # sea
    d.rectangle([x0, y1 - 46, x1, y1], fill=(52, 110, 150))
    for yy in range(y1 - 42, y1 - 4, 10):
        d.line([(x0 + 8, yy), (x1 - 8, yy)], fill=(120, 170, 205), width=2)
    mid_y = y0 + 96
    # left deck (intact)
    d.rectangle([x0, mid_y, x0 + 150, mid_y + 10], fill=(60, 60, 60))
    # right deck (intact)
    d.rectangle([x1 - 150, mid_y, x1, mid_y + 10], fill=(60, 60, 60))
    # collapsed span: thick tilted deck segment falling into the sea
    d.polygon([(x0 + 146, mid_y - 2), (x0 + 160, mid_y + 10),
               (x0 + 234, y1 - 28), (x0 + 222, y1 - 38)], fill=(80, 80, 80))
    # splash where the span hits the water
    for sx in (x0 + 224, x0 + 238, x0 + 252):
        d.arc([sx - 10, y1 - 44, sx + 10, y1 - 24], 180, 360,
              fill=(255, 255, 255), width=2)
    # debris
    d.rectangle([x0 + 258, y1 - 40, x0 + 266, y1 - 34], fill=(90, 90, 90))
    # towers
    for tx in (x0 + 40, x1 - 60):
        d.rectangle([tx, mid_y - 62, tx + 8, mid_y], fill=(60, 60, 60))
        d.line([(tx + 4, mid_y - 62), (x0 + 10, mid_y)], fill=(120, 120, 120), width=1)
        d.line([(tx + 4, mid_y - 62), (x1 - 10, mid_y)], fill=(120, 120, 120), width=1)
    # broken arch stubs
    d.arc([x0 + 120, mid_y - 44, x0 + 190, mid_y + 6], 180, 270, fill=(60, 60, 60), width=5)
    d.arc([x1 - 190, mid_y - 44, x1 - 120, mid_y + 6], 270, 360, fill=(60, 60, 60), width=5)
    # explosion starburst at the break
    cx, cy = x0 + 195, mid_y - 6
    for r, col in ((34, (255, 190, 60)), (24, (255, 120, 20)), (13, (200, 40, 10))):
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    # caption
    d.text((x0 + 4, y1 - 18), "The Kerch Bridge after the overnight strike",
           font=f(SANS, 11), fill=(255, 255, 255))


def draw_drone(d, cx, cy, s):
    """Simple quadcopter silhouette."""
    body = (40, 40, 40)
    d.ellipse([cx - 16 * s, cy - 7 * s, cx + 16 * s, cy + 7 * s], fill=body)
    for dx, dy in ((-26, -14), (26, -14), (-26, 14), (26, 14)):
        d.line([(cx, cy), (cx + dx * s, cy + dy * s)], fill=body, width=3)
        d.ellipse([cx + dx * s - 12 * s, cy + dy * s - 3 * s,
                   cx + dx * s + 12 * s, cy + dy * s + 3 * s], fill=(90, 90, 90))
    d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=RED)


def draw_jet(d, cx, cy, s):
    """Simple fighter-jet silhouette, side view."""
    body = (40, 40, 40)
    pts = [(cx - 52 * s, cy), (cx - 30 * s, cy - 7 * s), (cx + 18 * s, cy - 6 * s),
           (cx + 52 * s, cy - 2 * s), (cx + 52 * s, cy + 2 * s), (cx + 18 * s, cy + 6 * s),
           (cx - 30 * s, cy + 7 * s)]
    d.polygon(pts, fill=body)
    d.polygon([(cx - 6 * s, cy - 6 * s), (cx + 8 * s, cy - 26 * s),
               (cx + 16 * s, cy - 6 * s)], fill=body)
    d.polygon([(cx - 20 * s, cy + 6 * s), (cx - 8 * s, cy + 22 * s),
               (cx + 2 * s, cy + 6 * s)], fill=body)
    # cockpit canopy
    d.ellipse([cx + 22 * s, cy - 7 * s, cx + 38 * s, cy - 1 * s], fill=(150, 200, 230))
    # exhaust flame behind the tail
    d.polygon([(cx - 52 * s, cy - 2 * s), (cx - 66 * s, cy - 9 * s),
               (cx - 66 * s, cy + 9 * s), (cx - 52 * s, cy + 2 * s)], fill=(220, 90, 20))


def draw_chip(d, cx, cy, s):
    """Simple microchip."""
    d.rectangle([cx - 26 * s, cy - 26 * s, cx + 26 * s, cy + 26 * s],
                fill=(30, 30, 46), outline=(150, 150, 170), width=2)
    d.rectangle([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s],
                fill=(60, 180, 120))
    for i in range(-2, 3):
        off = i * 11 * s
        d.line([(cx + off, cy - 26 * s), (cx + off, cy - 36 * s)], fill=(150, 150, 170), width=3)
        d.line([(cx + off, cy + 26 * s), (cx + off, cy + 36 * s)], fill=(150, 150, 170), width=3)
        d.line([(cx - 26 * s, cy + off), (cx - 36 * s, cy + off)], fill=(150, 150, 170), width=3)
        d.line([(cx + 26 * s, cy + off), (cx + 36 * s, cy + off)], fill=(150, 150, 170), width=3)


def region_box(d, x, y, w, h, title, color, items, accent):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 26], fill=color)
    d.text((x + 8, y + 5), title, font=f(SANS_B, 14), fill=(255, 255, 255))
    yy = y + 34
    body = f(SANS, 12)
    for it in items:
        d.rectangle([x + 8, yy + 4, x + 14, yy + 10], fill=accent)
        lines = wrap(d, it, body, w - 26, max_lines=2)
        for ln in lines:
            d.text((x + 19, yy), ln, font=body, fill=INK)
            yy += 15
        yy += 4
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 10], fill=DARKRED)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=f(SERIF_B, 58),
           fill=INK, anchor="ma")
    d.line([(24, 84), (W - 24, 84)], fill=RED, width=3)
    d.text((W // 2, 90), "TUESDAY, 17 NOVEMBER 2026", font=f(SERIF_B, 28),
           fill=RED, anchor="ma")
    d.text((24, 92), "40 STORIES", font=f(SANS_B, 13), fill=GREY)
    d.text((W - 24, 92), "6 CONTINENTS", font=f(SANS_B, 13), fill=GREY, anchor="ra")
    d.line([(24, 124), (W - 24, 124)], fill=LINE, width=2)

    # ---------- Lead story ----------
    ly = 134
    d.text((24, ly), "UKRAINE DROPS PUTIN'S KERCH BRIDGE",
           font=f(SERIF_B, 33), fill=INK)
    d.text((24, ly + 50), "Drones and missiles collapse a 270-metre road arch of the",
           font=f(SANS, 15), fill=INK)
    d.text((24, ly + 70), "Crimea link in a seven-stage operation; rail traffic",
           font=f(SANS, 15), fill=INK)
    d.text((24, ly + 90), "resumes by afternoon as Moscow vows to rebuild.",
           font=f(SANS, 15), fill=INK)
    d.text((24, ly + 116), "Russia answers with its biggest drone raid of the war —",
           font=f(SANS, 15), fill=INK)
    d.text((24, ly + 136), "1,441 shot down, Kyiv says — and strikes Kyiv bridges.",
           font=f(SANS, 15), fill=INK)
    d.rectangle([24, ly + 160, 120, ly + 182], fill=RED)
    d.text((72, ly + 164), "LEAD STORY", font=f(SANS_B, 12),
           fill=(255, 255, 255), anchor="ma")
    draw_bridge(d, 600, ly + 48, 1000, ly + 182)

    d.line([(24, 330), (W - 24, 330)], fill=LINE, width=1)

    # ---------- Three illustrated panels ----------
    py = 340
    pw, gap = 320, 8
    panels = [
        ("IRAN'S DRONES TARGET US RADAR IN BAHRAIN",
         "Third strike in days on US targets in the Gulf; Bahrain says the "
         "drones were intercepted, no damage. Carrier USS Theodore Roosevelt arrives.",
         "drone", TEAL),
        ("JAPAN SCRAMBLES JETS AS RUSSIAN PLANES BREACH ITS AIRSPACE",
         "Two suspected Russian aircraft enter airspace near Okinoshima for three "
         "minutes each; Seoul and Taipei also send up jets.",
         "jet", BLUE),
        ("NVIDIA BEATS FORECASTS WITHOUT HUANG",
         "$115.8bn revenue, up 103%, in its first report since the CEO quit; "
         "the board says it will not reinstate him.",
         "chip", GOLD),
    ]
    for i, (head, body_text, icon, accent) in enumerate(panels):
        x = 24 + i * (pw + gap)
        d.rectangle([x, py, x + pw, py + 168], outline=LINE, width=1)
        d.rectangle([x, py, x + pw, py + 5], fill=accent)
        if icon == "drone":
            draw_drone(d, x + 52, py + 40, 1.0)
        elif icon == "jet":
            draw_jet(d, x + 56, py + 40, 0.85)
        else:
            draw_chip(d, x + 52, py + 42, 1.0)
        hl = wrap(d, head, f(SANS_B, 14), pw - 112, max_lines=3)
        yy = py + 12
        for ln in hl:
            d.text((x + 108, yy), ln, font=f(SANS_B, 14), fill=INK)
            yy += 17
        bl = wrap(d, body_text, f(SANS, 12), pw - 20, max_lines=4)
        yy = py + 82
        for ln in bl:
            d.text((x + 10, yy), ln, font=f(SANS, 12), fill=INK)
            yy += 15

    d.line([(24, 522), (W - 24, 522)], fill=LINE, width=1)

    # ---------- Region grid ----------
    gy = 532
    bw, bh = 320, 208
    regions = [
        ("EUROPE", DARKRED, RED, [
            "Russia hits Kyiv bridges in overnight strikes",
            "UK sanctions 8 Israeli settlement firms, Gaza aid blockers",
            "France strike: 146,000 march; turnout sharply down",
            "Knesset elects Kahana speaker in blow to Netanyahu",
            "Iran-linked assassination plot foiled in Greece; 5 held",
            "Deutsche Bank leak: 15m files, 230 journalists",
        ]),
        ("MIDDLE EAST", (110, 60, 0), ORANGE, [
            "US and Iran edge closer to renewed all-out war",
            "Jordan bans Telegram over national security",
            "Houthis assert grip on Bab al-Mandab Strait",
            "West urges Israel to open Gaza aid crossings",
            "Iran-Oman talks on Hormuz shipping corridors",
        ]),
        ("ASIA-PACIFIC", BLUE, (60, 130, 200), [
            "Trump lands in Manila for ASEAN finale; chair to Singapore",
            "Quad leaders meet in Manila, first since 2024",
            "APEC opens in Shenzhen; Trump-Xi-Putin summit Thursday",
            "US widens AI chip curbs to SE Asia and Brazil",
            "Myanmar air strike kills 12 at Rakhine camp",
            "Hong Kong tops Dubai in super-luxury housing",
        ]),
        ("AMERICAS", TEAL, (0, 150, 140), [
            "Senate bill would strip China's trade status",
            "Argentina crush Costa Rica 7-0; Scaloni signs to 2030",
            "Costa Rican reporter killed after probing drug gangs",
            "Cuba says it is braced for possible US attack",
            "Pope Leo XIV presses justice for Amazon defenders in Peru",
            "Tech sell-off deepens; chip index down 5% Monday",
        ]),
        ("AFRICA", (90, 70, 20), (150, 110, 30), [
            "DR Congo Ebola 'out of control': 5,500 dead",
            "17 killed in two mass shootings in South Africa",
            "Guinea mining crackdown: 1,263 arrested, 10 killed",
            "South Sudan delays first elections to February",
            "Ethiopia accuses Eritrea of backing Tigray rebels",
            "Five EU states plan Rwanda return hub for 2027",
        ]),
        ("OCEANIA & SPACE", (70, 60, 110), (130, 110, 190), [
            "Locusts swarm South Australia's pastoral land",
            "Rocket failure destroys Amazon satellite payload",
            "Anthropic plans mega IPO as AI race heats up",
        ]),
    ]
    for i, (title, color, accent, items) in enumerate(regions):
        x = 24 + (i % 3) * (bw + gap)
        y = gy + (i // 3) * (bh + gap)
        region_box(d, x, y, bw, bh, title, color, items, accent)

    # ---------- Also today strip ----------
    ay = 964
    d.rectangle([24, ay, W - 24, ay + 34], fill=(232, 226, 212))
    d.text((32, ay + 8), "ALSO TODAY:", font=f(SANS_B, 12), fill=RED)
    also = ("Depardieu drops appeal; conviction final  •  UN court to rule Thursday "
            "on Myanmar genocide  •  Colombia's hottest November day: 37.8°C")
    d.text((140, ay + 8), also, font=f(SANS, 12), fill=INK)

    d.text((24, 1006), "All events reported Tuesday 17 November 2026  •  Sources: Reuters, AP, BBC, NPR, Le Monde",
           font=f(SANS, 11), fill=GREY)
    d.text((W - 24, 1006), "40 stories", font=f(SANS_B, 11), fill=GREY, anchor="ra")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
