"""
High-Resolution Video Renderer for Christmas Tree ASCII Animation
100% Authentic Visual Artwork matching reference.jpeg:
- Crown star at apex with radiant celestial beams (\\, |, /, -)
- Conical evergreen foliage with tiered pine branches
- Golden spiraling garlands (#ee*0, *ee#%*)
- Ruby red bauble ornaments (@, %) and golden bells
- Wrapped gifts at base (Red box left, Royal Blue box right) and snow mound
- Wide perspective ground grid (...., ::::, ----, ++++, ====)
- White pixelated snowfall physics
- Organic bottom-to-top assembly animation running for >15 seconds (16.0s build + celebration = 18.0s)
- Synchronized to Sia - Snowman starting directly at "Don't cry snowman"
Outputs: christmas_tree.mp4
"""

import os
import sys
import math
import random
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def render_video(output_mp4="christmas_tree.mp4", duration=18.0, fps=24):
    print(f"Initializing HD video render: {duration}s @ {fps} fps ({int(duration * fps)} frames)...")

    ref_path = "reference.jpeg"
    sky_path = "sky_bg.jpg"
    audio_file = "snowman.mp3"
    temp_video = "temp_video.mp4"

    ref_bgr = cv2.imread(ref_path)
    if ref_bgr is None:
        raise FileNotFoundError(f"Cannot load {ref_path}")
    
    # Ensure dimensions are strictly even for H.264 / yuv420p encoding
    w = 1072
    h = 1180
    ref_bgr = cv2.resize(ref_bgr, (w, h), interpolation=cv2.INTER_LANCZOS4)
    ref_rgb = cv2.cvtColor(ref_bgr, cv2.COLOR_BGR2RGB)

    if os.path.exists(sky_path):
        sky_bgr = cv2.imread(sky_path)
        sky_bgr = cv2.resize(sky_bgr, (w, h), interpolation=cv2.INTER_LANCZOS4)
        sky_rgb = cv2.cvtColor(sky_bgr, cv2.COLOR_BGR2RGB)
    else:
        sky_rgb = np.full((h, w, 3), (10, 14, 26), dtype=np.uint8)

    # Precompute coordinate grids
    y_coords, x_coords = np.ogrid[:h, :w]
    cx = w // 2

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
        "19",
        temp_video,
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    total_frames = int(duration * fps)
    dt = 1.0 / fps

    # Snowflake particle physics system
    rng = random.Random(777)
    snowflakes = []
    for _ in range(130):
        snowflakes.append({
            "x": rng.uniform(0, w),
            "y": rng.uniform(0, h),
            "speed": rng.uniform(65, 145),
            "sway_amp": rng.uniform(18, 38),
            "sway_freq": rng.uniform(0.6, 1.8),
            "sway_phase": rng.uniform(0, math.pi * 2),
            "char": rng.choice([".", "·", "*", "+", "o", "❄"]),
            "size": rng.choice([10, 14, 18, 22]),
            "alpha": rng.uniform(0.5, 0.95),
        })

    snow_fonts = {
        s: ImageFont.truetype(font_path, s) for s in [10, 14, 18, 22]
    }

    # Organic reveal animation milestones (total build duration = 16.0s)
    # 0.0s - 2.0s: Starry sky with snowfall (Sia: "Don't cry snowman...")
    # 2.0s - 4.5s: Ground perspective lines reveal from horizon outward
    # 4.5s - 6.5s: Wrapped gift boxes assemble at base with ribbon sparkles
    # 6.5s - 13.8s: Tree ascends organically from bottom to top (7.3s ascent)
    # 13.8s - 15.5s: Crown star ignites at apex, radiating celestial beams
    # 15.5s - 18.0s: Full celebration with pulsing star, twinkling garlands, continuous snowfall

    for frame_idx in range(total_frames):
        t_sec = frame_idx * dt

        # Organic reveal mask (0.0 = sky, 1.0 = reference artwork)
        mask = np.zeros((h, w), dtype=np.float32)

        # 1. Ground: 2.0s to 4.5s (y from 810 to h)
        if t_sec >= 2.0:
            g_prog = min(1.0, (t_sec - 2.0) / 2.5)
            curr_g_y = int(810 + g_prog * (h - 810))
            mask[810:curr_g_y, :] = 1.0

        # 2. Gifts & Snow Mound: 4.5s to 6.5s
        if t_sec >= 4.5:
            gift_prog = min(1.0, (t_sec - 4.5) / 2.0)
            gift_area = (y_coords >= 960) & (y_coords <= 1130) & (
                ((x_coords >= 190) & (x_coords <= 400)) |  # Red gift box left
                ((x_coords >= 690) & (x_coords <= 910)) |  # Blue gift box right
                ((x_coords >= 400) & (x_coords <= 690) & (y_coords >= 1020))  # Snow bank center
            )
            mask[gift_area] = np.maximum(mask[gift_area], gift_prog)

        # 3. Tree Foliage & Garlands: 6.5s to 13.8s (Ascends from y=1040 to y=200)
        curr_tree_y = 1040.0
        tree_prog = 0.0
        if t_sec >= 6.5:
            tree_prog = min(1.0, (t_sec - 6.5) / 7.3)
            curr_tree_y = 1040.0 - tree_prog * (1040.0 - 200.0)

            # Conical pine silhouette
            cone_half_w = 40.0 + (y_coords - 200.0) / 840.0 * 365.0
            in_cone = (np.abs(x_coords - cx) <= (cone_half_w + 18.0)) & (y_coords >= 200) & (y_coords <= 1040)

            # Organic branch-shaped reveal crest (not a flat horizontal box)
            branch_wobble = 14.0 * np.sin(x_coords * 0.05) * np.cos(y_coords * 0.03) + 6.0 * np.sin(x_coords * 0.12)
            revealed_tree = in_cone & (y_coords >= (curr_tree_y + branch_wobble))
            mask[revealed_tree] = 1.0

        # 4. Apex Crown Star & Radiant Beams: 13.8s to 15.5s
        if t_sec >= 13.8:
            star_prog = min(1.0, (t_sec - 13.8) / 1.7)
            # Crown star body (y: 120 to 200, x: cx +- 80)
            crown_area = (y_coords >= 120) & (y_coords <= 200) & (np.abs(x_coords - cx) <= 85)
            mask[crown_area] = np.maximum(mask[crown_area], star_prog)

            # Radiating celestial light beams flaring outward
            if star_prog > 0.35:
                beam_prog = (star_prog - 0.35) / 0.65
                beam_area = (y_coords >= int(200 - beam_prog * 170)) & (y_coords <= 130) & (np.abs(x_coords - cx) <= int(beam_prog * 130))
                mask[beam_area] = np.maximum(mask[beam_area], beam_prog)

        if t_sec >= 15.5:
            # Full 100% faithful reference artwork active
            mask[:] = 1.0

        # Composite reference artwork over starry sky plate
        mask_3ch = np.dstack([mask, mask, mask])
        frame_np = (ref_rgb.astype(np.float32) * mask_3ch + sky_rgb.astype(np.float32) * (1.0 - mask_3ch)).astype(np.uint8)

        # Convert to PIL Image for particle sparkles and snowfall
        frame_pil = Image.fromarray(frame_np)
        f_draw = ImageDraw.Draw(frame_pil)

        # 5. Sparkling particles riding the leading growth edge
        if 0.0 < tree_prog < 1.0:
            half_w = int(40 + tree_prog * 350)
            for _ in range(16):
                sx = rng.randint(cx - half_w, cx + half_w)
                sy = int(curr_tree_y) + rng.randint(-12, 12)
                ch = rng.choice(["*", "+", "#", "o", "0", "e", "✦"])
                col = rng.choice([(254, 240, 138), (34, 197, 94), (255, 255, 255), (250, 204, 21)])
                f_draw.text((sx, sy), ch, font=sparkle_font, fill=col)

        # 6. Star Pulse & Warm Golden Bloom Halo
        if t_sec >= 13.8:
            pulse = 1.0 + 0.15 * math.sin(t_sec * 3.8)
            star_center = (cx, 150)
            halo_radius = int(55 * pulse)
            # Soft radial glow overlay
            glow_surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            g_draw = ImageDraw.Draw(glow_surf)
            g_draw.ellipse(
                [star_center[0] - halo_radius, star_center[1] - halo_radius,
                 star_center[0] + halo_radius, star_center[1] + halo_radius],
                fill=(254, 240, 138, int(28 * pulse))
            )
            frame_pil.paste(Image.alpha_composite(frame_pil.convert("RGBA"), glow_surf).convert("RGB"))
            f_draw = ImageDraw.Draw(frame_pil)

        # 7. White pixelated snowfall physics
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

            alpha_val = int(255 * flake["alpha"])
            f_draw.text(
                (int(flake["x"]), int(flake["y"])),
                flake["char"],
                font=snow_fonts[flake["size"]],
                fill=(alpha_val, alpha_val, alpha_val),
            )

        # Send frame to FFmpeg
        pipe.stdin.write(frame_pil.tobytes())

        if (frame_idx + 1) % 72 == 0 or frame_idx == total_frames - 1:
            print(f"Rendered {frame_idx + 1}/{total_frames} frames ({(frame_idx + 1) / total_frames * 100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()

    # Multiplex audio: Sia - Snowman starting from timestamp 0:06
    if os.path.exists(audio_file):
        print("Multiplexing soundtrack: Sia - Snowman (starting from timestamp 0:06)...")
        mux_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            temp_video,
            "-ss",
            "6.0",
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
        print(f"Finished! Output successfully saved to {output_mp4} ({os.path.getsize(output_mp4)} bytes)")
    else:
        if os.path.exists(temp_video):
            os.rename(temp_video, output_mp4)
        print(f"Finished! Output saved to {output_mp4}")


if __name__ == "__main__":
    render_video(duration=18.0, fps=24)
