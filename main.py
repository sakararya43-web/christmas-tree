#!/usr/bin/env python3
"""
Festive Christmas Tree Animation in Terminal
Directly sampled from reference.jpeg for 100% visual fidelity!
Synchronized to Sia - Snowman starting from:
"Don't cry, snowman, not in front of me..."
Features:
- Progressive bottom-to-top growth animation
- Perspective ground lines, wrapped gifts, pine foliage, bells & ornaments
- Crown star with radiant beams igniting at the apex
- White pixelated snowfall physics
- Background audio via pygame.mixer
- ANSI Truecolor terminal output for vibrant retro neon glow
"""

import sys
import time
import math
import os
import shutil
import colorama
from tree_builder import (
    build_static_scene,
    get_animated_frame,
    SnowfallSystem,
    WIDTH,
    HEIGHT,
)

colorama.init()


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def play_audio(audio_path):
    try:
        import pygame

        pygame.mixer.init()
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(-1)
            return True
    except Exception:
        return False
    return False


def render_to_terminal(frame, terminal_width, terminal_height, elapsed):
    pad_left = max(0, (terminal_width - WIDTH) // 2)
    pad_str = " " * pad_left

    output_lines = []
    output_lines.append("\033[?25l\033[H")

    # Header banner with synced lyrics starting from "Don't cry snowman"
    if elapsed < 2.0:
        lyric = "🎶 'Don't cry, snowman, not in front of me...'"
    elif elapsed < 4.0:
        lyric = "🎶 'Who'll catch your tears if you can't catch me, darling...'"
    elif elapsed < 8.0:
        lyric = "🌲 'If you can't catch me, darling...' [Tree Ascending]"
    elif elapsed < 12.0:
        lyric = "✨ 'Don't cry, snowman, don't leave me this way...'"
    elif elapsed < 14.5:
        lyric = "⭐ 'A puddle of water can't hold me close, baby!' ⭐"
    else:
        lyric = "❄  MERRY CHRISTMAS  ❄  [ Sia - Snowman ]"

    title_pad = max(0, (terminal_width - len(lyric)) // 2)
    output_lines.append(" " * title_pad + "\033[38;2;254;240;138;1m" + lyric + "\033[0m\n")

    for row in frame:
        line_parts = [pad_str]
        current_color = None
        for cell in row:
            r, g, b = hex_to_rgb(cell.color)
            if cell.glow > 0.0:
                factor = 1.0 + cell.glow * 0.35
                r = min(255, int(r * factor))
                g = min(255, int(g * factor))
                b = min(255, int(b * factor))

            ansi_color = f"\033[38;2;{r};{g};{b}m"
            if ansi_color != current_color:
                line_parts.append(ansi_color)
                current_color = ansi_color

            line_parts.append(cell.char)

        line_parts.append("\033[0m")
        output_lines.append("".join(line_parts))

    footer = "Press Ctrl+C to exit | Bottom-to-Top Growth | Sia - Snowman"
    footer_pad = max(0, (terminal_width - len(footer)) // 2)
    output_lines.append("\n" + " " * footer_pad + "\033[38;2;148;163;184m" + footer + "\033[0m")

    sys.stdout.write("\n".join(output_lines))
    sys.stdout.flush()


def main():
    os.system("cls" if os.name == "nt" else "clear")

    print("\033[?25l")
    print("Loading Christmas Tree Animation (Sia - Snowman)...")
    static_scene = build_static_scene()
    snow = SnowfallSystem(WIDTH, HEIGHT, count=90)

    audio_file = os.path.join(os.path.dirname(__file__), "snowman.mp3")
    play_audio(audio_file)

    target_fps = 24
    frame_duration = 1.0 / target_fps
    build_duration = 16.0

    start_time = time.time()
    last_time = start_time

    try:
        while True:
            now = time.time()
            dt = now - last_time
            last_time = now
            elapsed = now - start_time

            snow.update(dt, elapsed)

            frame = get_animated_frame(
                static_scene,
                t_sec=elapsed,
                total_build_duration=build_duration,
                snow_system=snow,
            )

            term_size = shutil.get_terminal_size((WIDTH + 4, HEIGHT + 4))
            render_to_terminal(frame, term_size.columns, term_size.lines, elapsed)

            compute_time = time.time() - now
            sleep_time = max(0.005, frame_duration - compute_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h\033[0m\n")
        try:
            import pygame

            pygame.mixer.music.stop()
        except Exception:
            pass
        print("Merry Christmas and Happy Holidays!")


if __name__ == "__main__":
    main()
