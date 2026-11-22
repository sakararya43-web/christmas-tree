"""
High-Resolution Video Renderer for Christmas Tree ASCII Animation
Renders the animation using PIL + FFmpeg with:
- Monospace font Consolas
- True phosphor bloom and character glow
- White pixelated snowfall
- Bottom-to-top progressive growth (18 seconds)
- Synchronized Sia - Snowman audio track
- Outputs christmas_tree.mp4
"""

import os
import sys
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont
from tree_builder import (
    build_static_scene,
    get_animated_frame,
    SnowfallSystem,
    WIDTH,
    HEIGHT,
)


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def render_video(output_mp4="christmas_tree.mp4", duration=18.0, fps=24):
    print(f"Initializing video render: {duration}s @ {fps} fps ({int(duration * fps)} frames)...")

    # Dimensions
    font_size = 18
    font_path = "C:/Windows/Fonts/consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/cour.ttf"

    font = ImageFont.truetype(font_path, font_size)

    # Character spacing
    char_w = 11
    char_h = 18

    margin_x = 25
    margin_y = 30

    canvas_w = WIDTH * char_w + margin_x * 2  # 84 * 11 + 50 = 974
    canvas_h = HEIGHT * char_h + margin_y * 2  # 62 * 18 + 60 = 1176

    # Ensure even dimensions for H.264
    if canvas_w % 2 != 0:
        canvas_w += 1
    if canvas_h % 2 != 0:
        canvas_h += 1

    print(f"Canvas resolution: {canvas_w}x{canvas_h}")

    static_scene = build_static_scene(WIDTH, HEIGHT)
    snow = SnowfallSystem(WIDTH, HEIGHT, count=90)

    audio_file = "snowman.mp3"
    temp_video = "temp_video.mp4"
    if os.path.exists(temp_video):
        try:
            os.remove(temp_video)
        except Exception:
            pass

    # FFmpeg command: stderr=DEVNULL prevents pipe buffer deadlocks on Windows
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{canvas_w}x{canvas_h}",
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
        "22",
        temp_video,
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    total_frames = int(duration * fps)
    dt = 1.0 / fps

    bg_color = (7, 11, 25)  # Dark navy #070b19

    for frame_idx in range(total_frames):
        t_sec = frame_idx * dt
        snow.update(dt, t_sec)

        # Build animated frame
        frame_grid = get_animated_frame(
            static_scene,
            t_sec=t_sec,
            total_build_duration=16.0,
            snow_system=snow,
        )

        # Create image
        img = Image.new("RGB", (canvas_w, canvas_h), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Draw characters
        for row_idx, row in enumerate(frame_grid):
            py = margin_y + row_idx * char_h
            for col_idx, cell in enumerate(row):
                if cell.char == " ":
                    continue
                px = margin_x + col_idx * char_w
                r, g, b = hex_to_rgb(cell.color)

                if cell.glow > 0.0:
                    boost = 1.0 + cell.glow * 0.35
                    r = min(255, int(r * boost))
                    g = min(255, int(g * boost))
                    b = min(255, int(b * boost))

                # Draw character
                draw.text((px, py), cell.char, font=font, fill=(r, g, b))

        # Push raw bytes to ffmpeg
        pipe.stdin.write(img.tobytes())

        if (frame_idx + 1) % 50 == 0 or frame_idx == total_frames - 1:
            print(f"Rendered {frame_idx + 1}/{total_frames} frames ({(frame_idx + 1) / total_frames * 100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()

    # Multiplex with audio if snowman.mp3 exists
    if os.path.exists(audio_file):
        print("Multiplexing audio (Sia - Snowman)...")
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
        print(f"Finished (no audio)! Output saved to {output_mp4}")


if __name__ == "__main__":
    render_video(duration=18.0, fps=24)
