# 🎄 Festive Christmas Tree ASCII Animation

> An authentic, glowing ASCII art Christmas tree animation with 100% visual fidelity to the reference artwork, organic bottom-to-top assembly running for **at least 15 seconds** (16.0s build + celebration), white pixelated snowfall, bells, wrapped gifts, and synchronized to **"Snowman" by Sia** (starting from *"Don't cry snowman"*).

[![Deploy to GitHub Pages](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml/badge.svg)](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml)
**Live Demo on GitHub Pages**: [https://sakararya43-web.github.io/christmas-tree/](https://sakararya43-web.github.io/christmas-tree/)

---

## ✨ Features

- **100% Visual Fidelity to the Reference Artwork**:
  - Sampled and structured directly from the authentic reference photo.
  - Deep midnight cosmic sky with distant twinkling stars.
  - Wide perspective ground plane grid (`====`, `++++`, `----`, `::::`, `....`).
  - Wrapped gift boxes with ribbons & bows at the base (Crimson Red box on left, Royal Blue box on right) and snow mound.
  - Conical pine foliage, golden spiraling garland paths (`#ee*0`, `*ee#%*`), ruby red baubles (`@`, `%`), and golden bells.
  - Golden crown star with radiating celestial light beams (`\`, `|`, `/`, `-`).
- **Organic Bottom-to-Top Assembly Animation (>15 Seconds)**:
  - **0.0s – 2.0s**: Quiet cosmic night with drifting snowfall; Sia opens with *"Don't cry, snowman, not in front of me..."*.
  - **2.0s – 4.5s**: Wide perspective ground plane lines reveal smoothly from the horizon down to the foreground.
  - **4.5s – 6.5s**: Wrapped gift boxes assemble and tie their bows with shimmering sparkles at the base.
  - **6.5s – 13.8s**: The Christmas tree ascends smoothly from bottom to top; foliage, garland spirals, and ornaments illuminate as a dynamic sparkle crest rides the leading edge.
  - **13.8s – 15.5s**: Crown star takes shape and ignites at the apex with radiant celestial light beams flaring into space!
  - **15.5s – 18.0s+**: Full festive celebration with breathing golden star halo, rippling garland lights, shimmering baubles, and continuous white pixel snowfall.
- **Pixelated Snowfall Physics**:
  - Swaying ASCII snowflakes (`*`, `·`, `.`, `+`, `o`, `❄`) drifting down across the canvas with realistic physics.
- **Synchronized Soundtrack**:
  - Sia's *"Snowman"* starting cleanly at *"Don't cry snowman"*.
- **Multi-Platform Support**:
  - **Python Terminal Engine**: [`tree_builder.py`](tree_builder.py) + [`main.py`](main.py) with ANSI truecolor glow.
  - **HD Video Renderer**: [`render_video.py`](render_video.py) producing [`christmas_tree.mp4`](christmas_tree.mp4) (18s @ 24fps).
  - **Web App on GitHub Pages**: Interactive Canvas engine with CRT bloom, interactive click sparkles, and mode switch.

---

## 🚀 Running Locally with Python

### 1. Requirements
```bash
pip install pygame-ce colorama pillow opencv-python numpy
```

### 2. Run Terminal Animation
```bash
python main.py
```

### 3. Re-render HD Video
```bash
python render_video.py
```

---

## 🌐 GitHub Pages Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) and pushes to both `main` and `gh-pages` branches for instant deployment.

👉 **[https://sakararya43-web.github.io/christmas-tree/](https://sakararya43-web.github.io/christmas-tree/)**

---

## 🎵 Music Credits
- **Song**: *"Snowman"*
- **Artist**: Sia
- **Opening Lyric**: *"Don't cry, snowman, not in front of me..."*

---

*Merry Christmas and Happy Holidays!* 🎄❄️✨
