#!/usr/bin/env python3
"""
Festive Christmas Tree Animation in Terminal
Synchronized to Sia - Snowman (Chorus Main Part):
"I want you to know that I'm never leaving..."
Features:
- Bottom-to-top progressive growth animation matching reference photo
- Ground perspective grid, snow bank, wrapped gifts, pine foliage, bells & ornaments
- Golden crown star with radiant light beams igniting at the vocal drop
- White pixelated snowfall with dynamic physics
- Plays "Snowman" by Sia via pygame.mixer starting directly at the chorus
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

    # Header banner with synced lyrics
    if elapsed < 1.5:
        lyric = "🎶 'I want you to know that I'm never leaving...'"
    elif elapsed < 3.0:
        lyric = "🎶 ''Cause I'm Mrs. Snow, 'til death we'll be freezing...'"
    elif elapsed < 6.0:
        lyric = "🎶 'Yeah, you are my home, my home for all seasons...'"
    elif elapsed < 9.5:
        lyric = "🎶 'So come on, let's go...'"
    elif elapsed < 12.0:
        lyric = "⭐ 'Let's go below zero and hide from the sun!' ⭐"
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

    footer = "Press Ctrl+C to exit | Bottom-to-Top Growth Synced with Chorus"
    footer_pad = max(0, (terminal_width - len(footer)) // 2)
    output_lines.append("\n" + " " * footer_pad + "\033[38;2;148;163;184m" + footer + "\033[0m")

    sys.stdout.write("\n".join(output_lines))
    sys.stdout.flush()


def main():
    os.system("cls" if os.name == "nt" else "clear")

    print("\033[?25l")
    print("Loading Christmas Tree Animation (Sia - Snowman Main Chorus)...")
    static_scene = build_static_scene(WIDTH, HEIGHT)
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
