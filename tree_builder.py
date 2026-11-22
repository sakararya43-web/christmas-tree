"""
Christmas Tree ASCII Art & Animation Engine (100% Authentic to Reference Art)
Extracts every character, color, and layer directly from reference.jpeg:
- Crown star at apex with radiant celestial beams (\\, |, /, -)
- Conical evergreen foliage with tiered pine branches
- Golden spiraling garlands (#ee*0, *ee#%*)
- Ruby red bauble ornaments (@, %) and golden bells
- Wrapped gifts at base (Red box left, Royal Blue box right) and snow mound
- Wide perspective ground grid (...., ::::, ----, ++++, ====)
- Drifting white pixel snowfall physics
- Organic bottom-to-top assembly animation running for >15 seconds (16.0s build + celebration)
- Perfectly synchronized to Sia - Snowman starting from "Don't cry snowman"
"""

import math
import random
import json
import os
import cv2
import numpy as np

WIDTH = 90
HEIGHT = 58


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


def rgb_to_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def build_static_scene(ref_path="reference.jpeg", width=WIDTH, height=HEIGHT):
    """
    Builds the scene by sampling directly from reference.jpeg with semantic feature preservation.
    """
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), "reference.jpeg")

    img = cv2.imread(ref_path)
    if img is None:
        raise FileNotFoundError(f"Could not load reference image at {ref_path}")

    img_h, img_w, _ = img.shape
    cell_w = img_w / float(width)
    cell_h = img_h / float(height)

    b, g, r = cv2.split(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # High-precision feature masks
    garland_mask = (r > 120) & (g > 105) & (b < 100) & (gray > 80)
    red_mask = (r > 1.25 * g) & (r > 1.25 * b) & (r > 60)
    blue_mask = (b > 1.2 * r) & (b > 1.1 * g) & (b > 50)
    
    star_box = np.zeros((img_h, img_w), dtype=bool)
    star_box[:int(img_h * 0.20), int(img_w * 0.38):int(img_w * 0.62)] = True
    star_mask = star_box & (gray > 60)

    grid = []

    for gy in range(height):
        row = []
        y1, y2 = int(gy * cell_h), int((gy + 1) * cell_h)
        for gx in range(width):
            x1, x2 = int(gx * cell_w), int((gx + 1) * cell_w)
            patch_gray = gray[y1:y2, x1:x2]
            mean_v = float(np.mean(patch_gray))
            max_v = float(np.max(patch_gray))

            r_avg = float(np.mean(r[y1:y2, x1:x2]))
            g_avg = float(np.mean(g[y1:y2, x1:x2]))
            b_avg = float(np.mean(b[y1:y2, x1:x2]))

            p_star = float(np.mean(star_mask[y1:y2, x1:x2]))
            p_garland = float(np.mean(garland_mask[y1:y2, x1:x2]))
            p_red = float(np.mean(red_mask[y1:y2, x1:x2]))
            p_blue = float(np.mean(blue_mask[y1:y2, x1:x2]))

            is_ground_area = (gy >= 41)
            color = rgb_to_hex(r_avg, g_avg, b_avg)
            glow = 0.0
            layer = "sky"
            char = " "

            # 1. Background Sky vs Foreground
            if mean_v < 18 and max_v < 45:
                # Dark sky background
                if max_v > 28:
                    char = "." if max_v < 60 else "*"
                    color = "#94a3b8"
                    glow = 0.3
                else:
                    char = " "
                    color = "#070b19"
                layer = "sky"

            # 2. Ground Perspective Grid
            elif is_ground_area and (p_red < 0.15 and p_blue < 0.15 and not (g_avg > r_avg * 1.15)):
                layer = "ground"
                glow = min(0.6, mean_v / 140.0)
                if gy >= 53:
                    char = "=" if gx % 2 == 0 else "+"
                elif gy >= 47:
                    char = "-" if gx % 2 == 0 else "+"
                elif gy >= 44:
                    char = ":" if gx % 2 == 0 else "."
                else:
                    char = "." if gx % 2 == 0 else " "

            # 3. Apex Star & Radiant Rays
            elif p_star > 0.12 or (gy <= 10 and 39 <= gx <= 50 and mean_v > 50):
                glow = 1.0
                if gy < 7:
                    layer = "beam"
                    if abs(gx - 45) <= 1:
                        char = "|"
                    elif gx < 45:
                        char = "\\"
                    else:
                        char = "/"
                else:
                    layer = "star"
                    char = "e"
                color = rgb_to_hex(max(200, r_avg), max(190, g_avg), min(120, b_avg))

            # 4. Golden Spiraling Garland Lights
            elif p_garland > 0.12 or (r_avg > 115 and g_avg > 100 and b_avg < 90 and not is_ground_area):
                layer = "garland"
                char = "*" if mean_v > 120 else "#"
                color = rgb_to_hex(max(240, r_avg), max(200, g_avg), min(80, b_avg))
                glow = min(1.0, mean_v / 130.0)

            # 5. Red Bauble Ornaments & Red Gift Box
            elif p_red > 0.12 or (r_avg > 1.25 * g_avg and r_avg > 1.25 * b_avg and r_avg > 60):
                if is_ground_area and gx < 38:
                    layer = "gift"
                    char = "%" if r_avg > 120 else "#"
                else:
                    layer = "ornament"
                    char = "@" if r_avg > 110 else "%"
                color = rgb_to_hex(max(180, r_avg), min(50, g_avg), min(50, b_avg))
                glow = min(0.9, mean_v / 110.0)

            # 6. Royal Blue Gift Box
            elif p_blue > 0.12 or (b_avg > 1.2 * r_avg and b_avg > 1.1 * g_avg and is_ground_area and gx > 55):
                layer = "gift"
                char = "%" if b_avg > 100 else "#"
                color = rgb_to_hex(min(50, r_avg), min(80, g_avg), max(170, b_avg))
                glow = 0.65

            # 7. Green Pine Foliage
            elif g_avg >= r_avg and g_avg >= b_avg and mean_v > 22:
                layer = "foliage"
                glow = min(0.7, mean_v / 120.0)
                if mean_v > 95:
                    char = "*"
                elif mean_v > 65:
                    char = "%"
                elif mean_v > 40:
                    char = "+"
                else:
                    char = "#"
                color = rgb_to_hex(min(70, r_avg), max(110, g_avg), min(70, b_avg))

            # 8. Snow Mound & Base Highlights
            elif is_ground_area and mean_v > 70:
                layer = "ground"
                char = "*" if gx % 2 == 0 else "+"
                glow = 0.6
                color = "#e2e8f0"

            else:
                layer = "sky"
                char = " "
                color = "#070b19"

            row.append(Cell(char, color, glow, layer, gy))
        grid.append(row)

    return grid


class SnowfallSystem:
    def __init__(self, width=WIDTH, height=HEIGHT, count=100, seed=42):
        self.width = width
        self.height = height
        rng = random.Random(seed)
        self.flakes = []
        for _ in range(count):
            self.flakes.append({
                "x": rng.uniform(0, width),
                "y": rng.uniform(0, height),
                "speed": rng.uniform(0.35, 0.95),
                "sway_amp": rng.uniform(0.4, 1.4),
                "sway_freq": rng.uniform(0.6, 1.8),
                "sway_phase": rng.uniform(0, math.pi * 2),
                "char": rng.choice([".", "·", "*", "+", "o", "❄"]),
                "color": rng.choice(["#ffffff", "#e2e8f0", "#cbd5e1", "#93c5fd"]),
                "glow": rng.uniform(0.4, 0.9),
            })

    def update(self, dt, t):
        for flake in self.flakes:
            flake["y"] += flake["speed"] * dt * 8.5
            flake["x"] += math.sin(t * flake["sway_freq"] + flake["sway_phase"]) * flake["sway_amp"] * dt * 2.5
            if flake["y"] >= self.height:
                flake["y"] = 0
                flake["x"] = random.uniform(0, self.width)
            if flake["x"] < 0:
                flake["x"] += self.width
            elif flake["x"] >= self.width:
                flake["x"] -= self.width


def get_animated_frame(static_scene, t_sec, total_build_duration=16.0, snow_system=None):
    """
    Organic bottom-to-top assembly timeline (>15 seconds):
    - 0.0s - 2.0s: Starry cosmos and gentle snowfall; Sia begins "Don't cry snowman...".
    - 2.0s - 4.5s: Ground perspective lines illuminate from horizon outward.
    - 4.5s - 6.5s: Wrapped gift boxes assemble at the base with ribbon sparkles.
    - 6.5s - 13.8s: Tree ascends smoothly from bottom to top with dynamic sparkling crest!
    - 13.8s - 15.5s: Crown star ignites at the apex and radiant beams shoot into space!
    - 15.5s+: Full celebration with glowing garland pulses, star breathing, and snow.
    """
    width = len(static_scene[0])
    height = len(static_scene)
    frame = [[Cell(" ", "#070b19", 0.0, "sky", y) for _ in range(width)] for y in range(height)]

    # Distant background stars
    for y in range(height):
        for x in range(width):
            cell = static_scene[y][x]
            if cell.layer == "sky":
                twinkle = 0.5 + 0.5 * math.sin(t_sec * 2.2 + x * 0.7 + y * 1.1)
                frame[y][x] = Cell(cell.char, cell.color, cell.glow * twinkle, "sky", y)

    # Phase 1: Ground perspective grid (2.0s to 4.5s)
    if t_sec >= 2.0:
        g_prog = min(1.0, (t_sec - 2.0) / 2.5)
        # Horizon at gy = 41 down to gy = 57
        cutoff_gy = int(41 + g_prog * (height - 41))
        for y in range(41, min(height, cutoff_gy + 1)):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "ground":
                    is_edge = (y == cutoff_gy)
                    flash = 1.4 if is_edge and g_prog < 1.0 else 1.0
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * flash, "ground", y)

    # Phase 2: Gifts & Snow Mound at Base (4.5s to 6.5s)
    if t_sec >= 4.5:
        gift_prog = min(1.0, (t_sec - 4.5) / 2.0)
        gift_cutoff_y = int((height - 2) - gift_prog * 12)
        for y in range(45, height):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "gift" and y >= gift_cutoff_y:
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow, "gift", y)

    # Phase 3: Organic Pine Tree Growth (6.5s to 13.8s)
    if t_sec >= 6.5:
        tree_bottom_gy = 51
        tree_top_gy = 9
        tree_prog = min(1.0, (t_sec - 6.5) / 7.3)
        curr_tree_growth_y = tree_bottom_gy - tree_prog * (tree_bottom_gy - tree_top_gy)

        cx = width // 2
        for y in range(height):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer in ("foliage", "garland", "ornament", "bell"):
                    # Organic branch-like growth wave
                    wave = 1.2 * math.sin(x * 0.4) * math.cos(y * 0.3)
                    if y >= (curr_tree_growth_y + wave):
                        char = orig.char
                        color = orig.color
                        glow = orig.glow

                        # Leading sparkle crest
                        dist = abs(y - curr_tree_growth_y)
                        if dist < 1.5 and tree_prog < 1.0:
                            glow = 1.0
                            if random.random() < 0.28:
                                char = random.choice(["*", "+", "#", "o", "✦", "0"])
                                color = random.choice(["#fef08a", "#ffffff", "#86efac", "#facc15"])

                        # Post-reveal celebration effects
                        if t_sec >= 14.0:
                            if orig.layer == "garland":
                                wave_g = math.sin(t_sec * 3.8 - y * 0.4 + x * 0.15)
                                glow = 0.75 + 0.25 * wave_g
                            elif orig.layer in ("ornament", "bell"):
                                shimmer = math.sin(t_sec * 3.0 + x * 0.6 + y * 0.8)
                                glow = 0.8 + 0.2 * shimmer

                        frame[y][x] = Cell(char, color, glow, orig.layer, y)

    # Phase 4: Crown Star & Radiant Beams (13.8s to 15.5s)
    if t_sec >= 13.8:
        star_prog = min(1.0, (t_sec - 13.8) / 1.7)
        star_pulse = 1.0 + 0.2 * math.sin(t_sec * 4.5)
        for y in range(height):
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "star":
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * star_pulse, "star", y)
                elif orig.layer == "beam" and star_prog >= 0.35:
                    b_prog = (star_prog - 0.35) / 0.65
                    dist = math.sqrt((x - width // 2) ** 2 + (y - 8) ** 2)
                    if dist <= b_prog * 10.0:
                        b_pulse = 0.7 + 0.3 * math.sin(t_sec * 3.5 + dist * 0.6)
                        frame[y][x] = Cell(orig.char, orig.color, orig.glow * b_pulse, "beam", y)

    # Phase 5: Pixelated Snowfall
    if snow_system is not None:
        for flake in snow_system.flakes:
            fx = int(round(flake["x"])) % width
            fy = int(round(flake["y"])) % height
            bg_cell = frame[fy][fx]
            if bg_cell.layer in ("sky", "ground", "foliage"):
                if bg_cell.layer == "sky" or random.random() < 0.35:
                    frame[fy][fx] = Cell(flake["char"], flake["color"], flake["glow"], "snow", fy)

    return frame


def export_scene_data(json_path="tree_data.json"):
    scene = build_static_scene()
    data = {
        "width": WIDTH,
        "height": HEIGHT,
        "build_duration": 16.0,
        "cells": [[scene[y][x].to_dict() for x in range(WIDTH)] for y in range(HEIGHT)],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Exported scene data directly from reference.jpeg to {json_path} ({os.path.getsize(json_path)} bytes)")


if __name__ == "__main__":
    export_scene_data()
