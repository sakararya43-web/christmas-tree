"""
Christmas Tree ASCII Art & Animation Engine (Refined to match reference photo)
Generates the exact scene matching reference photo:
- Wide perspective ground grid (..., :::, ---, ===)
- Snow bank under tree (xxxx, XXXX, ****)
- Wrapped gift boxes (Red with gold ribbon, Royal Blue with ribbon, Burgundy, Gold center)
- Authentic foliage containing pine characters and reference tokens (0.0, 0**, %o, *ee#%*, etc.)
- Golden garland ribbons winding across (#ee*0, *#ee*o, *#XX*#)
- Crimson red bauble clusters (@, %, #, o) and golden bells
- Top golden star made of 'e' with radiant beam lines
- Bottom-to-top reveal animation synchronized to Sia - Snowman chorus!
"""

import math
import random
import json
import os

WIDTH = 84
HEIGHT = 62

# Character tokens
TREE_TOKENS = [
    "%", "#", "*", "+", "-", "=", ".", "o", "0", ":",
    "0.0", "0**", "%o", "0..00", "=0.0#", "+0.0",
]

GARLAND_TOKENS = ["#ee*0", "*ee#%*", "*%o%=", ":%o%:", "*#ee*o", "*#XX*#", "*ee*"]
STAR_CHARS = ["e", "@", "#", "*"]
SNOW_CHARS = [".", "·", "*", "+", "o", "❄"]

# Colors matching the reference image palette
COLOR_SKY = "#060913"
COLOR_GROUND_DIM = "#1e293b"
COLOR_GROUND_MID = "#334155"
COLOR_GROUND_BRIGHT = "#475569"
COLOR_GROUND_LINE = "#64748b"
COLOR_GROUND_FROST = "#cbd5e1"

COLOR_SNOW_BANK = "#e2e8f0"
COLOR_SNOW_DIM = "#94a3b8"

COLOR_PINE_DEEP = "#0e3818"
COLOR_PINE_DARK = "#14532d"
COLOR_PINE_MID = "#166534"
COLOR_PINE_BRIGHT = "#22c55e"
COLOR_PINE_TIP = "#4ade80"
COLOR_PINE_LIME = "#86efac"

COLOR_GARLAND_GOLD = "#facc15"
COLOR_GARLAND_BRIGHT = "#fef08a"
COLOR_GARLAND_WARM = "#eab308"

COLOR_ORNAMENT_RED = "#ef4444"
COLOR_ORNAMENT_DARK_RED = "#b91c1c"
COLOR_ORNAMENT_SHINE = "#fca5a5"

COLOR_BELL_GOLD = "#fde047"
COLOR_STAR_CORE = "#ffffff"
COLOR_STAR_GOLD = "#fef08a"
COLOR_STAR_BEAM = "#fde047"

COLOR_GIFT_RED = "#dc2626"
COLOR_GIFT_DARK_RED = "#991b1b"
COLOR_GIFT_BLUE = "#1d4ed8"
COLOR_GIFT_DARK_BLUE = "#1e3a8a"
COLOR_GIFT_RIBBON_GOLD = "#fde047"
COLOR_GIFT_RIBBON_CYAN = "#38bdf8"


class Cell:
    def __init__(self, char=" ", color="#ffffff", glow=0.0, layer="sky", y_pos=0):
        self.char = char
        self.color = color
        self.glow = glow
        self.layer = layer
        self.y_pos = y_pos

    def to_dict(self):
        return {
            "char": self.char,
            "color": self.color,
            "glow": round(self.glow, 2),
            "layer": self.layer,
        }


def build_static_scene(width=WIDTH, height=HEIGHT, seed=42):
    rng = random.Random(seed)
    grid = [[Cell(" ", "#000000", 0.0, "sky", y) for _ in range(width)] for y in range(height)]
    center_x = width // 2  # 42

    # 1. NIGHT SKY BACKGROUND STARS
    for y in range(height):
        for x in range(width):
            if rng.random() < 0.036:
                star_char = rng.choice([".", "·", "+", "*"])
                dimness = rng.uniform(0.3, 0.85)
                color = rng.choice(["#64748b", "#94a3b8", "#cbd5e1", "#e2e8f0", "#93c5fd"])
                grid[y][x] = Cell(star_char, color, dimness * 0.4, "sky", y)

    # 2. PERSPECTIVE GROUND PLANE (Rows 47 to 61)
    # Replicates the horizontal perspective grid in the reference image
    ground_top = 47
    for y in range(ground_top, height):
        row_idx = y - ground_top
        if y >= height - 3:
            main_char = "="
            sub_char = "+"
            step = 2
            col = COLOR_GROUND_LINE
            glow_val = 0.35
        elif y >= height - 6:
            main_char = "=" if y % 2 == 0 else "-"
            sub_char = "+" if y % 2 == 0 else ":"
            step = 3
            col = COLOR_GROUND_BRIGHT
            glow_val = 0.25
        elif y >= height - 10:
            main_char = "-" if y % 2 == 0 else ":"
            sub_char = ":" if y % 2 == 0 else "."
            step = 4
            col = COLOR_GROUND_MID
            glow_val = 0.15
        else:
            main_char = ":" if y % 2 == 0 else "."
            sub_char = "."
            step = 5
            col = COLOR_GROUND_DIM
            glow_val = 0.08

        for x in range(width):
            ch = sub_char if (x % step == 0) else main_char
            if rng.random() < 0.04:
                ch = "*"  # Frost spark
                c = COLOR_GROUND_FROST
            else:
                c = col
            grid[y][x] = Cell(ch, c, glow_val, "ground", y)

    # 3. SNOW BANK / BASE UNDER TREE (Rows 53 to 57)
    # Reference image has textured snow drift: xxxx, XXXX, ****, ====, ++++
    for y in range(54, 58):
        v = (y - 54) / 4.0
        w = int(22 + v * 8)
        for dx in range(-w, w + 1):
            x = center_x + dx
            if 0 <= x < width:
                if rng.random() < 0.82:
                    ch = rng.choice(["x", "X", "*", "+", "=", "-", "%"])
                    col = rng.choice([COLOR_SNOW_BANK, COLOR_SNOW_DIM, "#f1f5f9", "#cbd5e1"])
                    grid[y][x] = Cell(ch, col, 0.45, "ground", y)

    # 4. GIFTS AT THE BASE
    # Left Red Gift Box: x: 18-29, y: 51-58
    left_ribbon_x = 24
    left_ribbon_y = 54
    for y in range(51, 59):
        for x in range(18, 30):
            if x == left_ribbon_x or y == left_ribbon_y:
                ch = "+" if (x == left_ribbon_x and y == left_ribbon_y) else ("|" if x == left_ribbon_x else "=")
                grid[y][x] = Cell(ch, COLOR_GIFT_RIBBON_GOLD, 0.8, "gift", y)
            else:
                ch = rng.choice(["%", "#", "X", "@"])
                c = COLOR_GIFT_RED if x < left_ribbon_x else COLOR_GIFT_DARK_RED
                grid[y][x] = Cell(ch, c, 0.35, "gift", y)

    # Left Gift Bow
    grid[50][left_ribbon_x - 1] = Cell("(", COLOR_GIFT_RIBBON_GOLD, 0.85, "gift", 50)
    grid[50][left_ribbon_x] = Cell("o", COLOR_STAR_CORE, 0.95, "gift", 50)
    grid[50][left_ribbon_x + 1] = Cell(")", COLOR_GIFT_RIBBON_GOLD, 0.85, "gift", 50)

    # Center Burgundy Gift: x: 30-36, y: 53-58
    for y in range(53, 59):
        for x in range(30, 37):
            if x == 33 or y == 56:
                grid[y][x] = Cell("#", "#fca5a5", 0.55, "gift", y)
            else:
                grid[y][x] = Cell(rng.choice(["%", "#", "*"]), "#881337", 0.25, "gift", y)

    # Center Golden Accent Gift under trunk: x: 39-45, y: 53-56
    for y in range(53, 57):
        for x in range(39, 46):
            if x in (41, 42) or y == 55:
                grid[y][x] = Cell("e", COLOR_GARLAND_BRIGHT, 0.85, "gift", y)
            else:
                grid[y][x] = Cell(rng.choice(["#", "X", "*"]), COLOR_GARLAND_WARM, 0.6, "gift", y)

    # Right Royal Blue Gift Box: x: 57-69, y: 51-58
    right_ribbon_x = 63
    right_ribbon_y = 54
    for y in range(51, 59):
        for x in range(57, 70):
            if x == right_ribbon_x or y == right_ribbon_y:
                ch = "+" if (x == right_ribbon_x and y == right_ribbon_y) else ("|" if x == right_ribbon_x else "=")
                grid[y][x] = Cell(ch, COLOR_GIFT_RIBBON_CYAN, 0.8, "gift", y)
            else:
                ch = rng.choice(["%", "#", "8", "X"])
                c = COLOR_GIFT_BLUE if x < right_ribbon_x else COLOR_GIFT_DARK_BLUE
                grid[y][x] = Cell(ch, c, 0.35, "gift", y)

    # Right Gift Bow
    grid[50][right_ribbon_x - 1] = Cell("{", COLOR_GIFT_RIBBON_CYAN, 0.85, "gift", 50)
    grid[50][right_ribbon_x] = Cell("*", COLOR_STAR_CORE, 0.95, "gift", 50)
    grid[50][right_ribbon_x + 1] = Cell("}", COLOR_GIFT_RIBBON_CYAN, 0.85, "gift", 50)

    # 5. TREE TRUNK (Center base)
    for y in range(49, 56):
        for dx in range(-3, 4):
            x = center_x + dx
            ch = rng.choice(["#", "%", "8", "X"])
            shade = "#78350f" if abs(dx) <= 1 else "#451a03"
            grid[y][x] = Cell(ch, shade, 0.25, "trunk", y)

    # 6. TREE FOLIAGE (Pine Branches)
    tree_apex_y = 11
    tree_base_y = 50
    foliage_positions = set()

    for y in range(tree_apex_y, tree_base_y + 1):
        v = (y - tree_apex_y) / (tree_base_y - tree_apex_y)
        tier_phase = (v * 5.6) % 1.0
        tier_scallop = (tier_phase ** 0.65) * 3.4
        half_w = 1.6 + 25.0 * (v ** 0.94) + tier_scallop
        half_w = min(half_w, 29.0)

        x_start = int(round(center_x - half_w))
        x_end = int(round(center_x + half_w))

        for x in range(x_start, x_end + 1):
            if x < 0 or x >= width:
                continue

            foliage_positions.add((x, y))
            dist = abs(x - center_x)
            norm_r = dist / max(0.5, half_w)

            # Assign characters with reference tokens (0.0, %, #, *, +, =, -)
            if norm_r < 0.35:
                ch = rng.choice(["%", "#", "@", "8", "&", "X", "0"])
                col = rng.choice([COLOR_PINE_DEEP, COLOR_PINE_DARK, COLOR_PINE_MID])
                glow = 0.25
            elif norm_r < 0.72:
                ch = rng.choice(["*", "%", "+", "#", "x", "s", "o", "0", "="])
                col = rng.choice([COLOR_PINE_MID, COLOR_PINE_BRIGHT, "#15803d"])
                glow = 0.42
            else:
                ch = rng.choice(["*", "+", "-", "=", ".", "^", "o"])
                col = rng.choice([COLOR_PINE_BRIGHT, COLOR_PINE_TIP, COLOR_PINE_LIME])
                glow = 0.58

            grid[y][x] = Cell(ch, col, glow, "foliage", y)

    # Inject reference special character clusters (0.0, 0**, etc.)
    special_clusters = [
        (0.0, 0.18, "0.0#+"),
        (-0.2, 0.22, "==+0.0°0::++"),
        (0.15, 0.26, "*.0.0.."),
        (-0.35, 0.34, "00#%"),
        (0.28, 0.36, "0..00"),
        (-0.15, 0.48, "0.0#+"),
        (0.32, 0.58, "0**"),
    ]
    for x_rat, y_rat, token in special_clusters:
        sy = int(round(tree_apex_y + y_rat * (tree_base_y - tree_apex_y)))
        v = (sy - tree_apex_y) / (tree_base_y - tree_apex_y)
        half_w = 1.6 + 25.0 * (v ** 0.94)
        sx = int(round(center_x + x_rat * half_w)) - len(token) // 2
        for idx, ch in enumerate(token):
            px = sx + idx
            if (px, sy) in foliage_positions:
                grid[sy][px] = Cell(ch, COLOR_PINE_LIME if ch in ("0", ".") else COLOR_PINE_BRIGHT, 0.55, "foliage", sy)

    # 7. SPIRALING GOLDEN GARLAND LIGHTS
    num_garland_points = 280
    for i in range(num_garland_points):
        frac = i / float(num_garland_points)
        y = int(round(tree_apex_y + frac * (tree_base_y - tree_apex_y)))
        v = (y - tree_apex_y) / (tree_base_y - tree_apex_y)
        angle = v * 5.2 * 2.0 * math.pi - 0.4
        half_w = 1.6 + 25.0 * (v ** 0.94)
        z = math.cos(angle)

        if z > -0.25:
            x_offset = half_w * math.sin(angle) * 0.88
            x = int(round(center_x + x_offset))

            for dy in (-1, 0):
                curr_y = y + dy
                if (x, curr_y) in foliage_positions:
                    g_char = rng.choice(["e", "e", "@", "#", "*", "+", "o", "="])
                    col = COLOR_GARLAND_BRIGHT if z > 0.4 else COLOR_GARLAND_GOLD
                    grid[curr_y][x] = Cell(g_char, col, 0.85 + z * 0.15, "garland", curr_y)

    # 8. BELLS & ORNAMENTS (Baubles)
    ornaments = [
        (-0.35, 0.22, "red"), (0.32, 0.25, "red"), (0.05, 0.28, "bell"),
        (-0.52, 0.38, "bell"), (0.48, 0.39, "red"), (-0.15, 0.42, "red"),
        (0.22, 0.45, "bell"), (-0.42, 0.52, "red"), (0.38, 0.53, "red"),
        (0.02, 0.56, "bell"), (-0.62, 0.62, "red"), (0.58, 0.63, "bell"),
        (-0.25, 0.65, "red"), (0.28, 0.68, "red"), (-0.50, 0.74, "bell"),
        (0.45, 0.75, "red"), (-0.08, 0.78, "bell"), (0.12, 0.81, "red"),
        (-0.35, 0.85, "bell"), (0.35, 0.86, "red"), (-0.68, 0.89, "red"),
        (0.65, 0.90, "bell"), (-0.18, 0.93, "bell"), (0.20, 0.94, "red"),
    ]

    for x_rat, y_rat, otype in ornaments:
        oy = int(round(tree_apex_y + y_rat * (tree_base_y - tree_apex_y)))
        v = (oy - tree_apex_y) / (tree_base_y - tree_apex_y)
        half_w = 1.6 + 25.0 * (v ** 0.94)
        ox = int(round(center_x + x_rat * half_w))

        if (ox, oy) in foliage_positions:
            if otype == "red":
                for ddx in (-1, 0):
                    px = ox + ddx
                    if (px, oy) in foliage_positions:
                        ch = "@" if ddx == 0 else "%"
                        col = COLOR_ORNAMENT_RED if ddx == 0 else COLOR_ORNAMENT_DARK_RED
                        grid[oy][px] = Cell(ch, col, 0.85, "ornament", oy)
                if (ox, oy - 1) in foliage_positions:
                    grid[oy - 1][ox] = Cell(".", COLOR_ORNAMENT_SHINE, 0.95, "ornament", oy - 1)
            elif otype == "bell":
                if (ox, oy - 1) in foliage_positions:
                    grid[oy - 1][ox] = Cell("^", COLOR_GARLAND_WARM, 0.8, "bell", oy - 1)
                grid[oy][ox] = Cell("e", COLOR_BELL_GOLD, 0.95, "bell", oy)
                if (ox - 1, oy) in foliage_positions:
                    grid[oy][ox - 1] = Cell("o", COLOR_BELL_GOLD, 0.85, "bell", oy)
                if (ox + 1, oy) in foliage_positions:
                    grid[oy][ox + 1] = Cell("o", COLOR_BELL_GOLD, 0.85, "bell", oy)
                if (ox, oy + 1) in foliage_positions:
                    grid[oy + 1][ox] = Cell(".", COLOR_STAR_CORE, 0.9, "bell", oy + 1)

    # 9. TOP STAR (The Golden Pinnacle Crown from reference)
    # Exact structure in reference photo:
    #       e
    #      eee
    #     eeeee
    #    eeeeeee
    #     eeeee
    #      eee
    star_rows = [
        (5, ["e"]),
        (6, ["e", "e", "e"]),
        (7, ["e", "e", "e", "e", "e"]),
        (8, ["e", "e", "e", "e", "e", "e", "e"]),
        (9, ["e", "e", "e", "e", "e"]),
        (10, ["e", "e", "e"]),
    ]

    for sy, char_list in star_rows:
        num_c = len(char_list)
        start_x = center_x - (num_c // 2)
        for i, ch in enumerate(char_list):
            sx = start_x + i
            is_center = (i == num_c // 2)
            c_char = "@" if is_center and sy == 8 else ch
            c_col = COLOR_STAR_CORE if is_center else COLOR_STAR_GOLD
            grid[sy][sx] = Cell(c_char, c_col, 1.0, "star", sy)

    # 10. RADIANT CELESTIAL RAYS (Dashed radiant beams from reference)
    # Upper vertical ray
    for dy in range(1, 5):
        grid[5 - dy][center_x] = Cell("|", COLOR_STAR_BEAM, max(0.3, 1.0 - dy * 0.18), "beam", 5 - dy)

    # Upper-diagonal rays
    for d in range(1, 5):
        grid[5 - d][center_x - d * 2] = Cell("\\", COLOR_STAR_BEAM, max(0.3, 1.0 - d * 0.18), "beam", 5 - d)
        grid[5 - d][center_x + d * 2] = Cell("/", COLOR_STAR_BEAM, max(0.3, 1.0 - d * 0.18), "beam", 5 - d)

    # Horizontal rays
    for dx in range(1, 6):
        grid[8][center_x - 4 - dx] = Cell("-", COLOR_STAR_BEAM, max(0.3, 1.0 - dx * 0.15), "beam", 8)
        grid[8][center_x + 4 + dx] = Cell("-", COLOR_STAR_BEAM, max(0.3, 1.0 - dx * 0.15), "beam", 8)

    # Lower-diagonal rays
    for d in range(1, 4):
        grid[10 + d][center_x - d * 2] = Cell("/", COLOR_STAR_BEAM, max(0.3, 0.9 - d * 0.2), "beam", 10 + d)
        grid[10 + d][center_x + d * 2] = Cell("\\", COLOR_STAR_BEAM, max(0.3, 0.9 - d * 0.2), "beam", 10 + d)

    return grid


class SnowfallSystem:
    def __init__(self, width=WIDTH, height=HEIGHT, count=110, seed=123):
        self.width = width
        self.height = height
        rng = random.Random(seed)
        self.flakes = []
        for _ in range(count):
            self.flakes.append({
                "x": rng.uniform(0, width),
                "y": rng.uniform(0, height),
                "speed": rng.uniform(0.35, 0.95),
                "sway_amp": rng.uniform(0.3, 1.4),
                "sway_freq": rng.uniform(0.5, 1.8),
                "sway_phase": rng.uniform(0, math.pi * 2),
                "char": rng.choice([".", "·", "*", "+", "o", "❄"]),
                "color": rng.choice(["#ffffff", "#e2e8f0", "#cbd5e1", "#93c5fd"]),
                "glow": rng.uniform(0.35, 0.85),
            })

    def update(self, dt, t):
        for flake in self.flakes:
            flake["y"] += flake["speed"] * dt * 9.0
            flake["x"] += math.sin(t * flake["sway_freq"] + flake["sway_phase"]) * flake["sway_amp"] * dt * 2.8
            if flake["y"] >= self.height:
                flake["y"] = 0
                flake["x"] = random.uniform(0, self.width)
            if flake["x"] < 0:
                flake["x"] += self.width
            elif flake["x"] >= self.width:
                flake["x"] -= self.width


def get_animated_frame(static_scene, t_sec, total_build_duration=16.0, snow_system=None):
    """
    Synchronized Bottom-to-Top Animation:
    - t = 0.0s - 1.2s: "I want you to know that I'm never leaving..." -> Ground plane appears from bottom row.
    - t = 1.2s - 2.5s: "'Cause I'm Mrs. Snow..." -> Gifts assemble at base with ribbon sparkles.
    - t = 2.5s - 9.5s: "til death we'll be freezing... Yeah you are my home... So come on let's go..."
                       -> Pine tree ascends smoothly row by row from bottom (56) to apex (11).
                          Garlands and ornaments ignite as growth wave passes.
    - t = 9.5s - 11.5s: "Let's go below zero and hide from the sun!"
                        -> Crown star ignites with brilliant golden burst & celestial rays!
    - t = 11.5s+: Full celebration with continuous snowfall, garland light ripple, and shining star!
    """
    width = len(static_scene[0])
    height = len(static_scene)
    frame = [[Cell(" ", "#000000", 0.0, "sky", y) for _ in range(width)] for y in range(height)]

    # Sky stars are always present
    for y in range(height):
        for x in range(width):
            cell = static_scene[y][x]
            if cell.layer == "sky":
                twinkle = 0.5 + 0.5 * math.sin(t_sec * 2.5 + x * 0.7 + y * 1.3)
                frame[y][x] = Cell(cell.char, cell.color, cell.glow * twinkle, "sky", y)

    # Phase 1: Ground plane emergence (0.0s to 1.5s)
    ground_y_bottom = height - 1
    ground_y_top = 47
    ground_progress = min(1.0, t_sec / 1.5) if t_sec >= 0.0 else 0.0
    ground_cutoff_y = ground_y_bottom - ground_progress * (ground_y_bottom - ground_y_top)

    for y in range(ground_y_top, height):
        if y >= ground_cutoff_y:
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "ground":
                    age = y - ground_cutoff_y
                    flash = 1.0 + max(0.0, 1.0 - age) * 0.5
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * flash, "ground", y)

    # Phase 2: Gifts emergence (1.2s to 2.8s)
    gift_progress = min(1.0, max(0.0, (t_sec - 1.2) / 1.6))
    gift_cutoff_y = (height - 2) - gift_progress * 11
    for y in range(48, height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer == "gift" and y >= gift_cutoff_y:
                frame[y][x] = Cell(orig.char, orig.color, orig.glow, "gift", y)

    # Phase 3: Trunk and Tree Growth from Bottom to Top (2.5s to 9.5s)
    tree_bottom_y = 56
    tree_top_y = 11
    tree_progress = min(1.0, max(0.0, (t_sec - 2.5) / 7.0))
    current_tree_growth_y = tree_bottom_y - tree_progress * (tree_bottom_y - tree_top_y)

    for y in range(height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer in ("trunk", "foliage", "garland", "ornament", "bell"):
                if y >= current_tree_growth_y:
                    char = orig.char
                    color = orig.color
                    glow = orig.glow

                    dist = abs(y - current_tree_growth_y)
                    if dist < 1.8 and tree_progress < 1.0:
                        glow = 1.0
                        if random.random() < 0.25:
                            char = random.choice(["*", "+", "#", "o"])
                            color = COLOR_STAR_CORE

                    if t_sec > 9.5:
                        if orig.layer == "garland":
                            wave = math.sin(t_sec * 4.0 - y * 0.4 + x * 0.1)
                            glow = 0.7 + 0.3 * wave
                        elif orig.layer in ("ornament", "bell"):
                            shimmer = math.sin(t_sec * 3.0 + x * 0.5 + y * 0.8)
                            glow = 0.75 + 0.25 * shimmer

                    frame[y][x] = Cell(char, color, glow, orig.layer, y)

    # Phase 4: Star and Celestial Rays (9.5s to 11.5s - Vocal drop "Let's go below zero!")
    star_progress = min(1.0, max(0.0, (t_sec - 9.5) / 2.0))
    if star_progress > 0.0:
        star_pulse = 1.0 + 0.3 * math.sin(t_sec * 5.0)
        for y in range(height):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "star":
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * star_pulse, "star", y)
                elif orig.layer == "beam" and star_progress >= 0.4:
                    beam_frac = (star_progress - 0.4) / 0.6
                    dist = math.sqrt((x - width // 2) ** 2 + (y - 8) ** 2)
                    if dist <= beam_frac * 12.0:
                        pulse = 0.7 + 0.3 * math.sin(t_sec * 3.5 + dist * 0.5)
                        frame[y][x] = Cell(orig.char, orig.color, orig.glow * pulse, "beam", y)

    # Phase 5: Pixelated Snowfall
    if snow_system is not None:
        for flake in snow_system.flakes:
            fx = int(round(flake["x"])) % width
            fy = int(round(flake["y"])) % height
            bg_cell = frame[fy][fx]
            if bg_cell.layer in ("sky", "ground", "foliage"):
                if bg_cell.layer == "sky" or random.random() < 0.4:
                    frame[fy][fx] = Cell(flake["char"], flake["color"], flake["glow"], "snow", fy)

    return frame


def export_scene_data(json_path="tree_data.json"):
    scene = build_static_scene()
    data = {
        "width": WIDTH,
        "height": HEIGHT,
        "build_duration": 16.0,
        "cells": [[scene[y][x].to_dict() for x in range(WIDTH)] for y in range(HEIGHT)]
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Exported scene data to {json_path} ({os.path.getsize(json_path)} bytes)")


if __name__ == "__main__":
    export_scene_data()
