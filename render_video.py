"""
High-Resolution Video Renderer for Christmas Tree ASCII Animation
Faithfully matches reference.jpeg with bottom-to-top progressive growth.
Soundtrack: Sia - Snowman starting directly at "Don't cry snowman"
Outputs: christmas_tree.mp4
"""

import os
import sys
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


def render_video(output_mp4="christmas_tree.mp4", duration=18.0, fps=24):
    print(f"Initializing video render: {duration}s @ {fps} fps ({int(duration * fps)} frames)...")

    ref_path = "reference.jpeg"
    sky_path = "sky_bg.jpg"
    audio_file = "snowman.mp3"
    temp_video = "temp_video.mp4"

    ref_img = Image.open(ref_path).convert("RGB")
    w, h = 1072, 1180
    ref_img = ref_img.resize((w, h), Image.Resampling.LANCZOS)

    if os.path.exists(sky_path):
        sky_img = Image.open(sky_path).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    else:
        sky_img = Image.new("RGB", (w, h), (10, 14, 26))

    font_path = "C:/Windows/Fonts/consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/cour.ttf"
    sparkle_font = ImageFont.truetype(font_path, 20)

    if os.path.exists(temp_video):
        try:
            os.remove(temp_video)
        except Exception:
            pass

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{w}x{h}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(fps),
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "ultrafast",
        "-crf",
        "21",
        temp_video,
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    total_frames = int(duration * fps)
    dt = 1.0 / fps

    # Snowflake physics system
    rng = random.Random(999)
    snowflakes = []
    for _ in range(120):
        snowflakes.append({
            "x": rng.uniform(0, w),
            "y": rng.uniform(0, h),
            "speed": rng.uniform(60, 140),
            "sway_amp": rng.uniform(15, 35),
            "sway_freq": rng.uniform(0.6, 1.8),
            "sway_phase": rng.uniform(0, math.pi * 2),
            "char": rng.choice([".", "·", "*", "+", "o", "❄"]),
            "size": rng.choice([10, 14, 18, 22]),
        })

    snow_fonts = {
        s: ImageFont.truetype(font_path, s) for s in [10, 14, 18, 22]
    }

    # Animation milestones
    ground_y_bottom = 1180
    ground_y_top = 820
    tree_y_bottom = 1060
    tree_y_top = 180

    for frame_idx in range(total_frames):
        t_sec = frame_idx * dt

        # Base frame starts with starry night sky
        frame = sky_img.copy()

        # Phase 1: Ground emergence (0.0s to 2.0s)
        ground_prog = min(1.0, t_sec / 2.0)
        curr_ground_y = int(ground_y_bottom - ground_prog * (ground_y_bottom - ground_y_top))

        # Phase 2: Gifts emergence (1.5s to 3.5s)
        # Phase 3: Tree climb (3.5s to 12.5s)
        tree_prog = min(1.0, max(0.0, (t_sec - 3.5) / 9.0))
        curr_tree_y = int(tree_y_bottom - tree_prog * (tree_y_bottom - tree_y_top))

        # Phase 4: Star emergence (12.5s to 14.5s)
        star_prog = min(1.0, max(0.0, (t_sec - 12.5) / 2.0))

        # Composite mask
        mask = Image.new("L", (w, h), 0)
        m_draw = ImageDraw.Draw(mask)

        # Ground mask
        if ground_prog > 0:
            m_draw.rectangle([0, curr_ground_y, w, h], fill=255)

        # Tree mask (reveals upward)
        if tree_prog > 0:
            # Tree region
            m_draw.rectangle([180, curr_tree_y, 890, tree_y_bottom], fill=255)

        # Star mask
        if star_prog > 0:
            star_y_reveal = int(tree_y_top - star_prog * tree_y_top)
            m_draw.rectangle([340, star_y_reveal, 730, tree_y_top + 40], fill=255)

        if t_sec >= 14.5:
            # Full image revealed
            mask = Image.new("L", (w, h), 255)

        # Paste the revealed portion of the authentic reference image
        frame.paste(ref_img, (0, 0), mask)

        f_draw = ImageDraw.Draw(frame)

        # Sparkle particles along leading growth edge
        if 0.0 < tree_prog < 1.0:
            half_w = 20 + int(320 * (tree_prog ** 0.85))
            cx = w // 2
            for _ in range(12):
                sx = rng.randint(cx - half_w, cx + half_w)
                sy = curr_tree_y + rng.randint(-8, 8)
                ch = rng.choice(["*", "+", "#", "o", "0", "e"])
                col = rng.choice([(254, 240, 138), (34, 197, 94), (255, 255, 255), (250, 204, 21)])
                f_draw.text((sx, sy), ch, font=sparkle_font, fill=col)

        # Update and draw snowfall
        for flake in snowflakes:
            flake["y"] += flake["speed"] * dt
            flake["x"] += math.sin(t_sec * flake["sway_freq"] + flake["sway_phase"]) * flake["sway_amp"] * dt
            if flake["y"] >= h:
                flake["y"] = 0
                flake["x"] = random.uniform(0, w)
            if flake["x"] < 0:
                flake["x"] += w
            elif flake["x"] >= w:
                flake["x"] -= w

            f_draw.text(
                (int(flake["x"]), int(flake["y"])),
                flake["char"],
                font=snow_fonts[flake["size"]],
                fill=(255, 255, 255),
            )

        # Push to ffmpeg
        pipe.stdin.write(frame.tobytes())

        if (frame_idx + 1) % 60 == 0 or frame_idx == total_frames - 1:
            print(f"Rendered {frame_idx + 1}/{total_frames} frames ({(frame_idx + 1) / total_frames * 100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()

    # Multiplex audio
    if os.path.exists(audio_file):
        print("Multiplexing audio: Sia - Snowman (starting from 'Don't cry snowman')...")
        mux_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            temp_video,
            "-ss",
            "0",
            "-t",
            str(duration),
            "-i",
            audio_file,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-af",
            f"afade=t=out:st={duration - 1.5}:d=1.5",
            output_mp4,
        ]
        subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(temp_video):
            os.remove(temp_video)
        print(f"Finished! Output saved to {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
    else:
        if os.path.exists(temp_video):
            os.rename(temp_video, output_mp4)
        print(f"Finished! Output saved to {output_mp4}")


if __name__ == "__main__":
    render_video(duration=18.0, fps=24)
