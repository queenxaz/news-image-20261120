#!/usr/bin/env python3
"""Render THE WORLD TODAY, Friday 20 November 2026, as a 1024x1024 front page.

Draws the whole page programmatically with Pillow: masthead, lead story,
markets ticker, a three-column grid of twelve stories, a compact list of
seven more, and a small schematic world map of the day's hot spots.
Deterministic: no randomness, no timestamps, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (12, 12, 12)
RED = (178, 24, 24)
GREY = (110, 110, 105)
LIGHT = (238, 236, 228)
RULE = (60, 60, 60)
MAP_LAND = (206, 202, 188)
MAP_LINE = (120, 116, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis when clipped."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " ..."
    return lines


def one_line(draw, head, text, head_fnt, text_fnt, max_w):
    """Truncate text so bold head + ' — ' + text fits max_w pixels."""
    prefix = head + " — "
    head_w = draw.textlength(prefix, font=head_fnt)
    clipped = False
    while text and head_w + draw.textlength(text, font=text_fnt) > max_w:
        text = text.rsplit(" ", 1)[0].rstrip(",")
        clipped = True
    if clipped:
        text += " ..."
    return prefix, text


def block(draw, x, y, w, kicker, head, summary, head_size=18, sum_size=14,
          head_lines=2, sum_lines=2):
    """One grid story: red kicker, bold headline, short summary."""
    draw.text((x, y), kicker, font=SANS_B(11), fill=RED)
    y += 16
    hf = SANS_B(head_size)
    for ln in fit_lines(draw, head, hf, w, head_lines):
        draw.text((x, y), ln, font=hf, fill=INK)
        y += head_size + 4
    y += 2
    sf = SANS(sum_size)
    for ln in fit_lines(draw, summary, sf, w, sum_lines):
        draw.text((x, y), ln, font=sf, fill=(40, 40, 40))
        y += sum_size + 4
    return y


# ---------------------------------------------------------------- stories
LEAD_HEAD = ["AI FEARS SEND ASIAN", "MARKETS PLUNGING"]
LEAD_DECK = ("Japan's Nikkei fell 4.8% and SoftBank plunged 16% as Anthropic's "
             "record Nasdaq debut failed to calm fears that the AI boom is built "
             "on debt. Wall Street fell for a fifth straight day.")
LEAD_FALLS = [("Nikkei 225", -4.8), ("KOSPI", -5.7), ("Taiex", -6.8),
              ("SoftBank", -16.0)]

GRID = [
    ("THE HAGUE", "World court: Myanmar committed genocide",
     "ICJ rules 9-6 in the Rohingya case, the first genocide finding against a state."),
    ("SHENZHEN", "Trump, Xi and Putin hold first three-way summit",
     "Leaders sign a four-point declaration; Ukraine and Iran go unmentioned."),
    ("NEW YORK", "Anthropic closes 17% up in record debut",
     "Claude maker raises $81.3bn, the largest IPO ever, but tech shares still fall."),
    ("RIYADH", "Houthi missile damages Riyadh's PIF Tower",
     "Windows blown out across seven floors of the wealth fund HQ; no injuries."),
    ("ANTALYA", "COP31 draft drops fossil-fuel phase-out",
     "Slimmed-down text erases the phase-out call and net-zero dates on the final day."),
    ("CULTURE", "GTA 6 launch tops $2.36bn in sales",
     "Sensor Tower counts 24.6m copies on day one, the biggest entertainment launch ever."),
    ("BERLIN", "UK pledges 1,000+ drones for Ukraine",
     "A £260m package of long-range strike drones is unveiled at allied talks."),
    ("KYIV", "Ukraine hits Crimea Bridge a third time",
     "Rail traffic halts; Putin vows a painful reply as fresh missiles hit Kyiv."),
    ("WASHINGTON", "Senate rejects Iran war-powers bid",
     "Vote fails 48-51 as Hormuz tanker attacks grow; Pentagon puts the war at $48.3bn."),
    ("CALIFORNIA", "California subpoenas Nvidia over China chips",
     "Probe follows CEO Huang's exit; House says 879,000 AI chips reached Chinese firms."),
    ("WASHINGTON", "Trump pardons late baseball star Pete Rose",
     "Posthumous pardon for the hits leader's 1990 tax convictions; Hall vote due 2027."),
    ("WASHINGTON", "US sanctions Comancheros and 'Ndrangheta",
     "Treasury targets the biker gang and the mafia's Toronto arm for aiding cartels."),
]

ALSO = [
    ("Bukele files for a third term",
     "El Salvador's president registers for February's vote."),
    ("Boat sinks off Senegal",
     "Four dead, dozens missing off Yenne."),
    ("Cyber chief fired",
     "White House ousts Sean Cairncross after a week of outages."),
    ("Florida's 20th execution",
     "State sets a yearly record; Texas executes Dennes, 70."),
    ("Haiti raid kills 34",
     "Police say 34 gang suspects died in the Martissant operation."),
    ("Poland probes mystery objects",
     "Army checks two airspace violations; alert lifted."),
    ("Voyager 1, one light-day out",
     "NASA probe passes 26bn km, 49 years after launch."),
]

# Rough continent outlines as (lon, lat) polygons, for the schematic map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-70, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20),
     (-77, -12), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (25, 71), (18, 69),
     (12, 65), (5, 60), (-5, 50)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (32, -29), (25, -34), (18, -35), (12, -18), (8, -2), (9, 4),
     (-8, 5), (-13, 9)],
    [(30, 70), (40, 68), (60, 69), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (162, 60), (158, 52),
     (142, 50), (140, 40), (130, 33), (127, 35), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (80, 20), (75, 10),
     (70, 20), (60, 25), (55, 26), (48, 30), (43, 28), (35, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
]
HOTSPOTS = [  # (lon, lat)
    (139.7, 35.7), (46.7, 24.7), (30.7, 36.9), (114.1, 22.5), (30.5, 50.5),
    (21.0, 52.2), (-72.3, 18.5), (-89.2, 13.7), (-17.4, 14.7), (4.3, 52.1),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26  # page margin

    # ---------------------------------------------------------------- masthead
    title = "THE WORLD TODAY"
    tf = SERIF_B(82)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title, font=tf, fill=INK)
    d.line([(mx, 112), (W - mx, 112)], fill=INK, width=3)
    d.line([(mx, 117), (W - mx, 117)], fill=INK, width=1)
    d.text((mx, 126), "FRIDAY 20 NOVEMBER 2026", font=SANS_B(19), fill=INK)
    right = "ONE PAGE  ·  20 STORIES"
    d.text((W - mx - d.textlength(right, font=SANS_B(14)), 130), right,
           font=SANS_B(14), fill=GREY)
    d.line([(mx, 152), (W - mx, 152)], fill=RULE, width=1)

    # ---------------------------------------------------------------- lead story
    d.text((mx, 162), "MARKETS — TOKYO · SEOUL · TAIPEI", font=SANS_B(14), fill=RED)
    hf = SERIF_B(45)
    y = 184
    for ln in LEAD_HEAD:
        d.text((mx, y), ln, font=hf, fill=INK)
        y += 50
    sf = SANS(16)
    y = 288
    for ln in fit_lines(d, LEAD_DECK, sf, 648, 3):
        d.text((mx, y), ln, font=sf, fill=(40, 40, 40))
        y += 20

    # Lead chart: the day's falls, right of the lead text.
    cx0, cy0, cx1, cy1 = 700, 162, W - mx, 348
    d.rectangle([cx0, cy0, cx1, cy1], fill=LIGHT, outline=RULE, width=1)
    d.text((cx0 + 14, cy0 + 10), "THE FALL, IN A DAY", font=SANS_B(13), fill=INK)
    by = cy0 + 44
    for name, val in LEAD_FALLS:
        d.text((cx0 + 14, by), name, font=SANS(14), fill=INK)
        bar_x = cx0 + 118
        bar_w = int(abs(val) / 16.0 * 118)
        d.rectangle([bar_x, by + 2, bar_x + bar_w, by + 14], fill=RED)
        d.text((bar_x + bar_w + 6, by), f"{val}%", font=SANS_B(14), fill=RED)
        by += 32

    # ---------------------------------------------------------------- markets ticker
    d.rectangle([mx, 360, W - mx, 390], fill=INK)
    tick = ("MARKETS   Nikkei -4.8%  ·  KOSPI -5.7%  ·  Taiex -6.8%  ·  "
            "S&P 500 -2.0%  ·  Nasdaq -2.3%  ·  Gold -4.2%  ·  Brent $90.05")
    tick_size = 15
    while tick_size > 11 and d.textlength(tick, font=SANS_B(tick_size)) > 950:
        tick_size -= 1
    tf2 = SANS_B(tick_size)
    d.text(((W - d.textlength(tick, font=tf2)) / 2, 368), tick, font=tf2,
           fill=(255, 255, 255))

    # ---------------------------------------------------------------- story grid
    cols = [(mx, 322), (356, 322), (686, 286)]
    rows_y = [400, 496, 592, 688]
    for i, (kicker, head, summary) in enumerate(GRID):
        cx, cw = cols[i % 3]
        cy = rows_y[i // 3]
        block(d, cx, cy, cw, kicker, head, summary)
        if i % 3 < 2:
            d.line([(cx + cw + 8, cy + 2), (cx + cw + 8, cy + 88)],
                   fill=(200, 198, 188), width=1)
    d.line([(mx, 788), (W - mx, 788)], fill=RULE, width=1)

    # ---------------------------------------------------------------- also today
    d.text((mx, 800), "ALSO TODAY", font=SANS_B(14), fill=RED)
    y = 824
    for head, text in ALSO:
        prefix, clipped = one_line(d, head, text, SANS_B(15), SANS(15), 660)
        d.text((mx, y), prefix, font=SANS_B(15), fill=INK)
        hw = d.textlength(prefix, font=SANS_B(15))
        d.text((mx + hw, y), clipped, font=SANS(15), fill=(40, 40, 40))
        y += 22

    # ---------------------------------------------------------------- world map
    px0, py0, px1, py1 = 700, 800, W - mx, 978
    d.rectangle([px0, py0, px1, py1], fill=LIGHT, outline=RULE, width=1)
    d.text((px0 + 12, py0 + 8), "THE DAY IN PLACES", font=SANS_B(13), fill=INK)
    map_x0, map_y0 = px0 + 8, py0 + 30
    map_w, map_h = px1 - px0 - 16, 108

    def project(lon, lat):
        return (map_x0 + (lon + 180.0) / 360.0 * map_w,
                map_y0 + (90.0 - lat) / 180.0 * map_h)

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
    for lon, lat in HOTSPOTS:
        x, yy = project(lon, lat)
        d.ellipse([x - 4, yy - 4, x + 4, yy + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
    legend = ("Tokyo · Riyadh · Antalya · Shenzhen · Kyiv · Warsaw · "
              "Dakar · Haiti · San Salvador · The Hague")
    ly = py1 - 36
    for ln in fit_lines(d, legend, SANS(11), px1 - px0 - 20, 2):
        d.text((px0 + 10, ly), ln, font=SANS(11), fill=GREY)
        ly += 14

    # ---------------------------------------------------------------- footer
    d.line([(mx, 992), (W - mx, 992)], fill=RULE, width=1)
    foot = ("THE WORLD TODAY  ·  FRIDAY 20 NOVEMBER 2026  ·  Stories first "
            "reported on 20 November 2026")
    ff = SANS(12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1000), foot, font=ff, fill=GREY)
    return img


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    img = render()
    img.save("entry.jpg", "JPEG", quality=88)
    print("wrote entry.jpg", img.size)


if __name__ == "__main__":
    main()
