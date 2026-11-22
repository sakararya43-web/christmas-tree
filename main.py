#!/usr/bin/env python3
"""
Festive Christmas Tree Animation in Terminal
Features:
- Bottom-to-top progressive growth animation (16 seconds)
- Authentic ASCII character rendering matching reference.jpeg
- Bells, gifts with ribbons, and golden spiraling garlands
- White pixelated snowfall with dynamic drifting physics
- Plays "Snowman" by Sia via pygame.mixer
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

# Initialize colorama for Windows ANSI support
colorama.init()


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))


def play_audio(audio_path):
    """Attempts to play Sia - Snowman using pygame.mixer."""
    try:
        import pygame

        pygame.mixer.init()
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(-1)
            return True
    except Exception as e:
        return False
    return False


def render_to_terminal(frame, terminal_width, terminal_height):
    """
    Renders the frame to the terminal with ANSI truecolor and centering.
    """
    pad_left = max(0, (terminal_width - WIDTH) // 2)
    pad_str = " " * pad_left

    output_lines = []
    # Hide cursor and move to home position
    output_lines.append("\033[?25l\033[H")

    # Header banner
    title = "❄  MERRY CHRISTMAS  ❄  [ Sia - Snowman ]"
    title_pad = max(0, (terminal_width - len(title)) // 2)
    output_lines.append(" " * title_pad + "\033[38;2;254;240;138;1m" + title + "\033[0m\n")

    for row in frame:
        line_parts = [pad_str]
        current_color = None
        for cell in row:
            r, g, b = hex_to_rgb(cell.color)
            if cell.glow > 0.0:
                # Boost brightness with glow
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

    # Controls footer
    footer = "Press Ctrl+C to exit | Animation grows bottom-to-top | Snowman by Sia"
    footer_pad = max(0, (terminal_width - len(footer)) // 2)
    output_lines.append("\n" + " " * footer_pad + "\033[38;2;148;163;184m" + footer + "\033[0m")

    sys.stdout.write("\n".join(output_lines))
    sys.stdout.flush()


def main():
    # Setup terminal screen
    os.system("cls" if os.name == "nt" else "clear")

    print("\033[?25l")  # Hide cursor
    print("Loading Christmas Tree ASCII Animation...")
    static_scene = build_static_scene(WIDTH, HEIGHT)
    snow = SnowfallSystem(WIDTH, HEIGHT, count=90)

    audio_file = os.path.join(os.path.dirname(__file__), "snowman.mp3")
    music_playing = play_audio(audio_file)

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

            # Update snowfall physics
            snow.update(dt, elapsed)

            # Get animated frame at current timestamp
            frame = get_animated_frame(
                static_scene,
                t_sec=elapsed,
                total_build_duration=build_duration,
                snow_system=snow,
            )

            # Get current terminal dimensions
            term_size = shutil.get_terminal_size((WIDTH + 4, HEIGHT + 4))
            render_to_terminal(frame, term_size.columns, term_size.lines)

            # Cap frame rate
            compute_time = time.time() - now
            sleep_time = max(0.005, frame_duration - compute_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor and terminal color
        print("\033[?25h\033[0m\n")
        try:
            import pygame

            pygame.mixer.music.stop()
        except Exception:
            pass
        print("Merry Christmas and Happy Holidays!")


if __name__ == "__main__":
    main()
