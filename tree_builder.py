"""
Christmas Tree ASCII Art & Animation Engine
Generates the festive ASCII scene matching reference.jpeg with:
- Ground perspective grid
- Wrapped gift boxes with ribbons & bows
- Tiered pine tree foliage with natural serrated branches
- Spiraling golden garland lights
- Hanging golden bells & crimson baubles
- Golden crown star with radiant light beams
- White pixelated snowfall & night sky stars
- Bottom-to-top growth animation sequence (>= 15 seconds)
"""

import math
import random
import json
import os

WIDTH = 84
HEIGHT = 62

# Character palettes
TREE_CHARS_DENSE = ["%", "#", "@", "8", "&", "X"]
TREE_CHARS_MID = ["*", "%", "+", "#", "x", "s", "o"]
TREE_CHARS_LIGHT = ["*", "+", "-", "=", ".", "^", "~"]

GARLAND_CHARS = ["e", "@", "#", "*", "+", "o", "=", "%"]
STAR_CHARS = ["e", "@", "#", "*", "+"]
SNOW_CHARS = [".", "·", "*", "+", "o", "❄"]

# Color hex constants matching reference
COLOR_SKY = "#070b19"
COLOR_GROUND_BASE = "#232a3e"
COLOR_GROUND_SNOW = "#4b5b75"
COLOR_GROUND_LINE = "#64748b"

COLOR_PINE_DEEP = "#0f3e1a"
COLOR_PINE_MID = "#166534"
COLOR_PINE_BRIGHT = "#22c55e"
COLOR_PINE_TIP = "#4ade80"
COLOR_PINE_HIGHLIGHT = "#86efac"

COLOR_GARLAND_GOLD = "#facc15"
COLOR_GARLAND_BRIGHT = "#fef08a"
COLOR_GARLAND_WARM = "#eab308"

COLOR_ORNAMENT_RED = "#ef4444"
COLOR_ORNAMENT_DARK_RED = "#b91c1c"
COLOR_ORNAMENT_SHINE = "#fca5a5"

COLOR_BELL_GOLD = "#fde047"
COLOR_BELL_DEEP = "#d97706"

COLOR_STAR_CORE = "#ffffff"
COLOR_STAR_GOLD = "#fef08a"
COLOR_STAR_BEAM = "#fde047"

COLOR_GIFT_RED = "#dc2626"
COLOR_GIFT_DARK_RED = "#991b1b"
COLOR_GIFT_BLUE = "#2563eb"
COLOR_GIFT_DARK_BLUE = "#1e3a8a"
COLOR_GIFT_RIBBON_GOLD = "#fde047"
COLOR_GIFT_RIBBON_CYAN = "#38bdf8"

COLOR_SNOW_DIM = "#94a3b8"
COLOR_SNOW_BRIGHT = "#ffffff"


class Cell:
    def __init__(self, char=" ", color="#ffffff", glow=0.0, layer="sky", y_pos=0):
        self.char = char
        self.color = color
        self.glow = glow
        self.layer = layer  # sky, ground, gift, trunk, foliage, garland, ornament, bell, star, beam
        self.y_pos = y_pos

    def to_dict(self):
        return {
            "char": self.char,
            "color": self.color,
            "glow": round(self.glow, 2),
            "layer": self.layer,
        }


def build_static_scene(width=WIDTH, height=HEIGHT, seed=42):
    """
    Builds the complete finished scene matching reference.jpeg.
    Returns a 2D grid of Cell objects [height][width].
    """
    rng = random.Random(seed)
    grid = [[Cell(" ", "#000000", 0.0, "sky", y) for _ in range(width)] for y in range(height)]

    center_x = width // 2  # 42

    # 1. NIGHT SKY BACKGROUND STARS (Scattered delicately)
    for y in range(height):
        for x in range(width):
            if rng.random() < 0.035:
                star_char = rng.choice([".", "·", "+", "*"])
                dimness = rng.uniform(0.3, 0.9)
                blue_shift = rng.choice(["#64748b", "#94a3b8", "#cbd5e1", "#e2e8f0", "#93c5fd"])
                grid[y][x] = Cell(star_char, blue_shift, dimness * 0.4, "sky", y)

    # 2. GROUND PERSPECTIVE GRID (Rows 48 to 61)
    # Reference image has perspective grid with lines of =, -, +, :, .
    ground_top = 48
    for y in range(ground_top, height):
        row_frac = (y - ground_top) / max(1, (height - 1 - ground_top))
        # Line character varies with perspective
        if y >= height - 3:
            main_char = "="
            sub_char = "+"
            step = 2
            col = COLOR_GROUND_LINE
            glow_val = 0.4
        elif y >= height - 7:
            main_char = "=" if y % 2 == 0 else "-"
            sub_char = "+" if y % 2 == 0 else ":"
            step = 3
            col = "#475569"
            glow_val = 0.2
        elif y >= height - 11:
            main_char = "-" if y % 2 == 0 else ":"
            sub_char = ":" if y % 2 == 0 else "."
            step = 4
            col = "#334155"
            glow_val = 0.1
        else:
            main_char = ":" if y % 2 == 0 else "."
            sub_char = "."
            step = 5
            col = "#1e293b"
            glow_val = 0.05

        for x in range(width):
            # Ground spreads across bottom with perspective
            char = sub_char if (x % step == 0) else main_char
            if rng.random() < 0.05:
                char = "*"  # Frost spark
                col_c = "#e2e8f0"
            else:
                col_c = col
            grid[y][x] = Cell(char, col_c, glow_val, "ground", y)

    # 3. GIFTS AT THE BASE (Sitting on ground)
    # Left Gift (Large Red Box with Gold Ribbon): x: 18-30, y: 51-58
    left_box_l, left_box_r = 17, 29
    left_box_t, left_box_b = 51, 58
    left_ribbon_x = 23
    left_ribbon_y = 54

    for y in range(left_box_t, left_box_b + 1):
        for x in range(left_box_l, left_box_r + 1):
            if x == left_ribbon_x or y == left_ribbon_y:
                char = "+" if (x == left_ribbon_x and y == left_ribbon_y) else ("|" if x == left_ribbon_x else "=")
                grid[y][x] = Cell(char, COLOR_GIFT_RIBBON_GOLD, 0.7, "gift", y)
            else:
                char = rng.choice(["%", "#", "X", "@"])
                shade = COLOR_GIFT_RED if x < left_ribbon_x else COLOR_GIFT_DARK_RED
                grid[y][x] = Cell(char, shade, 0.3, "gift", y)

    # Left Gift Bow on top
    grid[left_box_t - 1][left_ribbon_x - 1] = Cell("(", COLOR_GIFT_RIBBON_GOLD, 0.8, "gift", left_box_t - 1)
    grid[left_box_t - 1][left_ribbon_x] = Cell("o", COLOR_STAR_CORE, 0.9, "gift", left_box_t - 1)
    grid[left_box_t - 1][left_ribbon_x + 1] = Cell(")", COLOR_GIFT_RIBBON_GOLD, 0.8, "gift", left_box_t - 1)

    # Small Dark Burgundy Gift Box: x: 29-35, y: 53-58
    for y in range(53, 59):
        for x in range(29, 36):
            if x == 32 or y == 56:
                grid[y][x] = Cell("#", "#fca5a5", 0.5, "gift", y)
            else:
                grid[y][x] = Cell(rng.choice(["%", "#", "*"]), "#881337", 0.2, "gift", y)

    # Right Gift (Royal Blue Box with Ribbon): x: 56-68, y: 51-58
    right_box_l, right_box_r = 57, 68
    right_box_t, right_box_b = 51, 58
    right_ribbon_x = 62
    right_ribbon_y = 54

    for y in range(right_box_t, right_box_b + 1):
        for x in range(right_box_l, right_box_r + 1):
            if x == right_ribbon_x or y == right_ribbon_y:
                char = "+" if (x == right_ribbon_x and y == right_ribbon_y) else ("|" if x == right_ribbon_x else "=")
                grid[y][x] = Cell(char, COLOR_GIFT_RIBBON_CYAN, 0.7, "gift", y)
            else:
                char = rng.choice(["%", "#", "8", "X"])
                shade = COLOR_GIFT_BLUE if x < right_ribbon_x else COLOR_GIFT_DARK_BLUE
                grid[y][x] = Cell(char, shade, 0.3, "gift", y)

    # Right Gift Bow
    grid[right_box_t - 1][right_ribbon_x - 1] = Cell("{", COLOR_GIFT_RIBBON_CYAN, 0.8, "gift", right_box_t - 1)
    grid[right_box_t - 1][right_ribbon_x] = Cell("*", COLOR_STAR_CORE, 0.9, "gift", right_box_t - 1)
    grid[right_box_t - 1][right_ribbon_x + 1] = Cell("}", COLOR_GIFT_RIBBON_CYAN, 0.8, "gift", right_box_t - 1)

    # 4. TREE TRUNK (Center base)
    trunk_y_start, trunk_y_end = 49, 56
    trunk_width = 3
    for y in range(trunk_y_start, trunk_y_end + 1):
        for dx in range(-trunk_width, trunk_width + 1):
            x = center_x + dx
            char = rng.choice(["#", "%", "8", "X"])
            shade = "#78350f" if abs(dx) <= 1 else "#451a03"
            grid[y][x] = Cell(char, shade, 0.2, "trunk", y)

    # 5. TREE FOLIAGE (Pine Branches)
    # Apex at y=11, Base at y=50.
    tree_apex_y = 11
    tree_base_y = 50

    foliage_positions = set()

    for y in range(tree_apex_y, tree_base_y + 1):
        v = (y - tree_apex_y) / (tree_base_y - tree_apex_y)  # 0 at top to 1 at bottom

        # Layered natural branch tiers (5 distinct tiers)
        tier_phase = (v * 5.5) % 1.0
        tier_scallop = (tier_phase ** 0.65) * 3.2

        # Base width calculation
        half_w = 1.6 + 24.5 * (v ** 0.94) + tier_scallop
        half_w = min(half_w, 28.5)

        x_start = int(round(center_x - half_w))
        x_end = int(round(center_x + half_w))

        for x in range(x_start, x_end + 1):
            if x < 0 or x >= width:
                continue

            foliage_positions.add((x, y))

            dist_from_center = abs(x - center_x)
            norm_r = dist_from_center / max(0.5, half_w)

            # Character and color based on depth/layer
            if norm_r < 0.35:
                char = rng.choice(TREE_CHARS_DENSE)
                color = rng.choice([COLOR_PINE_DEEP, COLOR_PINE_MID, "#14532d"])
                glow = 0.25
            elif norm_r < 0.72:
                char = rng.choice(TREE_CHARS_MID)
                color = rng.choice([COLOR_PINE_MID, COLOR_PINE_BRIGHT, "#15803d"])
                glow = 0.4
            else:
                char = rng.choice(TREE_CHARS_LIGHT)
                color = rng.choice([COLOR_PINE_BRIGHT, COLOR_PINE_TIP, COLOR_PINE_HIGHLIGHT])
                glow = 0.55

            grid[y][x] = Cell(char, color, glow, "foliage", y)

    # 6. SPIRALING GOLDEN GARLAND LIGHTS
    # Spirals gracefully around the cone in 5 loops
    num_garland_points = 260
    garland_coords = set()

    for i in range(num_garland_points):
        frac = i / float(num_garland_points)
        y = int(round(tree_apex_y + frac * (tree_base_y - tree_apex_y)))
        v = (y - tree_apex_y) / (tree_base_y - tree_apex_y)

        # 5.2 full spiral rotations
        angle = v * 5.2 * 2.0 * math.pi - 0.4
        half_w = 1.6 + 24.5 * (v ** 0.94)

        # 3D projection: visible on front half
        z = math.cos(angle)
        if z > -0.25:  # Front-facing or edge
            x_offset = half_w * math.sin(angle) * 0.88
            x = int(round(center_x + x_offset))

            for dy in (-1, 0):
                curr_y = y + dy
                if (x, curr_y) in foliage_positions:
                    garland_coords.add((x, curr_y))
                    g_char = rng.choice(GARLAND_CHARS)
                    # Brighter towards the center of front
                    brightness_col = COLOR_GARLAND_BRIGHT if z > 0.4 else COLOR_GARLAND_GOLD
                    grid[curr_y][x] = Cell(g_char, brightness_col, 0.85 + z * 0.15, "garland", curr_y)

    # 7. BELLS & ORNAMENTS (Baubles)
    # Carefully scattered ornaments across the foliage
    ornament_locations = [
        # (x_offset_ratio, y_ratio, type: 'red' or 'bell')
        (-0.35, 0.22, "red"), (0.32, 0.25, "red"), (0.05, 0.28, "bell"),
        (-0.52, 0.38, "bell"), (0.48, 0.39, "red"), (-0.15, 0.42, "red"),
        (0.22, 0.45, "bell"), (-0.42, 0.52, "red"), (0.38, 0.53, "red"),
        (0.02, 0.56, "bell"), (-0.62, 0.62, "red"), (0.58, 0.63, "bell"),
        (-0.25, 0.65, "red"), (0.28, 0.68, "red"), (-0.50, 0.74, "bell"),
        (0.45, 0.75, "red"), (-0.08, 0.78, "bell"), (0.12, 0.81, "red"),
        (-0.35, 0.85, "bell"), (0.35, 0.86, "red"), (-0.68, 0.89, "red"),
        (0.65, 0.90, "bell"), (-0.18, 0.93, "bell"), (0.20, 0.94, "red"),
    ]

    for x_rat, y_rat, otype in ornament_locations:
        oy = int(round(tree_apex_y + y_rat * (tree_base_y - tree_apex_y)))
        v = (oy - tree_apex_y) / (tree_base_y - tree_apex_y)
        half_w = 1.6 + 24.5 * (v ** 0.94)
        ox = int(round(center_x + x_rat * half_w))

        if (ox, oy) in foliage_positions:
            if otype == "red":
                # Red Bauble cluster (2x2 or 3x1)
                for ddx in (-1, 0):
                    for ddy in (0,):
                        px, py = ox + ddx, oy + ddy
                        if (px, py) in foliage_positions:
                            ch = "@" if ddx == 0 else "%"
                            col = COLOR_ORNAMENT_RED if ddx == 0 else COLOR_ORNAMENT_DARK_RED
                            grid[py][px] = Cell(ch, col, 0.8, "ornament", py)
                # Highlight glint
                if (ox, oy - 1) in foliage_positions:
                    grid[oy - 1][ox] = Cell(".", COLOR_ORNAMENT_SHINE, 0.9, "ornament", oy - 1)
            elif otype == "bell":
                # Golden Bell: top bow, bell bell shape, clapper
                if (ox, oy - 1) in foliage_positions:
                    grid[oy - 1][ox] = Cell("^", COLOR_GARLAND_WARM, 0.8, "bell", oy - 1)
                grid[oy][ox] = Cell("e", COLOR_BELL_GOLD, 0.95, "bell", oy)
                if (ox - 1, oy) in foliage_positions:
                    grid[oy][ox - 1] = Cell("o", COLOR_BELL_GOLD, 0.85, "bell", oy)
                if (ox + 1, oy) in foliage_positions:
                    grid[oy][ox + 1] = Cell("o", COLOR_BELL_GOLD, 0.85, "bell", oy)
                if (ox, oy + 1) in foliage_positions:
                    grid[oy + 1][ox] = Cell(".", COLOR_STAR_CORE, 0.9, "bell", oy + 1)

    # 8. TOP STAR (The Golden Pinnacle Crown)
    # Matches the exact structure in reference.jpeg:
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

    # 9. RADIANT CELESTIAL RAYS (Emitted from top star)
    # Reference image has radiant lines: \ | / and -- * --
    # Upper vertical ray
    for dy in range(1, 5):
        grid[5 - dy][center_x] = Cell("|", COLOR_STAR_BEAM, max(0.3, 1.0 - dy * 0.18), "beam", 5 - dy)

    # Upper-left diagonal ray
    for d in range(1, 5):
        grid[5 - d][center_x - d * 2] = Cell("\\", COLOR_STAR_BEAM, max(0.3, 1.0 - d * 0.18), "beam", 5 - d)

    # Upper-right diagonal ray
    for d in range(1, 5):
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
    def __init__(self, width=WIDTH, height=HEIGHT, count=120, seed=123):
        self.width = width
        self.height = height
        rng = random.Random(seed)
        self.flakes = []
        for _ in range(count):
            self.flakes.append({
                "x": rng.uniform(0, width),
                "y": rng.uniform(0, height),
                "speed": rng.uniform(0.35, 1.1),
                "sway_amp": rng.uniform(0.3, 1.5),
                "sway_freq": rng.uniform(0.5, 2.0),
                "sway_phase": rng.uniform(0, math.pi * 2),
                "char": rng.choice([".", "·", "*", "+", "o", "❄"]),
                "color": rng.choice(["#ffffff", "#e2e8f0", "#cbd5e1", "#93c5fd"]),
                "glow": rng.uniform(0.3, 0.9),
            })

    def update(self, dt, t):
        for flake in self.flakes:
            flake["y"] += flake["speed"] * dt * 10.0
            flake["x"] += math.sin(t * flake["sway_freq"] + flake["sway_phase"]) * flake["sway_amp"] * dt * 3.0
            if flake["y"] >= self.height:
                flake["y"] = 0
                flake["x"] = random.uniform(0, self.width)
            if flake["x"] < 0:
                flake["x"] += self.width
            elif flake["x"] >= self.width:
                flake["x"] -= self.width


def get_animated_frame(static_scene, t_sec, total_build_duration=16.0, snow_system=None):
    """
    Computes the frame state at timestamp t_sec for the bottom-to-top animation.
    Animation Phases:
    0.0s - 1.5s: Silent night sky, initial snowflakes falling.
    1.5s - 3.5s: Ground perspective plane settles upward from bottom-most row.
    3.5s - 5.5s: Gift boxes at base assemble with ribbon sparkles.
    5.5s - 13.5s: Tree growth phase! Conical pine ascends smoothly from bottom (row 50) to top (row 11).
                  Garlands and ornaments light up in the wake of the growth line.
                  Leading edge sparkles with glowing ascent particles.
    13.5s - 15.5s: Crown reached! Golden star coalesces, flares, and radiant beams burst into sky.
    15.5s+: Full celebration! Continuous gentle snow, garland light ripples, shimmering ornaments, pulsating star!
    """
    width = len(static_scene[0])
    height = len(static_scene)

    # Deep copy / create active frame
    frame = [[Cell(" ", "#000000", 0.0, "sky", y) for _ in range(width)] for y in range(height)]

    # Sky stars are always present
    for y in range(height):
        for x in range(width):
            cell = static_scene[y][x]
            if cell.layer == "sky":
                # Twinkle calculation
                twinkle = 0.5 + 0.5 * math.sin(t_sec * 2.5 + x * 0.7 + y * 1.3)
                frame[y][x] = Cell(cell.char, cell.color, cell.glow * twinkle, "sky", y)

    # Phase 1: Ground emergence (1.5s to 3.5s)
    # Ground rows: 61 down to 48 (14 rows). Reveal starts at row 61 and goes up to 48.
    ground_y_bottom = height - 1
    ground_y_top = 48

    ground_progress = 0.0
    if t_sec >= 1.5:
        ground_progress = min(1.0, (t_sec - 1.5) / 2.0)

    ground_current_cutoff_y = ground_y_bottom - ground_progress * (ground_y_bottom - ground_y_top)

    for y in range(ground_y_top, height):
        if y >= ground_current_cutoff_y:
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "ground":
                    # Flash slightly as row appears
                    age = y - ground_current_cutoff_y
                    flash = 1.0 + max(0.0, 1.0 - age) * 0.6
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * flash, "ground", y)

    # Phase 2: Gifts emergence (3.0s to 5.0s)
    gift_progress = 0.0
    if t_sec >= 3.0:
        gift_progress = min(1.0, (t_sec - 3.0) / 2.0)

    gift_cutoff_y = (height - 2) - gift_progress * 10
    for y in range(48, height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer == "gift":
                if y >= gift_cutoff_y:
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow, "gift", y)

    # Phase 3: Trunk and Tree Growth from Bottom to Top (5.0s to 13.5s)
    tree_bottom_y = 56  # Includes trunk
    tree_top_y = 11

    tree_progress = 0.0
    if t_sec >= 5.0:
        tree_progress = min(1.0, (t_sec - 5.0) / 8.5)

    current_tree_growth_y = tree_bottom_y - tree_progress * (tree_bottom_y - tree_top_y)

    for y in range(height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer in ("trunk", "foliage", "garland", "ornament", "bell"):
                if y >= current_tree_growth_y:
                    # Cell is revealed!
                    dist_from_growth_crest = abs(y - current_tree_growth_y)

                    char = orig.char
                    color = orig.color
                    glow = orig.glow

                    # If this row was just revealed, add a sparkle flash
                    if dist_from_growth_crest < 1.8 and tree_progress < 1.0:
                        glow = 1.0
                        if random.random() < 0.25:
                            char = random.choice(["*", "+", "#", "o"])
                            color = COLOR_STAR_CORE

                    # Post-growth dynamic twinkling
                    if t_sec > 13.5:
                        if orig.layer == "garland":
                            # Ripple light wave along garlands
                            wave = math.sin(t_sec * 4.0 - y * 0.4 + x * 0.1)
                            glow = 0.7 + 0.3 * wave
                        elif orig.layer in ("ornament", "bell"):
                            shimmer = math.sin(t_sec * 3.0 + x * 0.5 + y * 0.8)
                            glow = 0.75 + 0.25 * shimmer

                    frame[y][x] = Cell(char, color, glow, orig.layer, y)

    # Phase 4: Star and Celestial Rays (13.5s to 15.5s)
    star_progress = 0.0
    if t_sec >= 13.5:
        star_progress = min(1.0, (t_sec - 13.5) / 2.0)

    if star_progress > 0.0:
        # Star appears with pulsing bloom
        star_pulse = 1.0 + 0.3 * math.sin(t_sec * 5.0) * min(1.0, star_progress * 2.0)
        for y in range(height):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "star":
                    # Reveal star rows
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * star_pulse, "star", y)
                elif orig.layer == "beam" and star_progress >= 0.5:
                    beam_frac = (star_progress - 0.5) / 0.5
                    # Beams shoot outwards
                    dist_from_apex = math.sqrt((x - width // 2) ** 2 + (y - 8) ** 2)
                    max_reach = beam_frac * 12.0
                    if dist_from_apex <= max_reach:
                        pulse = 0.7 + 0.3 * math.sin(t_sec * 3.5 + dist_from_apex * 0.5)
                        frame[y][x] = Cell(orig.char, orig.color, orig.glow * pulse, "beam", y)

    # Phase 5: Pixelated Snowfall
    if snow_system is not None:
        for flake in snow_system.flakes:
            fx = int(round(flake["x"])) % width
            fy = int(round(flake["y"])) % height
            # Snow displays on top of sky or softly overlays foliage
            bg_cell = frame[fy][fx]
            if bg_cell.layer in ("sky", "ground", "foliage"):
                if bg_cell.layer == "sky" or random.random() < 0.4:
                    frame[fy][fx] = Cell(flake["char"], flake["color"], flake["glow"], "snow", fy)

    return frame


def export_scene_data(json_path="tree_data.json"):
    """
    Exports static scene structure and animation parameters to JSON for the web app.
    """
    scene = build_static_scene()
    data = {
        "width": WIDTH,
        "height": HEIGHT,
        "build_duration": 16.0,
        "cells": []
    }
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(scene[y][x].to_dict())
        data["cells"].append(row)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Exported scene data to {json_path} ({os.path.getsize(json_path)} bytes)")


if __name__ == "__main__":
    export_scene_data()
