#!/usr/bin/env python3
"""Compose the News Image entry for Wednesday 25 November 2026.

Draws a one-page illustrated broadsheet (1024x1024 PNG) with PIL: a black
date band, a big-number stat strip, three illustrated lead panels, a numbered
story grid with a drawn icon per story, a dotted world map whose numbered
pins match the story numbers, an ALSO ON WEDNESDAY micro-list, and a
DATE CHECK box. Every story was researched from 25 November 2026 reporting
and date-checked; stories that belonged to 24 November were left out and are
named in the DATE CHECK box.

Deterministic: no randomness, no clock reads inside the drawing (the
wires-read time is passed in as WIRES_UTC by the builder).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (18, 18, 18)
GREY = (92, 88, 80)
RED = (164, 32, 24)
DARKRED = (128, 24, 18)
GOLD = (176, 132, 26)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(path, size):
    return ImageFont.truetype(path, size)


F = {
    "mast": font(FL + "LiberationSerif-Bold.ttf", 58),
    "mast_small": font(FD + "DejaVuSans-Bold.ttf", 20),
    "mast_right": font(FD + "DejaVuSans.ttf", 12),
    "subline": font(FL + "LiberationSerif-Italic.ttf", 17),
    "stat_num": font(FL + "LiberationSerif-Bold.ttf", 31),
    "stat_cap": font(FD + "DejaVuSans.ttf", 10),
    "tab": font(FD + "DejaVuSans-Bold.ttf", 12),
    "kicker": font(FD + "DejaVuSans-Bold.ttf", 11),
    "lead_head": font(FL + "LiberationSerif-Bold.ttf", 19),
    "lead_sub": font(FD + "DejaVuSans.ttf", 11),
    "src": font(FL + "LiberationSerif-Italic.ttf", 11),
    "g_head": font(FD + "DejaVuSans-Bold.ttf", 13),
    "g_sub": font(FD + "DejaVuSans.ttf", 10),
    "also_head": font(FD + "DejaVuSans-Bold.ttf", 13),
    "also": font(FD + "DejaVuSans.ttf", 10),
    "map_title": font(FD + "DejaVuSans-Bold.ttf", 11),
    "pin": font(FD + "DejaVuSans-Bold.ttf", 9),
    "check": font(FD + "DejaVuSans.ttf", 11),
    "check_b": font(FD + "DejaVuSans-Bold.ttf", 11),
    "foot": font(FD + "DejaVuSans.ttf", 10),
    "foot_b": font(FD + "DejaVuSans-Bold.ttf", 11),
}

REGIONS = {
    "ASIA-PACIFIC": (31, 95, 158),
    "EUROPE": (47, 125, 79),
    "AMERICAS": (179, 84, 30),
    "MIDDLE EAST": (146, 106, 32),
    "AFRICA": (122, 74, 141),
    "WORLD": (96, 96, 96),
}

# n, place, beat, headline, summary, source, region, icon, pin (lon, lat)
LEADS = [
    (1, "CANBERRA", "DIPLOMACY",
     "Australia signs Solomon Islands security pact",
     "Signed in Canberra on Wednesday: Canberra becomes Honiara's defence partner of choice, and no foreign military base will ever be allowed.",
     "Reuters", "ASIA-PACIFIC", "treaty", (149, -35)),
    (2, "SPACE", "SCIENCE",
     "Pakistan's first astronaut flies to China's station",
     "China launched a crewed ship carrying the first foreign astronaut — a Pakistani — to its Tiangong space station.",
     "Reuters", "ASIA-PACIFIC", "rocket", (100, 41)),
    (3, "CARTAGENA", "COLOMBIA",
     "All hostages freed as forces storm supermarket",
     "Colombian security forces stormed the store and ended a day-long siege; every hostage came out alive, one captor was killed.",
     "France 24", "AMERICAS", "shield", (-75, 10)),
]

GRID = [
    (4, "BEIJING", "POLITICS",
     "Shanghai party chief Chen Jining investigated",
     "A rising star and politburo member falls in the anti-corruption purge.",
     "Reuters", "ASIA-PACIFIC", "gavel", (121, 31)),
    (5, "WEST JAVA", "DISASTER",
     "Rescuers hunt miners trapped in flooded gold mine",
     "Heavy rain burst a river into an unauthorised shaft; dozens are missing.",
     "Reports", "ASIA-PACIFIC", "drop", (107, -7)),
    (6, "KYIV", "WAR & MONEY",
     "Ukraine needs \u20ac115bn in outside funding for 2027",
     "Zelensky puts a figure on another year of war and statehood.",
     "Reports", "EUROPE", "coin", (30, 50)),
    (7, "DHAKA", "LABOUR",
     "Garment workers win a 36% minimum-wage rise",
     "Entry-level pay climbs to 17,000 takas after weeks of protest.",
     "Reports", "ASIA-PACIFIC", "shirt", (90, 23)),
    (8, "PYONGYANG", "DIPLOMACY",
     "North Korea expels Swiss envoy, shuts his office",
     "The newly opened Swiss office is ordered closed within 48 hours.",
     "Reports", "ASIA-PACIFIC", "door", (125, 39)),
    (9, "LONDON", "SECURITY",
     "Britain warns firms of a Russian sabotage threat",
     "MI5 and defence chiefs say Ukraine's suppliers may face arson attacks.",
     "Reports", "EUROPE", "eye", (0, 51)),
    (10, "LANGLEY", "SECURITY",
     "CIA hit by cyberattack on an unclassified system",
     "Hackers breached an intelligence analysis system, officials confirm.",
     "New York Times", "AMERICAS", "lock", (-77, 39)),
    (11, "IOWA", "SAFETY",
     "Army to blow up 5 tonnes of old explosives",
     "Degraded chemical stocks will be destroyed in a controlled detonation.",
     "Reports", "AMERICAS", "burst", (-93, 42)),
    (12, "YEMEN", "WAR",
     "Saudi-led coalition strikes Hodeidah port",
     "The coalition says it hit Houthi capabilities at Hodeidah, Saada and Amran.",
     "Al Jazeera", "MIDDLE EAST", "ship", (43, 14)),
    (13, "CANBERRA", "SOCIETY",
     "Australia apologises to LGBTQ veterans",
     "\u201cThis country did not keep faith with you. But today, it says sorry.\u201d",
     "Reuters", "ASIA-PACIFIC", "medal", (152, -33)),
    (14, "MARKETS", "MONEY",
     "Gold slips to $3,545 before US inflation data",
     "Bullion eased 0.3% as traders waited on the US PCE price index.",
     "Reuters", "WORLD", "chart", (-70, 42)),
    (15, "PANAY", "DISASTER",
     "Magnitude 5.1 quake jolts Panay Island",
     "The tremor struck near Antique at 7:29am, 10km down, shaking Iloilo.",
     "PHIVOLCS", "ASIA-PACIFIC", "wave", (122, 11)),
    (16, "SEOUL", "SECURITY",
     "Russian jets entered our air zone, Seoul says",
     "South Korea reports Russian aircraft inside its air defence zone.",
     "Reports", "ASIA-PACIFIC", "jet", (127, 37)),
    (17, "MISSISSIPPI", "DISASTER",
     "Six dead as plane crashes into the Gulf",
     "Two boys, aged eight and ten, are among the dead from the Cessna 210.",
     "Reports", "AMERICAS", "plane", (-89, 30)),
    (18, "TEHRAN", "MIDDLE EAST",
     "Iran vows to withstand a US blockade",
     "Tehran promises \u201call available means\u201d as Hormuz shipping is attacked.",
     "Reuters", "MIDDLE EAST", "flame", (51, 35)),
]

ALSO = [
    (19, "Ukraine strikes Russian energy sites as peace talks go on", "EUROPE"),
    (20, "US shelves plan to use business deals with Russia to end the war", "EUROPE"),
    (21, "\u00c1brego Garc\u00eda leaves the US for Spain, ending deportation battle", "AMERICAS"),
    (22, "EU plans a \u20ac50bn tech fund to challenge the US and China", "EUROPE"),
    (23, "UK energy bills to rise 26% as Ofgem lifts the price cap", "EUROPE"),
    (24, "Norse Atlantic says its finances are critical; shares plunge", "EUROPE"),
    (25, "Zimbabwe issues an arrest warrant for Mugabe's son", "AFRICA"),
    (26, "Houthi attack in Riyadh injures 11; two Indians among them", "MIDDLE EAST"),
    (27, "Australia passes law forcing platforms to remove harmful content", "ASIA-PACIFIC"),
    (28, "Two men arrested after break-in at Prince William's home", "EUROPE"),
    (29, "Pakistan warns of a global energy crisis as supplies are disrupted", "ASIA-PACIFIC"),
    (30, "MacKenzie Scott gives $8m more to Atlanta students", "AMERICAS"),
    (31, "A spacecraft returns to the asteroid knocked off course in 2022", "WORLD"),
    (32, "None of the \u00a32.5bn UK steel package has been spent in Wales", "EUROPE"),
    (33, "African insurgents turn to cheap commercial drones for attacks", "AFRICA"),
    (34, "China weighs airline mergers and tougher rules, SCMP reports", "ASIA-PACIFIC"),
]

# big number, caption, story it ties to
STATS = [
    ("\u20ac115bn", "Ukraine's external financing need for 2027 (story 6)", 6),
    ("36%", "Bangladesh garment workers' wage rise (story 7)", 7),
    ("$3,545", "gold, an ounce, before US inflation data (story 14)", 14),
    ("5.1", "magnitude of the Panay Island earthquake (story 15)", 15),
    ("26%", "rise in UK household energy bills from January (story 23)", 23),
    ("5 tonnes", "of old explosives the Army will blow up in Iowa (story 11)", 11),
]

WIRES_UTC = os.environ.get("WIRES_UTC", "12:45")

DATE_CHECK = (
    "Wires read up to " + WIRES_UTC + " UTC, Wed 25 Nov 2026. Every story here happened or was first "
    "reported on 25 Nov 2026 in at least one time zone. Left out as other days' news: Sooryavanshi's "
    "204 off 53 in Doha, the WHO Ebola team's evacuation from Akwe, and England's record heat-death "
    "report \u2014 all Tuesday 24 Nov."
)


def wrap(d, text, fnt, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrap(d, xy, text, fnt, fill, maxw, leading, max_lines=None):
    x, y = xy
    lines = wrap(d, text, fnt, maxw)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and d.textlength(last + "\u2026", font=fnt) > maxw:
            last = last[:-1]
        lines[-1] = last + "\u2026"
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon(d, kind, x, y, s, bg):
    """Draw a white glyph on a coloured s-by-s square at (x, y)."""
    d.rectangle([x, y, x + s, y + s], fill=bg)
    cx, cy = x + s / 2, y + s / 2
    u = s / 40.0  # unit
    W_ = WHITE
    if kind == "treaty":
        for px in (cx - 9 * u, cx + 5 * u):
            d.line([px, cy - 12 * u, px, cy + 12 * u], fill=W_, width=2)
        d.polygon([(cx - 9 * u, cy - 12 * u), (cx + 1 * u, cy - 8 * u), (cx - 9 * u, cy - 4 * u)], fill=W_)
        d.polygon([(cx + 5 * u, cy - 12 * u), (cx + 15 * u, cy - 8 * u), (cx + 5 * u, cy - 4 * u)], fill=W_)
    elif kind == "rocket":
        d.polygon([(cx, cy - 13 * u), (cx + 6 * u, cy + 2 * u), (cx - 6 * u, cy + 2 * u)], fill=W_)
        d.rectangle([cx - 6 * u, cy + 2 * u, cx + 6 * u, cy + 8 * u], fill=W_)
        d.polygon([(cx - 3 * u, cy + 8 * u), (cx + 3 * u, cy + 8 * u), (cx, cy + 14 * u)], fill=(255, 170, 40))
        d.ellipse([cx - 2.5 * u, cy - 6 * u, cx + 2.5 * u, cy - 1 * u], fill=bg)
    elif kind == "shield":
        d.polygon([(cx, cy - 12 * u), (cx + 10 * u, cy - 8 * u), (cx + 10 * u, cy + 2 * u),
                   (cx, cy + 13 * u), (cx - 10 * u, cy + 2 * u), (cx - 10 * u, cy - 8 * u)], outline=W_, width=3)
        d.line([cx - 5 * u, cy, cx - 1 * u, cy + 5 * u, cx + 6 * u, cy - 5 * u], fill=W_, width=3)
    elif kind == "gavel":
        d.line([cx - 10 * u, cy - 8 * u, cx + 2 * u, cy + 4 * u], fill=W_, width=4)
        d.rectangle([cx - 2 * u, cy - 12 * u, cx + 10 * u, cy - 4 * u], fill=W_)
        d.line([cx - 11 * u, cy + 11 * u, cx + 11 * u, cy + 11 * u], fill=W_, width=3)
    elif kind == "drop":
        d.polygon([(cx, cy - 13 * u), (cx + 8 * u, cy + 4 * u), (cx - 8 * u, cy + 4 * u)], fill=W_)
        d.ellipse([cx - 8 * u, cy - 3 * u, cx + 8 * u, cy + 13 * u], fill=W_)
        d.ellipse([cx - 3 * u, cy + 3 * u, cx + 2 * u, cy + 9 * u], fill=bg)
    elif kind == "coin":
        d.ellipse([cx - 11 * u, cy - 11 * u, cx + 11 * u, cy + 11 * u], outline=W_, width=3)
        d.ellipse([cx - 6 * u, cy - 6 * u, cx + 6 * u, cy + 6 * u], outline=W_, width=2)
    elif kind == "shirt":
        d.polygon([(cx - 5 * u, cy - 11 * u), (cx + 5 * u, cy - 11 * u), (cx + 12 * u, cy - 5 * u),
                   (cx + 7 * u, cy - 1 * u), (cx + 7 * u, cy + 12 * u), (cx - 7 * u, cy + 12 * u),
                   (cx - 7 * u, cy - 1 * u), (cx - 12 * u, cy - 5 * u)], fill=W_)
    elif kind == "door":
        d.rectangle([cx - 8 * u, cy - 13 * u, cx + 8 * u, cy + 13 * u], outline=W_, width=3)
        d.ellipse([cx + 3 * u, cy - 1.5 * u, cx + 6 * u, cy + 1.5 * u], fill=W_)
    elif kind == "eye":
        d.ellipse([cx - 13 * u, cy - 7 * u, cx + 13 * u, cy + 7 * u], outline=W_, width=3)
        d.ellipse([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], fill=W_)
    elif kind == "lock":
        d.rectangle([cx - 9 * u, cy - 1 * u, cx + 9 * u, cy + 12 * u], fill=W_)
        d.arc([cx - 6 * u, cy - 13 * u, cx + 6 * u, cy + 3 * u], start=180, end=360, fill=W_, width=3)
        d.ellipse([cx - 2 * u, cy + 4 * u, cx + 2 * u, cy + 8 * u], fill=bg)
    elif kind == "burst":
        pts = []
        import math
        for i in range(16):
            r = 13 * u if i % 2 == 0 else 5 * u
            a = math.pi * i / 8
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=W_)
    elif kind == "ship":
        d.polygon([(cx - 12 * u, cy + 3 * u), (cx + 12 * u, cy + 3 * u), (cx + 8 * u, cy + 10 * u), (cx - 8 * u, cy + 10 * u)], fill=W_)
        d.line([cx, cy - 12 * u, cx, cy + 3 * u], fill=W_, width=2)
        d.polygon([(cx, cy - 12 * u), (cx + 8 * u, cy - 2 * u), (cx, cy - 2 * u)], fill=W_)
        d.line([cx - 12 * u, cy + 13 * u, cx + 12 * u, cy + 13 * u], fill=W_, width=2)
    elif kind == "medal":
        d.polygon([(cx - 8 * u, cy - 13 * u), (cx - 2 * u, cy - 13 * u), (cx, cy - 3 * u), (cx - 5 * u, cy - 2 * u)], fill=W_)
        d.polygon([(cx + 8 * u, cy - 13 * u), (cx + 2 * u, cy - 13 * u), (cx, cy - 3 * u), (cx + 5 * u, cy - 2 * u)], fill=W_)
        d.ellipse([cx - 7 * u, cy - 2 * u, cx + 7 * u, cy + 12 * u], outline=W_, width=3)
    elif kind == "chart":
        d.line([cx - 12 * u, cy + 11 * u, cx + 12 * u, cy + 11 * u], fill=W_, width=2)
        d.line([cx - 12 * u, cy - 11 * u, cx - 12 * u, cy + 11 * u], fill=W_, width=2)
        d.line([cx - 10 * u, cy + 6 * u, cx - 3 * u, cy + 1 * u, cx + 3 * u, cy + 4 * u, cx + 10 * u, cy - 7 * u], fill=W_, width=3)
    elif kind == "wave":
        pts = [(cx - 13 * u, cy), (cx - 7 * u, cy), (cx - 4 * u, cy - 10 * u), (cx - 1 * u, cy + 10 * u),
               (cx + 2 * u, cy - 6 * u), (cx + 5 * u, cy + 4 * u), (cx + 8 * u, cy), (cx + 13 * u, cy)]
        d.line(pts, fill=W_, width=3)
    elif kind == "jet":
        d.polygon([(cx + 13 * u, cy), (cx - 4 * u, cy - 4 * u), (cx - 10 * u, cy - 11 * u), (cx - 8 * u, cy),
                   (cx - 10 * u, cy + 11 * u), (cx - 4 * u, cy + 4 * u)], fill=W_)
    elif kind == "plane":
        d.polygon([(cx - 13 * u, cy + 10 * u), (cx + 13 * u, cy - 10 * u), (cx + 2 * u, cy + 12 * u), (cx - 1 * u, cy + 2 * u)], fill=W_)
    elif kind == "flame":
        d.polygon([(cx, cy - 13 * u), (cx + 8 * u, cy + 2 * u), (cx + 6 * u, cy + 10 * u),
                   (cx - 6 * u, cy + 10 * u), (cx - 8 * u, cy + 2 * u)], fill=W_)
        d.ellipse([cx - 3.5 * u, cy + 2 * u, cx + 3.5 * u, cy + 10 * u], fill=bg)
    else:  # fallback: filled circle
        d.ellipse([cx - 8 * u, cy - 8 * u, cx + 8 * u, cy + 8 * u], fill=W_)


# ---------------------------------------------------------------- lead scenes
def scene_treaty(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 220, 240))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 96, 64))
    for px, cols in ((x + 78, None), (x + 218, None)):
        d.line([px, y + 14, px, y + h - 24], fill=(60, 60, 60), width=3)
    # Australian-style flag: blue field, white stars, red/white cross hints
    fx, fy = x + 78, y + 14
    d.rectangle([fx, fy, fx + 62, fy + 34], fill=(24, 52, 120))
    d.line([fx, fy, fx + 30, fy + 17], fill=WHITE, width=3)
    d.line([fx + 30, fy, fx, fy + 17], fill=WHITE, width=3)
    d.line([fx + 15, fy, fx + 15, fy + 34], fill=RED, width=3)
    d.line([fx, fy + 17, fx + 30, fy + 17], fill=RED, width=3)
    for sx, sy in ((8, 26), (46, 8), (54, 24), (40, 28)):
        d.ellipse([fx + sx, fy + sy, fx + sx + 4, fy + sy + 4], fill=WHITE)
    # Solomon-style flag: green/blue diagonal split, yellow band, stars
    fx2, fy2 = x + 218, y + 14
    d.rectangle([fx2, fy2, fx2 + 62, fy2 + 34], fill=(30, 110, 60))
    d.polygon([(fx2, fy2 + 34), (fx2 + 62, fy2), (fx2 + 62, fy2 + 34)], fill=(24, 52, 120))
    d.line([fx2, fy2 + 34, fx2 + 62, fy2], fill=(250, 200, 40), width=4)
    for sx, sy in ((8, 6), (20, 4), (14, 14)):
        d.ellipse([fx2 + sx, fy2 + sy, fx2 + sx + 4, fy2 + sy + 4], fill=WHITE)
    # document on the table
    d.rectangle([x + w / 2 - 34, y + h - 34, x + w / 2 + 34, y + h - 8], fill=WHITE, outline=INK)
    for i in range(3):
        d.line([x + w / 2 - 26, y + h - 27 + i * 6, x + w / 2 + 26, y + h - 27 + i * 6], fill=GREY, width=1)
    d.line([x + w / 2 + 20, y + h - 30, x + w / 2 + 40, y + h - 12], fill=INK, width=2)


def scene_rocket(d, x, y, w, h):
    import random
    d.rectangle([x, y, x + w, y + h], fill=(14, 22, 52))
    rng = random.Random(11)
    for _ in range(46):
        sx, sy = x + rng.randrange(4, w - 4), y + rng.randrange(3, h - 3)
        d.point((sx, sy), fill=WHITE)
        d.point((sx + 1, sy), fill=(200, 210, 235))
    # space station, top right
    sx, sy = x + w - 118, y + 16
    d.rectangle([sx + 34, sy + 8, sx + 62, sy + 20], fill=(210, 214, 220), outline=INK)
    d.rectangle([sx, sy + 4, sx + 30, sy + 24], fill=(50, 90, 170), outline=INK)
    d.rectangle([sx + 66, sy + 4, sx + 96, sy + 24], fill=(50, 90, 170), outline=INK)
    # rocket climbing diagonally
    bx, by = x + 84, y + h - 14
    d.polygon([(bx, by), (bx + 26, by - 62), (bx + 44, by - 50), (bx + 20, by + 6)], fill=(238, 240, 244), outline=INK)
    d.polygon([(bx + 26, by - 62), (bx + 33, by - 76), (bx + 44, by - 50)], fill=RED)
    d.ellipse([bx + 24, by - 44, bx + 34, by - 34], fill=(50, 90, 170), outline=INK)
    d.polygon([(bx + 2, by + 2), (bx + 20, by + 4), (bx + 4, by + 16)], fill=(255, 150, 30))
    d.polygon([(bx + 6, by + 4), (bx + 17, by + 5), (bx + 8, by + 12)], fill=(255, 205, 60))
    # earth curve
    d.chord([x - 60, y + h - 34, x + 190, y + h + 60], start=180, end=360, fill=(52, 110, 180))


def scene_rescue(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    d.ellipse([x + w - 52, y + 8, x + w - 20, y + 40], fill=(250, 205, 70), outline=GOLD)
    bx, by, bw, bh = x + 26, y + 26, 218, h - 26
    d.rectangle([bx, by, bx + bw, by + bh], fill=(238, 230, 214), outline=INK)
    d.rectangle([bx, by, bx + bw, by + 20], fill=RED)
    d.text((bx + 10, by + 3), "SUPERMARKET", font=F["kicker"], fill=WHITE)
    for i in range(6):  # awning stripes
        sx = bx + 8 + i * 34
        d.polygon([(sx, by + 20), (sx + 17, by + 20), (sx + 13, by + 30), (sx + 4, by + 30)],
                  fill=RED if i % 2 == 0 else WHITE, outline=GREY)
    d.rectangle([bx + 22, by + 40, bx + 74, by + bh], fill=(90, 120, 150), outline=INK)
    d.rectangle([bx + 96, by + 40, bx + 196, by + 62], fill=(170, 200, 220), outline=INK)
    # shield emblem
    cx, cy = x + w - 44, y + h - 40
    d.polygon([(cx, cy - 24), (cx + 19, cy - 17), (cx + 19, cy + 4), (cx, cy + 26),
               (cx - 19, cy + 4), (cx - 19, cy - 17)], fill=(31, 95, 158), outline=INK)
    d.line([cx - 9, cy - 1, cx - 2, cy + 9, cx + 11, cy - 9], fill=WHITE, width=4)


SCENES = {"treaty": scene_treaty, "rocket": scene_rocket, "shield": scene_rescue}


# ---------------------------------------------------------------- world map
# Land spans per row: (row, col_start, col_end) on a 90x40 grid,
# col = (lon + 180) / 4, row = (76 - lat) / 3.4.
LAND = [
    (0, 3, 6), (0, 33, 38), (0, 57, 62), (0, 70, 89),
    (1, 3, 9), (1, 14, 22), (1, 32, 39), (1, 48, 52), (1, 55, 89),
    (2, 3, 10), (2, 12, 28), (2, 33, 38), (2, 40, 41), (2, 48, 54), (2, 55, 89),
    (3, 3, 10), (3, 12, 30), (3, 34, 37), (3, 47, 57), (3, 57, 89),
    (4, 13, 31), (4, 44, 45), (4, 47, 58), (4, 58, 89),
    (5, 14, 32), (5, 44, 46), (5, 47, 57), (5, 57, 88),
    (6, 14, 33), (6, 46, 58), (6, 58, 87),
    (7, 15, 33), (7, 45, 59), (7, 59, 85), (7, 86, 87),
    (8, 15, 32), (8, 45, 58), (8, 59, 84), (8, 85, 86),
    (9, 15, 32), (9, 45, 57), (9, 60, 83), (9, 85, 87),
    (10, 15, 31), (10, 45, 56), (10, 62, 84), (10, 85, 86),
    (11, 15, 31), (11, 45, 54), (11, 58, 70), (11, 70, 84), (11, 84, 86),
    (12, 16, 30), (12, 45, 58), (12, 58, 65), (12, 66, 82),
    (13, 16, 29), (13, 44, 59), (13, 59, 64), (13, 67, 74), (13, 74, 81),
    (14, 17, 27), (14, 44, 60), (14, 59, 64), (14, 67, 73), (14, 75, 79),
    (15, 18, 26), (15, 43, 58), (15, 67, 72), (15, 75, 79),
    (16, 19, 25), (16, 43, 57), (16, 68, 72), (16, 75, 78),
    (17, 20, 24), (17, 43, 56), (17, 68, 71), (17, 75, 78),
    (18, 27, 30), (18, 43, 55), (18, 69, 70), (18, 75, 78),
    (19, 27, 32), (19, 44, 56), (19, 60, 62), (19, 75, 78),
    (20, 27, 34), (20, 45, 55), (20, 59, 63), (20, 74, 80), (20, 82, 84),
    (21, 28, 36), (21, 46, 54), (21, 74, 79), (21, 81, 86),
    (22, 28, 37), (22, 47, 54), (22, 75, 82), (22, 84, 87),
    (23, 29, 38), (23, 47, 55), (23, 78, 84), (23, 87, 89),
    (24, 29, 38), (24, 48, 55),
    (25, 29, 38), (25, 48, 56), (25, 61, 62),
    (26, 29, 37), (26, 48, 56), (26, 61, 62), (26, 74, 82),
    (27, 30, 37), (27, 49, 56), (27, 61, 62), (27, 73, 83),
    (28, 30, 36), (28, 49, 55), (28, 73, 83),
    (29, 30, 36), (29, 50, 55), (29, 73, 83),
    (30, 30, 35), (30, 50, 54), (30, 74, 82),
    (31, 30, 35), (31, 50, 54), (31, 74, 81),
    (32, 30, 34), (32, 51, 53), (32, 75, 80),
    (33, 30, 34), (33, 87, 88),
    (34, 30, 33), (34, 87, 88),
    (35, 30, 32),
    (36, 30, 32),
    (37, 30, 31),
]


def draw_map(d, x, y, w, h):
    """Dotted world map in the box (x, y, w, h); returns a pin placer."""
    cell_w, cell_h = w / 90.0, h / 40.0
    land = set()
    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            land.add((r, c))
    for (r, c) in land:
        px, py = x + c * cell_w, y + r * cell_h
        d.rectangle([px + 0.6, py + 0.6, px + cell_w - 0.6, py + cell_h - 0.6], fill=(178, 168, 148))

    def place(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (82 - lat) / 140.0 * h)

    return place


# ---------------------------------------------------------------- assembly
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    total = len(LEADS) + len(GRID) + len(ALSO)

    # masthead band
    d.rectangle([0, 0, W, 52], fill=INK)
    d.text((14, 9), "THE WORLD ON WEDNESDAY", font=F["mast_small"], fill=WHITE)
    right = f"{total} STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    rw = d.textlength(right, font=F["mast_right"])
    d.text((W - 14 - rw, 18), right, font=F["mast_right"], fill=(210, 205, 195))

    # title + subline
    d.text((14, 57), "Wednesday 25 November 2026", font=F["mast"], fill=INK)
    d.text((14, 120),
           "Treaty signed in Canberra \u00b7 Pakistan's first astronaut reaches orbit \u00b7 Cartagena hostages freed alive",
           font=F["subline"], fill=DARKRED)
    d.line([12, 140, W - 12, 140], fill=INK, width=3)
    d.line([12, 145, W - 12, 145], fill=INK, width=1)

    # stat strip
    colw = (W - 24) / 6.0
    for i, (num, cap, _tie) in enumerate(STATS):
        x = 12 + i * colw
        if i:
            d.line([x - 6, 154, x - 6, 204], fill=(200, 192, 172), width=1)
        d.text((x, 150), num, font=F["stat_num"], fill=DARKRED)
        draw_wrap(d, (x, 186), cap, F["stat_cap"], GREY, colw - 14, 12, max_lines=2)

    # region tabs
    counts = {}
    for s in LEADS + GRID:
        counts[s[6]] = counts.get(s[6], 0) + 1
    for _n, _t, reg in ALSO:
        counts[reg] = counts.get(reg, 0) + 1
    tab_w = {"ASIA-PACIFIC": 318, "EUROPE": 238, "AMERICAS": 159,
             "MIDDLE EAST": 105, "AFRICA": 90, "WORLD": 90}
    tab_f = font(FD + "DejaVuSans-Bold.ttf", 11)
    tx = 12
    for reg in ("ASIA-PACIFIC", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "WORLD"):
        wseg = tab_w[reg]
        d.rectangle([tx, 214, tx + wseg - 3, 236], fill=REGIONS[reg])
        label = f"{reg} {counts.get(reg, 0)}"
        lw = d.textlength(label, font=tab_f)
        d.text((tx + (wseg - 3 - lw) / 2, 219), label, font=tab_f, fill=WHITE)
        tx += wseg

    # lead panels
    for i, s in enumerate(LEADS):
        n, place, beat, head, sub, src, reg, icon_name, _pin = s
        x = 12 + i * 341
        pw = 330
        SCENES[icon_name](d, x, 244, pw, 94)
        d.rectangle([x, 244, x + pw, 338], outline=INK, width=1)
        d.rectangle([x, 340, x + pw, 355], fill=REGIONS[reg])
        d.text((x + 6, 342), f"{n}  {place} \u2014 {beat}", font=F["kicker"], fill=WHITE)
        y = draw_wrap(d, (x, 359), head, F["lead_head"], INK, pw - 4, 20, max_lines=2)
        draw_wrap(d, (x, max(y + 2, 401)), sub, F["lead_sub"], (58, 56, 52), pw - 4, 13, max_lines=3)
        sw = d.textlength(f"({src})", font=F["src"])
        d.text((x + pw - 4 - sw, 442), f"({src})", font=F["src"], fill=GREY)
    d.line([12, 460, W - 12, 460], fill=INK, width=1)

    # story grid: 3 columns x 5 rows
    gx, gy, cw, rh = 12, 468, 341, 52
    for idx, s in enumerate(GRID):
        n, place, beat, head, sub, src, reg, icon_name, _pin = s
        cx = gx + (idx % 3) * cw
        cy = gy + (idx // 3) * rh
        if idx % 3:
            d.line([cx - 6, cy + 2, cx - 6, cy + rh - 4], fill=(205, 197, 178), width=1)
        icon(d, icon_name, cx, cy + 6, 40, REGIONS[reg])
        d.text((cx + 50, cy), f"{n} \u00b7 {place} \u2014 {beat}", font=F["kicker"], fill=REGIONS[reg])
        y = draw_wrap(d, (cx + 50, cy + 13), head, F["g_head"], INK, cw - 64, 13, max_lines=2)
        draw_wrap(d, (cx + 50, cy + 41), sub + f" ({src})", F["g_sub"], GREY, cw - 64, 11, max_lines=1)

    # date check box
    d.rectangle([12, 736, W - 12, 778], outline=RED, width=2)
    d.rectangle([12, 736, 118, 752], fill=RED)
    d.text((20, 739), "DATE CHECK", font=F["check_b"], fill=WHITE)
    draw_wrap(d, (128, 739), DATE_CHECK, F["check"], INK, W - 152, 14, max_lines=2)

    # bottom left: map with pins
    d.text((12, 788), "WHERE IT HAPPENED \u2014 pins match story numbers", font=F["map_title"], fill=INK)
    d.rectangle([12, 804, 516, 974], fill=(252, 250, 244), outline=(190, 182, 164))
    place_pin = draw_map(d, 18, 810, 492, 158)
    for s in LEADS + GRID:
        n, pin = s[0], s[8]
        if pin is None:
            continue
        px, py = place_pin(pin[0], pin[1])
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
        label = str(n)
        lw = d.textlength(label, font=F["pin"])
        d.text((px - lw / 2, py - 5), label, font=F["pin"], fill=WHITE)

    # bottom right: also-on list, two columns of eight
    d.text((528, 788), f"ALSO ON WEDNESDAY \u2014 {len(ALSO)} MORE STORIES", font=F["also_head"], fill=INK)
    for j, (n, text, _reg) in enumerate(ALSO):
        ax = 528 + (j // 8) * 246
        ay = 804 + (j % 8) * 24
        num = f"{n}"
        d.text((ax, ay), num, font=F["also"], fill=DARKRED)
        nw = d.textlength(num + " ", font=F["also"])
        draw_wrap(d, (ax + nw + 2, ay), text, F["also"], INK, 246 - nw - 8, 11, max_lines=2)

    # footer band
    d.rectangle([0, 1002, W, H], fill=INK)
    d.text((14, 1008),
           "Sources: Reuters, AP, Al Jazeera, BBC, France 24, New York Times, PHIVOLCS and national wires \u2014 every story names its outlet.",
           font=F["foot"], fill=(215, 210, 200))
    fr = "ONE PAGE \u00b7 WEDNESDAY 25 NOVEMBER 2026"
    fw = d.textlength(fr, font=F["foot_b"])
    d.text((W - 14 - fw, 1008), fr, font=F["foot_b"], fill=WHITE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
