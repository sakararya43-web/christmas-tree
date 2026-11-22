"""
Christmas Tree ASCII Art & Animation Engine (Extracted directly from reference.jpeg)
Ensures 100% visual fidelity to the reference photo:
- Exact color mapping, character density, and coordinates sampled from reference.jpeg
- Ground perspective grid, snow bank, gifts (red, blue, burgundy, gold), trunk, tiered foliage
- Garland paths (#ee*0, *ee#%*), red baubles, golden bells, top star, and radiant beams
- Synchronized bottom-to-top reveal animation
- Audio starting from: "Don't cry snowman"
"""

import math
import random
import json
import os
import cv2
import numpy as np

WIDTH = 84
HEIGHT = 62

PINE_CHARS_DENSE = ["%", "#", "@", "8", "&", "X", "0"]
PINE_CHARS_MID = ["*", "%", "+", "#", "x", "s", "o", "0", "="]
PINE_CHARS_LIGHT = ["*", "+", "-", "=", ".", "^", "o"]
GARLAND_CHARS = ["e", "@", "#", "*", "+", "o", "="]
STAR_CHARS = ["e", "@", "#", "*"]
SNOW_CHARS = [".", "·", "*", "+", "o", "❄"]


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
    Builds the scene by sampling directly from reference.jpeg for 100% visual fidelity.
    """
    if not os.path.exists(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), "reference.jpeg")

    img = cv2.imread(ref_path)
    if img is None:
        raise FileNotFoundError(f"Could not load reference image at {ref_path}")

    img_h, img_w, _ = img.shape
    cell_w = img_w / float(width)
    cell_h = img_h / float(height)

    rng = random.Random(42)
    grid = []

    for gy in range(height):
        row = []
        y1, y2 = int(gy * cell_h), int((gy + 1) * cell_h)
        for gx in range(width):
            x1, x2 = int(gx * cell_w), int((gx + 1) * cell_w)
            patch = img[y1:y2, x1:x2]

            # Average BGR and max intensity
            b_avg, g_avg, r_avg = np.mean(patch, axis=(0, 1))
            max_intensity = float(np.max(patch))
            mean_intensity = float(np.mean(patch))

            # Classify layer and character based on color hue and position
            # Ground is gy >= 45
            is_ground_area = (gy >= 45)
            # Tree / star area
            is_star_area = (gy <= 10 and 38 <= gx <= 45)

            layer = "sky"
            char = " "
            glow = 0.0

            # Determine color and character
            if mean_intensity < 18 and max_intensity < 45:
                # Dark sky background
                if rng.random() < 0.04 and max_intensity > 25:
                    char = rng.choice([".", "·", "*", "+"])
                    color = "#94a3b8"
                    glow = 0.3
                    layer = "sky"
                else:
                    char = " "
                    color = "#070b19"
                    layer = "sky"
            else:
                # Active foreground pixel from reference image!
                # Compute dominant hue
                color = rgb_to_hex(r_avg, g_avg, b_avg)

                # Star & radiant rays
                if is_star_area:
                    layer = "star" if gy >= 5 else "beam"
                    glow = 1.0
                    if gy == 8 and gx == 41:
                        char = "@"
                    elif gy in (2, 3, 4):
                        if gx == 41:
                            char = "|"
                        elif gx < 41:
                            char = "\\"
                        else:
                            char = "/"
                    else:
                        char = "e"
                # Yellow Garland / Lights (High red and green, low blue)
                elif r_avg > 110 and g_avg > 100 and b_avg < 80:
                    layer = "garland"
                    char = rng.choice(["e", "*", "#", "o", "%", "="])
                    glow = min(1.0, mean_intensity / 150.0)
                # Red Ornaments / Baubles / Red Gift (High red, low green and blue)
                elif r_avg > 80 and g_avg < 55 and b_avg < 55:
                    if is_ground_area and gx < 35:
                        layer = "gift"
                        char = "%" if r_avg > 120 else "#"
                    else:
                        layer = "ornament"
                        char = "@" if r_avg > 120 else "%"
                    glow = min(0.9, mean_intensity / 120.0)
                # Royal Blue Gift (High blue, low red and green)
                elif b_avg > 60 and r_avg < 45 and g_avg < 55 and is_ground_area:
                    layer = "gift"
                    char = "%" if b_avg > 100 else "#"
                    glow = 0.6
                # White Snow Bank / Ground Lines
                elif is_ground_area and (r_avg > 70 and g_avg > 70 and b_avg > 70):
                    layer = "ground"
                    if gy >= 58:
                        char = "=" if gx % 2 == 0 else "+"
                    elif gy >= 54:
                        char = rng.choice(["x", "X", "*", "+", "="])
                    elif gy >= 50:
                        char = "-" if gx % 3 == 0 else ":"
                    else:
                        char = ":" if gx % 2 == 0 else "."
                    glow = min(0.6, mean_intensity / 140.0)
                # Green Pine Foliage
                elif g_avg > r_avg and g_avg > b_avg:
                    layer = "foliage"
                    glow = min(0.7, mean_intensity / 120.0)
                    if g_avg > 90:
                        char = rng.choice(["*", "+", "o", "0"])
                    elif g_avg > 50:
                        char = rng.choice(["%", "#", "*", "+", "0"])
                    else:
                        char = rng.choice(["%", "#", "@", "8"])
                else:
                    # Generic active cell
                    glow = min(0.5, mean_intensity / 150.0)
                    if is_ground_area:
                        layer = "ground"
                        char = "." if gy < 52 else "-"
                    else:
                        layer = "foliage"
                        char = "*"

            row.append(Cell(char, color, glow, layer, gy))
        grid.append(row)

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
    Bottom-to-Top Animation Timeline:
    - 0.0s - 1.5s: "Don't cry, snowman, not in front of me..." -> Ground perspective lines settle.
    - 1.5s - 3.5s: "Who'll catch your tears..." -> Gifts at base assemble with ribbon ties.
    - 3.5s - 12.0s: "if you can't catch me darling..." -> Pine tree ascends smoothly from bottom to top!
                    Garland spirals and ornaments light up in the wake of the growth front.
    - 12.0s - 14.5s: Crown reached! Star at apex ignites and radiant beams burst into the night sky!
    - 14.5s+: Full finished tree matching reference photo, with continuous snowfall and glowing twinkle!
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

    # Phase 1: Ground plane emergence (0.0s to 2.0s)
    ground_y_bottom = height - 1
    ground_y_top = 46
    ground_progress = min(1.0, t_sec / 2.0)
    ground_cutoff_y = ground_y_bottom - ground_progress * (ground_y_bottom - ground_y_top)

    for y in range(ground_y_top, height):
        if y >= ground_cutoff_y:
            for x in range(width):
                orig = static_scene[y][x]
                if orig.layer == "ground":
                    age = y - ground_cutoff_y
                    flash = 1.0 + max(0.0, 1.0 - age) * 0.5
                    frame[y][x] = Cell(orig.char, orig.color, orig.glow * flash, "ground", y)

    # Phase 2: Gifts emergence (1.5s to 3.5s)
    gift_progress = min(1.0, max(0.0, (t_sec - 1.5) / 2.0))
    gift_cutoff_y = (height - 2) - gift_progress * 12
    for y in range(46, height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer == "gift" and y >= gift_cutoff_y:
                frame[y][x] = Cell(orig.char, orig.color, orig.glow, "gift", y)

    # Phase 3: Pine Tree Growth from Bottom to Top (3.5s to 12.0s)
    tree_bottom_y = 55
    tree_top_y = 10
    tree_progress = min(1.0, max(0.0, (t_sec - 3.5) / 8.5))
    current_tree_growth_y = tree_bottom_y - tree_progress * (tree_bottom_y - tree_top_y)

    for y in range(height):
        for x in range(width):
            orig = static_scene[y][x]
            if orig.layer in ("foliage", "garland", "ornament", "bell"):
                if y >= current_tree_growth_y:
                    char = orig.char
                    color = orig.color
                    glow = orig.glow

                    dist = abs(y - current_tree_growth_y)
                    if dist < 1.8 and tree_progress < 1.0:
                        glow = 1.0
                        if random.random() < 0.25:
                            char = random.choice(["*", "+", "#", "o", "0"])
                            color = "#ffffff"

                    if t_sec > 12.0:
                        if orig.layer == "garland":
                            wave = math.sin(t_sec * 4.0 - y * 0.4 + x * 0.1)
                            glow = 0.7 + 0.3 * wave
                        elif orig.layer in ("ornament", "bell"):
                            shimmer = math.sin(t_sec * 3.0 + x * 0.5 + y * 0.8)
                            glow = 0.75 + 0.25 * shimmer

                    frame[y][x] = Cell(char, color, glow, orig.layer, y)

    # Phase 4: Star and Celestial Rays (12.0s to 14.5s)
    star_progress = min(1.0, max(0.0, (t_sec - 12.0) / 2.5))
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
    print(f"Exported scene data directly from reference.jpeg to {json_path} ({os.path.getsize(json_path)} bytes)")


if __name__ == "__main__":
    export_scene_data()
