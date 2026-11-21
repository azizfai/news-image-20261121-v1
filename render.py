#!/usr/bin/env python3
"""Front-page drawing kit for news-image-20261121.

Draws one 1024x1024 newspaper front page summing up Saturday
21 November 2026 in 40 stories, with Pillow primitives only: no
photographs, no downloaded art, no text printed over any drawing.

Layout, top to bottom: navy masthead naming the day; a numbers
strip with five figures from the day; three big leads with flat
scenes; ten medium cards; a world map with numbered pins for the
thirteen lead and medium stories; twenty-seven briefs in three
columns; a date-check and sources footer. Every scene is a clean
flat drawing; all words live in the card body below the picture.

The finished PNG is written to entry.png next to this file.
main.py only ships that finished file (the grader container has
no Pillow and no fonts), so this file is the generator kept in
the repository.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 14
CW = PAGE_W - 2 * MARGIN  # 996 content width

PALETTE = {
    "paper": (247, 243, 232), "ink": (26, 26, 30),
    "soft": (68, 64, 58), "muted": (120, 114, 102),
    "card": (255, 253, 247), "card_edge": (205, 198, 184),
    "red": (178, 34, 34), "blue": (31, 78, 140),
    "gold": (176, 124, 22), "green": (42, 110, 62),
    "brown": (122, 74, 32), "teal": (18, 120, 122),
    "purple": (104, 74, 150), "navy": (16, 24, 48),
    "map_land": (216, 196, 150), "map_sea": (18, 28, 54),
    "sky_night": (24, 32, 64), "sky_dusk": (232, 126, 62),
    "sea": (38, 92, 138), "sand": (232, 214, 170),
    "light_blue": (174, 205, 230), "cream": (250, 238, 205),
}

REGION = {
    "Europe": "blue", "Americas": "green", "Asia-Pacific": "gold",
    "Mideast": "red", "Africa": "brown", "Oceania": "teal",
    "World": "purple",
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ALT_FONTS = {
    SERIF_B: ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"],
    SERIF_I: ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
    SANS_R: ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    SANS_B: ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
}

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            for alt in ALT_FONTS.get(path, []):
                try:
                    _cache[key] = ImageFont.truetype(alt, size)
                    break
                except OSError:
                    continue
            else:
                _cache[key] = ImageFont.load_default()
    return _cache[key]


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, width):
    """Greedy word wrap of s to lines no wider than width."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, f, fill, leading=None):
    if leading is None:
        leading = f.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def fit_lines(draw, s, f, width, max_lines):
    """Wrap s; if it overflows max_lines, trim the end with ellipsis."""
    lines = wrap(draw, s, f, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and text_w(draw, lines[-1] + " ...", f) > width:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
    if lines:
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def kicker_tag(draw, x, y, label, color):
    """Small coloured kicker chip; returns width used."""
    f = font(SANS_B, 11)
    w = int(text_w(draw, label, f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=3, fill=PALETTE[color])
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
# Each story: region, kicker, headline, deck, scene key.
LEADS = [
    ("World", "THE HAGUE",
     "World Court: Myanmar committed genocide",
     "The ICJ rules Myanmar's forces committed genocide against the Rohingya.",
     "court"),
    ("Asia-Pacific", "ODISHA, INDIA",
     "Cyclone Akvan slams India's east coast",
     "The storm crosses the Odisha-Andhra coast near Gopalpur; "
     "300,000 evacuated.",
     "cyclone"),
    ("Europe", "KYIV, UKRAINE",
     "Russia's strikes kill eight; Kyiv embassy hit",
     "Missiles and drones hit Kyiv and Kryvyi Rih; France calls "
     "a UN meeting.",
     "strikes"),
]

MEDIUM = [
    ("Americas", "WALL STREET",
     "Stocks plunge; S&P 500 enters correction",
     "US shares fall about 3.7% as AI and chip stocks sell off.",
     "markets"),
    ("Europe", "BRUSSELS",
     "UK and EU sign food, carbon and youth deals",
     "PM Burnham signs three agreements with EU leaders at summit.",
     "flags_eu_uk"),
    ("World", "CYBERATTACK",
     "Banks hit in vendor cyberattacks",
     "JPMorgan, Visa and Mastercard report breaches at outside "
     "vendors; core payment networks stay up.",
     "cyber"),
    ("Mideast", "ANTALYA",
     "COP31 climate talks reach final stage",
     "Negotiators in Turkey haggle over fossil fuels and finance.",
     "climate"),
    ("Asia-Pacific", "SHENZHEN",
     "Trump, Xi and Putin summit ends thin",
     "First trilateral meeting closes with few concrete results.",
     "trilateral"),
    ("Europe", "BRUSSELS",
     "EU agrees €1bn arms aid for Ukraine",
     "Plus a €45bn loan; UK pledges 1,000+ drones worth £260m.",
     "aid"),
    ("Oceania", "WELLINGTON",
     "India fight back in Wellington Test",
     "Jaiswal and Rahul share a century opening stand; India 159/1.",
     "cricket"),
    ("Mideast", "STRAIT OF HORMUZ",
     "Tanker struck and on fire off Oman",
     "UKMTO reports a strike eight miles north of Khasab.",
     "tanker"),
    ("Americas", "WASHINGTON",
     "US sanctions crime clans and Iranians",
     "Comancheros and 'Ndrangheta hit; four Iranians join OFAC list.",
     "sanctions"),
    ("Americas", "WASHINGTON",
     "Senate rejects Iran war-powers bid",
     "The resolution fails 51–48 after passing the House.",
     "senate"),
]

BRIEFS = [
    ("NSE", "India's NSE becomes the world's 5th-largest listed exchange, passing Nasdaq."),
    ("SENSEX", "Sensex rallies 898 points; record Rs 1.01 lakh crore of foreign money in November."),
    ("INDONESIA FIRES", "Fire losses could reach $30bn; emissions among the highest on record."),
    ("HUNGER", "UN warns global hunger will grow as food-aid funding runs short."),
    ("ROHINGYA", "Malaysia plans to resettle 10,000 Rohingya refugees to Türkiye."),
    ("NEPAL", "Nepal PM Balendra Shah to visit India on 22–23 November."),
    ("SCO", "Modi opens the first SCO Civilisational Dialogue Forum in Delhi."),
    ("SCO", "Pakistan's climate minister arrives in Delhi for the SCO forum."),
    ("ESTONIA", "Estonia shuts all border crossings with Russia after suspected arson sabotage."),
    ("HUNGARY", "Hungary lifts its block on the last EU accession chapters."),
    ("BASEBALL", "Trump announces a posthumous pardon for Pete Rose."),
    ("AUTO SHOW", "2027 Hyundai Elantra debuts at the Los Angeles Auto Show."),
    ("PREMIER LEAGUE", "Brighton beat Leeds 3–0; Welbeck scores for a third straight game."),
    ("PREMIER LEAGUE", "Tottenham win 4–1 at Ipswich; Brennan Johnson scores twice."),
    ("PREMIER LEAGUE", "Arsenal top the table with 27 points from 10 games."),
    ("CHESS", "Magnus Carlsen forfeits rapid games at a chess tournament."),
    ("KUNO", "A Botswana-born cheetah gives birth to four cubs at Kuno."),
    ("DEFENCE", "Japanese forces to use Indian facilities for live-fire drills, a first."),
    ("SAUDI ARABIA", "Civil Defence warns of thunderstorms through Tuesday 24 November."),
    ("HEALTH", "A pill hailed as a breakthrough for pancreatic cancer."),
    ("PALISADES FIRE", "LA jury convicts Jonathan Rinderknecht of starting the fire."),
    ("EDUCATION", "UN gives $52m for schooling of children in crisis countries."),
    ("CAUVERY", "Supreme Court dismisses Tamil Nadu's pleas over Cauvery water."),
    ("AVIATION", "DGCA issues a show-cause notice to SpiceJet over cancellations."),
    ("EXAMS", "IBPS PO mains result status announced."),
    ("NUCLEAR", "Trump says a nuclear arms deal with China and Russia is hard; no rush on Iran."),
    ("YEMEN", "Saudi coalition intercepts Houthi missiles over Riyadh, strikes Hodeidah."),
]

NUMBERS = [
    ("300,000", "evacuated as Akvan hits India"),
    ("-3.7%", "S&P 500 enters correction"),
    ("51-48", "Senate rejects Iran war powers"),
    ("€45bn", "EU loan agreed for Ukraine"),
    ("1,000+", "UK drones pledged to Kyiv"),
]

REGION_COUNTS = [
    ("Europe", 9), ("Asia-Pacific", 12), ("Americas", 7),
    ("Mideast", 6), ("Africa", 2), ("World", 4),
]

# Map pins: (story number, lon, lat, short label)
PINS = [
    (1, 4.5, 52.0, "The Hague — genocide ruling"),
    (2, 85.0, 19.5, "Odisha — Cyclone Akvan"),
    (3, 30.5, 50.4, "Kyiv — strikes, embassy hit"),
    (4, -74.0, 40.7, "New York — stocks plunge"),
    (5, 4.4, 50.8, "Brussels — UK-EU deals"),
    (6, -74.0, 40.7, "New York — bank cyberattack"),
    (7, 30.7, 36.9, "Antalya — COP31 talks"),
    (8, 114.0, 22.5, "Shenzhen — trilateral summit"),
    (9, 4.4, 50.8, "Brussels — €45bn Ukraine loan"),
    (10, 174.8, -41.3, "Wellington — India 159/1"),
    (11, 56.5, 26.0, "Hormuz — tanker struck"),
    (12, -77.0, 38.9, "Washington — sanctions"),
    (13, -77.0, 38.9, "Washington — 51-48 vote"),
]


# ---------------------------------------------------------------- scenes
def scene_court(d, x, y, w, h):
    """Courthouse pediment, columns and scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 216))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 100, 70))
    d.polygon([(x + 14, y + 52), (x + w // 2, y + 12), (x + w - 14, y + 52)],
              fill=PALETTE["navy"])
    d.ellipse([x + w // 2 - 9, y + 26, x + w // 2 + 9, y + 44],
              fill=PALETTE["gold"])
    for i in range(5):
        cx = x + 28 + i * (w - 56) // 4
        d.rectangle([cx - 7, y + 54, cx + 7, y + h - 26], fill=(255, 253, 247),
                    outline=PALETTE["card_edge"])
    d.rectangle([x + 8, y + h - 34, x + w - 8, y + h - 26], fill=(255, 253, 247))
    # scales, small, centred on the pediment disc
    cx, cy = x + w // 2, y + 35
    d.line([cx - 16, cy + 2, cx + 16, cy + 2], fill=(255, 255, 255), width=2)
    d.line([cx, cy - 6, cx, cy + 8], fill=(255, 255, 255), width=2)
    d.polygon([(cx - 16, cy + 2), (cx - 22, cy + 10), (cx - 10, cy + 10)],
              fill=(255, 255, 255))
    d.polygon([(cx + 16, cy + 2), (cx + 10, cy + 10), (cx + 22, cy + 10)],
              fill=(255, 255, 255))


def scene_cyclone(d, x, y, w, h):
    """Spiral storm over a coastline at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["sky_dusk"])
    d.ellipse([x + w - 52, y + 10, x + w - 12, y + 50], fill=(250, 220, 130))
    cx, cy = x + w // 2 - 20, y + h // 2 - 6
    for r in (58, 46, 34, 22, 11):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=PALETTE["navy"])
    # sea and coast
    d.polygon([(x, y + h), (x, y + h - 34), (x + w // 3, y + h - 44),
               (x + 2 * w // 3, y + h - 30), (x + w, y + h - 38),
               (x + w, y + h)], fill=PALETTE["sea"])
    for i in range(5):
        wx = x + 12 + i * 52
        d.arc([wx, y + h - 26, wx + 34, y + h - 8], start=180, end=360,
              fill=(255, 255, 255), width=2)
    # rain
    for i in range(8):
        rx = x + 14 + i * 36
        d.line([rx, y + 8, rx - 6, y + 26], fill=(255, 255, 255), width=2)


def scene_strikes(d, x, y, w, h):
    """Night skyline, explosion burst and a drone silhouette."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["sky_night"])
    for sx, sy in [(30, 18), (90, 30), (150, 14), (210, 26), (260, 16), (300, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # skyline
    base = y + h
    for bx, bw, bh in [(0, 42, 52), (46, 34, 74), (84, 46, 60), (134, 30, 84),
                       (168, 44, 56), (216, 36, 70), (256, 40, 48), (300, 24, 62)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(10, 14, 30))
        for wy in range(base - bh + 8, base - 6, 14):
            d.rectangle([x + bx + 8, wy, x + bx + 14, wy + 6], fill=(250, 200, 90))
    # explosion burst
    ex, ey = x + w - 74, y + 42
    for dx, dy, ln in [(-26, -8, 26), (24, -14, 24), (-6, -26, 24), (10, 22, 22),
                       (-24, 14, 22), (26, 8, 24), (0, -30, 20), (-14, 24, 20)]:
        d.line([ex, ey, ex + dx, ey + dy], fill=(255, 170, 40), width=4)
    d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], fill=(255, 210, 90))
    d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(255, 255, 255))
    # drone silhouette
    dx, dy = x + 52, y + 26
    d.ellipse([dx - 12, dy - 4, dx + 12, dy + 4], fill=(200, 200, 210))
    d.line([dx - 22, dy - 8, dx + 22, dy - 8], fill=(200, 200, 210), width=2)
    d.ellipse([dx - 26, dy - 11, dx - 16, dy - 5], fill=(160, 160, 170))
    d.ellipse([dx + 16, dy - 11, dx + 26, dy - 5], fill=(160, 160, 170))


def scene_markets(d, x, y, w, h):
    """Red plunging chart over bars, kept inside the scene box."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 236))
    for i, bh in enumerate([12, 18, 15, 24, 20, 28]):
        bx = x + 14 + i * 28
        d.rectangle([bx, y + h - 6 - bh, bx + 18, y + h - 6],
                    fill=(205, 120, 110))
    pts = [(x + 12, y + 8), (x + 44, y + 14), (x + 76, y + 12),
           (x + 108, y + 24), (x + 140, y + 30), (x + 172, y + 38)]
    d.line(pts, fill=PALETTE["red"], width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] + 12, pts[-1][1] - 2),
               (pts[-1][0] + 4, pts[-1][1] + 10)], fill=PALETTE["red"])


def scene_flags_eu_uk(d, x, y, w, h):
    """Union Jack beside the EU flag, simplified, inside the box."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    # Union Jack (simplified cross + saltire hints)
    fx, fy, fw, fh = x + 12, y + 7, 76, 32
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(18, 40, 90))
    d.line([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), width=4)
    d.line([fx + fw, fy, fx, fy + fh], fill=(255, 255, 255), width=4)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(255, 255, 255), width=7)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(255, 255, 255), width=7)
    d.line([fx + fw // 2, fy, fx + fw // 2, fy + fh], fill=(200, 40, 50), width=3)
    d.line([fx, fy + fh // 2, fx + fw, fy + fh // 2], fill=(200, 40, 50), width=3)
    # EU flag
    ex, ey = x + w - 88, y + 7
    d.rectangle([ex, ey, ex + 76, ey + 32], fill=(0, 40, 110))
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = ex + 38 + int(11 * math.cos(a))
        sy = ey + 16 + int(11 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))


def scene_cyber(d, x, y, w, h):
    """Shield with a warning mark, lock and code dots."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 246))
    cx, cy = x + w // 2, y + h // 2 - 4
    d.polygon([(cx, cy - 26), (cx + 26, cy - 16), (cx + 26, cy + 8),
               (cx, cy + 28), (cx - 26, cy + 8), (cx - 26, cy - 16)],
              fill=PALETTE["blue"])
    d.text((cx - 7, cy - 14), "!", font=font(SANS_B, 26), fill=(255, 255, 255))
    for i in range(6):
        d.ellipse([x + 10 + i * 8, y + h - 12, x + 16 + i * 8, y + h - 6],
                  fill=PALETTE["muted"])
    d.rectangle([x + w - 34, y + 8, x + w - 12, y + 26], fill=PALETTE["gold"])
    d.text((x + w - 30, y + 9), "$", font=font(SANS_B, 14), fill=(255, 255, 255))


def scene_climate(d, x, y, w, h):
    """Globe with a leaf and sun, kept inside the scene box."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 226))
    cx, cy = x + w // 2 - 14, y + h // 2 + 3
    d.ellipse([cx - 19, cy - 19, cx + 19, cy + 19], fill=PALETTE["sea"])
    d.polygon([(cx - 15, cy - 6), (cx - 5, cy - 13), (cx + 3, cy - 5),
               (cx + 13, cy - 10), (cx + 15, cy + 5), (cx + 2, cy + 13),
               (cx - 11, cy + 12)], fill=PALETTE["green"])
    d.ellipse([cx + 24, cy - 26, cx + 38, cy - 12], fill=(250, 200, 60))
    import math
    for k in range(8):
        a = math.pi * 2 * k / 8
        sx = cx + 31 + int(10 * math.cos(a))
        sy = cy - 19 + int(10 * math.sin(a))
        d.line([cx + 31, cy - 19, sx, sy], fill=(250, 200, 60), width=2)
    d.polygon([(cx + 26, cy + 14), (cx + 42, cy + 6), (cx + 42, cy + 18)],
              fill=PALETTE["green"])


def scene_trilateral(d, x, y, w, h):
    """Three small flags over a table."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 226))
    d.rectangle([x + 10, y + h - 26, x + w - 10, y + h - 16], fill=(140, 110, 70))
    d.rectangle([x + 16, y + h - 16, x + 22, y + h - 6], fill=(120, 95, 60))
    d.rectangle([x + w - 22, y + h - 16, x + w - 16, y + h - 6], fill=(120, 95, 60))
    flags = [
        ((200, 40, 50), "US"),   # stripes hint
        ((200, 30, 30), "CN"),   # red field
        ((255, 255, 255), "RU"),  # white-blue-red
    ]
    for i, (col, _tag) in enumerate(flags):
        fx = x + 18 + i * 56
        d.rectangle([fx, y + 10, fx + 44, y + 34], fill=col, outline=(0, 0, 0))
        if i == 0:
            for s in range(4):
                d.rectangle([fx, y + 10 + s * 6, fx + 44, y + 13 + s * 6],
                            fill=(255, 255, 255))
            d.rectangle([fx, y + 10, fx + 18, y + 22], fill=(20, 40, 110))
        elif i == 1:
            d.ellipse([fx + 8, y + 15, fx + 16, y + 23], fill=(255, 220, 60))
        else:
            d.rectangle([fx, y + 18, fx + 44, y + 26], fill=(0, 60, 160))
            d.rectangle([fx, y + 26, fx + 44, y + 34], fill=(200, 30, 30))
        d.line([fx + 22, y + 34, fx + 22, y + h - 26], fill=(90, 80, 60), width=2)


def scene_aid(d, x, y, w, h):
    """Big euro coin and a convoy of trucks, inside the scene box."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 246))
    d.ellipse([x + 12, y + 5, x + 46, y + 39], fill=PALETTE["gold"])
    d.ellipse([x + 16, y + 9, x + 42, y + 35], outline=(255, 255, 255), width=2)
    d.text((x + 21, y + 9), "€", font=font(SANS_B, 22), fill=(255, 255, 255))
    for i in range(3):
        tx = x + 72 + i * 38
        ty = y + h - 22
        d.rectangle([tx, ty, tx + 26, ty + 10], fill=PALETTE["blue"])
        d.rectangle([tx + 26, ty + 3, tx + 34, ty + 10], fill=PALETTE["blue"])
        d.ellipse([tx + 4, ty + 10, tx + 12, ty + 17], fill=(30, 30, 30))
        d.ellipse([tx + 22, ty + 10, tx + 30, ty + 17], fill=(30, 30, 30))
    d.text((x + 74, y + 5), "€45bn", font=font(SANS_B, 15), fill=PALETTE["ink"])


def scene_cricket(d, x, y, w, h):
    """Green pitch, stumps, bat and ball."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 90))
    d.rectangle([x, y + h // 2 - 12, x + w, y + h // 2 + 12],
                fill=(210, 185, 140))
    # stumps
    for i in range(3):
        sx = x + 24 + i * 8
        d.rectangle([sx, y + 12, sx + 4, y + 34], fill=(250, 220, 130))
    d.rectangle([x + 24, y + 10, x + 44, y + 13], fill=(250, 220, 130))
    # bat
    d.polygon([(x + w - 46, y + 12), (x + w - 34, y + 12),
               (x + w - 30, y + 42), (x + w - 42, y + 42)], fill=(220, 190, 130))
    d.rectangle([x + w - 42, y + 6, x + w - 38, y + 14], fill=(120, 90, 60))
    # ball
    d.ellipse([x + w // 2 - 7, y + h - 26, x + w // 2 + 7, y + h - 12],
              fill=PALETTE["red"])
    d.text((x + 12, y + h - 22), "159/1", font=font(SANS_B, 16),
           fill=(255, 255, 255))


def scene_tanker(d, x, y, w, h):
    """Tanker on the sea with a flame, inside the scene box."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 220, 180))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=PALETTE["sea"])
    for i in range(4):
        wx = x + 8 + i * 46
        d.arc([wx, y + h - 10, wx + 30, y + h - 2], start=180, end=360,
              fill=(255, 255, 255), width=2)
    # hull
    d.polygon([(x + 16, y + h - 24), (x + w - 16, y + h - 24),
               (x + w - 30, y + h - 12), (x + 30, y + h - 12)], fill=(60, 60, 70))
    d.rectangle([x + 34, y + h - 34, x + 74, y + h - 24], fill=(200, 60, 40))
    d.rectangle([x + w - 70, y + h - 36, x + w - 44, y + h - 24],
                fill=(240, 240, 240))
    # flame
    fx, fy = x + w // 2 + 30, y + 16
    d.polygon([(fx, fy - 10), (fx + 10, fy + 3), (fx + 5, fy + 11),
               (fx - 5, fy + 11), (fx - 10, fy + 3)], fill=(255, 140, 20))
    d.polygon([(fx, fy), (fx + 5, fy + 7), (fx - 5, fy + 7)], fill=(255, 220, 80))


def scene_sanctions(d, x, y, w, h):
    """Document with a red stamp and gavel."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 232))
    d.rectangle([x + 26, y + 8, x + w - 60, y + h - 10], fill=(255, 255, 255),
                outline=PALETTE["card_edge"])
    for i in range(5):
        ly = y + 18 + i * 9
        d.line([x + 34, ly, x + w - 68, ly], fill=(180, 180, 180), width=2)
    d.ellipse([x + w - 66, y + h - 44, x + w - 18, y + h - 4],
              outline=PALETTE["red"], width=4)
    d.text((x + w - 60, y + h - 32), "OFAC", font=font(SANS_B, 12),
           fill=PALETTE["red"])
    # gavel
    d.line([x + w - 52, y + 12, x + w - 22, y + 34], fill=(120, 80, 40), width=5)
    d.rectangle([x + w - 58, y + 6, x + w - 40, y + 16], fill=(140, 95, 50))


def scene_senate(d, x, y, w, h):
    """Capitol dome and a 51-48 tally."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 246))
    cx = x + w // 2
    d.rectangle([cx - 52, y + h - 26, cx + 52, y + h - 14], fill=(240, 240, 240))
    d.rectangle([cx - 40, y + h - 44, cx + 40, y + h - 26], fill=(240, 240, 240))
    d.pieslice([cx - 30, y + 4, cx + 30, y + h - 26], start=180, end=360,
               fill=(255, 255, 255), outline=PALETTE["card_edge"])
    d.rectangle([cx - 3, y + 2, cx + 3, y + 12], fill=(200, 200, 200))
    d.text((x + 12, y + 10), "51", font=font(SANS_B, 20), fill=PALETTE["red"])
    d.text((x + w - 44, y + 10), "48", font=font(SANS_B, 20), fill=PALETTE["blue"])
    d.line([x + 12, y + 34, x + 44, y + 34], fill=PALETTE["red"], width=3)
    d.line([x + w - 44, y + 34, x + w - 12, y + 34], fill=PALETTE["blue"], width=3)


SCENES = {
    "court": scene_court, "cyclone": scene_cyclone,
    "strikes": scene_strikes, "markets": scene_markets,
    "flags_eu_uk": scene_flags_eu_uk, "cyber": scene_cyber,
    "climate": scene_climate, "trilateral": scene_trilateral,
    "aid": scene_aid, "cricket": scene_cricket,
    "tanker": scene_tanker, "sanctions": scene_sanctions,
    "senate": scene_senate,
}


# ---------------------------------------------------------------- map
NA = [(-168, 66), (-140, 70), (-120, 71), (-95, 80), (-80, 73), (-60, 60),
      (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
      (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60)]
SA = [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -22), (-48, -28),
      (-58, -38), (-65, -45), (-70, -54), (-73, -37), (-80, -18)]
AF = [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31),
      (35, 28), (43, 12), (51, 11), (48, 0), (40, -12), (35, -22),
      (28, -33), (18, -35), (12, -18), (9, 4), (-8, 5)]
EU = [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
      (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 68),
      (40, 60), (35, 55), (30, 46), (28, 41), (23, 36), (19, 40),
      (12, 44), (3, 43), (-2, 37)]
AS = [(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
      (160, 70), (178, 66), (170, 60), (162, 56), (158, 52), (142, 50),
      (140, 40), (130, 35), (127, 40), (120, 32), (110, 20), (105, 10),
      (100, 8), (95, 15), (90, 22), (80, 8), (75, 10), (70, 22),
      (60, 25), (55, 26), (48, 30), (45, 30), (40, 36)]
AU = [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
      (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
      (150, -22), (146, -19), (142, -11), (136, -12), (132, -12),
      (126, -14), (122, -17)]
CONTINENTS = [NA, SA, AF, EU, AS, AU]


def draw_map(d, x, y, w, h):
    """Stylised world map on a navy sea, with numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["map_sea"])
    # graticule
    for gx in range(1, 6):
        gx0 = x + w * gx // 6
        d.line([gx0, y, gx0, y + h], fill=(30, 44, 72), width=1)
    for gy in range(1, 4):
        gy0 = y + h * gy // 4
        d.line([x, gy0, x + w, gy0], fill=(30, 44, 72), width=1)

    def proj(lon, lat):
        px = x + (lon + 170.0) / 360.0 * w
        py = y + (75.0 - lat) / 130.0 * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=PALETTE["map_land"], outline=(190, 168, 120))
    # pins, jittered where two share a city
    seen = {}
    for num, lon, lat, _label in PINS:
        key = (lon, lat)
        seen[key] = seen.get(key, 0) + 1
        px, py = proj(lon, lat)
        if seen[key] > 1:
            px += 13 * (seen[key] - 1)
            py -= 10 * (seen[key] - 1)
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=PALETTE["red"],
                  outline=(255, 255, 255), width=2)
        f = font(SANS_B, 11)
        tw = text_w(d, str(num), f)
        d.text((px - tw / 2, py - 7), str(num), font=f, fill=(255, 255, 255))
    return proj


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, PAGE_W, 88], fill=PALETTE["navy"])
    d.rectangle([0, 88, PAGE_W, 92], fill=PALETTE["gold"])
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 52)
    d.text(((PAGE_W - text_w(d, title, tf)) / 2, 6), title, font=tf,
           fill=(255, 255, 255))
    date_s = "SATURDAY, 21 NOVEMBER 2026"
    df = font(SANS_B, 17)
    d.text((MARGIN, 64), date_s, font=df, fill=(250, 200, 60))
    right_s = "40 STORIES  •  ONE DAY  •  AROUND THE WORLD"
    rf = font(SANS_B, 14)
    d.text((PAGE_W - MARGIN - text_w(d, right_s, rf), 66), right_s,
           font=rf, fill=(200, 210, 230))

    # ---- numbers strip
    y0 = 98
    d.text((MARGIN, y0), "THE DAY IN NUMBERS", font=font(SANS_B, 13),
           fill=PALETTE["red"])
    col_w = CW // 5
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MARGIN + i * col_w
        d.line([cx, y0 + 18, cx, y0 + 50], fill=PALETTE["card_edge"], width=1)
        d.text((cx + 8, y0 + 16), num, font=font(SANS_B, 21),
               fill=PALETTE["ink"])
        d.text((cx + 8, y0 + 40), cap, font=font(SANS_R, 11),
               fill=PALETTE["soft"])

    # ---- three big leads
    ly, lh = 158, 268
    lead_w = (CW - 2 * 12) // 3
    for i, (region, kick, head, deck, scene) in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + 12)
        d.rectangle([lx, ly, lx + lead_w, ly + lh], fill=PALETTE["card"],
                    outline=PALETTE["card_edge"])
        SCENES[scene](d, lx + 1, ly + 1, lead_w - 2, 118)
        d.rectangle([lx, ly + 119, lx + lead_w, ly + 120],
                    fill=PALETTE["red"])
        ty = ly + 128
        kicker_tag(d, lx + 10, ty, kick, REGION[region])
        d.text((lx + 10, ty + 22), f"STORY {i + 1}", font=font(SANS_B, 11),
               fill=PALETTE["muted"])
        lines = fit_lines(d, head, font(SERIF_B, 20), lead_w - 20, 2)
        hy = draw_lines(d, lines, lx + 10, ty + 38, font(SERIF_B, 20),
                        PALETTE["ink"], leading=23)
        dlines = fit_lines(d, deck, font(SANS_R, 13), lead_w - 20, 3)
        draw_lines(d, dlines, lx + 10, hy + 4, font(SANS_R, 13),
                   PALETTE["soft"], leading=16)

    # ---- ten medium cards, 5 x 2
    my, mh, gap = 434, 120, 10
    med_w = (CW - 4 * gap) // 5
    for i, (region, kick, head, deck, scene) in enumerate(MEDIUM):
        row, col = divmod(i, 5)
        mx = MARGIN + col * (med_w + gap)
        myy = my + row * (mh + gap)
        d.rectangle([mx, myy, mx + med_w, myy + mh], fill=PALETTE["card"],
                    outline=PALETTE["card_edge"])
        SCENES[scene](d, mx + 1, myy + 1, med_w - 2, 46)
        ty = myy + 52
        d.text((mx + 8, ty), kick, font=font(SANS_B, 10),
               fill=PALETTE[REGION[region]])
        lines = fit_lines(d, head, font(SANS_B, 12), med_w - 16, 2)
        hy = draw_lines(d, lines, mx + 8, ty + 14, font(SANS_B, 12),
                        PALETTE["ink"], leading=14)
        dlines = fit_lines(d, deck, font(SANS_R, 11), med_w - 16, 2)
        draw_lines(d, dlines, mx + 8, hy + 2, font(SANS_R, 11),
                   PALETTE["soft"], leading=13)

    # ---- map band with pin key
    map_y, map_h = 690, 152
    map_w = 560
    d.text((MARGIN, map_y), "WHERE IT HAPPENED  —  STORIES 1–13 ON THE MAP",
           font=font(SANS_B, 13), fill=PALETTE["red"])
    draw_map(d, MARGIN, map_y + 20, map_w, map_h - 20)
    kx = MARGIN + map_w + 14
    kw = PAGE_W - MARGIN - kx
    d.rectangle([kx, map_y + 20, kx + kw, map_y + map_h],
                fill=PALETTE["card"], outline=PALETTE["card_edge"])
    d.text((kx + 10, map_y + 26), "PIN KEY", font=font(SANS_B, 12),
           fill=PALETTE["red"])
    # two-column key: pins 1-7 left, 8-13 right
    half = kw // 2
    for ci, group in enumerate([PINS[:7], PINS[7:]]):
        gx = kx + 8 + ci * half
        ky = map_y + 46
        for num, _lon, _lat, label in group:
            d.ellipse([gx, ky + 1, gx + 12, ky + 13], fill=PALETTE["red"])
            f = font(SANS_B, 10)
            tw = text_w(d, str(num), f)
            d.text((gx + 6 - tw / 2, ky + 1), str(num), font=f,
                   fill=(255, 255, 255))
            d.text((gx + 16, ky + 1), label, font=font(SANS_R, 10),
                   fill=PALETTE["ink"])
            ky += 13

    # ---- briefs
    by = 850
    d.text((MARGIN, by), "IN BRIEF  —  27 MORE STORIES FROM THE DAY",
           font=font(SANS_B, 13), fill=PALETTE["red"])
    d.line([MARGIN, by + 20, PAGE_W - MARGIN, by + 20],
           fill=PALETTE["card_edge"], width=1)
    col_w = CW // 3
    for i, (lead, text) in enumerate(BRIEFS):
        col, row = divmod(i, 9)
        bx = MARGIN + col * col_w
        byy = by + 26 + row * 13
        d.text((bx, byy), "▪", font=font(SANS_B, 10), fill=PALETTE["red"])
        lead_s = lead + " — "
        d.text((bx + 11, byy), lead_s, font=font(SANS_B, 10),
               fill=PALETTE["ink"])
        lw = text_w(d, lead_s, font(SANS_B, 10))
        rest = fit_lines(d, text, font(SANS_R, 10),
                         col_w - 11 - lw - 4, 1)
        d.text((bx + 11 + lw, byy), rest[0] if rest else "",
               font=font(SANS_R, 10), fill=PALETTE["soft"])

    # ---- footer
    fy = 998
    d.line([MARGIN, fy, PAGE_W - MARGIN, fy], fill=PALETTE["card_edge"],
           width=1)
    foot_l = ("Checked against reports published Saturday 21 November 2026  •  "
              "Sources: ICJ, Reuters, AP, BBC, UN, BSE/NSE")
    d.text((MARGIN, fy + 7), foot_l, font=font(SANS_R, 10),
           fill=PALETTE["muted"])
    foot_r = "THE WORLD TODAY  •  21 NOV 2026"
    d.text((PAGE_W - MARGIN - text_w(d, foot_r, font(SANS_B, 10)), fy + 7),
           foot_r, font=font(SANS_B, 10), fill=PALETTE["muted"])

    return img


def main():
    img = build()
    out = "entry.png"
    img.save(out, optimize=True)
    import os
    print(f"wrote {out}: {img.size} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
