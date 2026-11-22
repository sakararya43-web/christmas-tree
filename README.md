# 🎄 Festive Christmas Tree Animation

> An authentic, glowing ASCII art Christmas tree animation with bottom-to-top growth, white pixelated snowfall, bells, wrapped gifts, and synchronized to **"Snowman" by Sia** (starting from *"Don't cry snowman"*).

[![Deploy to GitHub Pages](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml/badge.svg)](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml)
**Live Demo on GitHub Pages**: [https://sakararya43-web.github.io/christmas-tree/](https://sakararya43-web.github.io/christmas-tree/)

---

## ✨ Features

- **100% Visual Fidelity to the Reference Photo**:
  - Sampled and structured directly from the reference image.
  - Deep midnight sky with faint stars.
  - Wide perspective ground plane (`====`, `----+`, `::::`, `....`).
  - Wrapped gifts with ribbons & bows at the base (Red gift on left, Royal Blue gift on right).
  - Tiered pine foliage, golden garland spirals (`#ee*0`, `*ee#%*`), red baubles (`@`, `%`), and golden bells.
  - Golden crown star with radiating celestial light beams (`\`, `|`, `/`, `-`).
- **Bottom-to-Top Assembly Animation (>15 Seconds)**:
  - **0.0s – 1.5s**: Deep starry night with falling snow; Sia opens with *"Don't cry, snowman, not in front of me..."*.
  - **1.5s – 3.5s**: Perspective ground plane lines settle upward across the bottom.
  - **3.5s – 5.5s**: Wrapped gift boxes assemble and tie their bows with shimmering sparkles.
  - **5.5s – 13.5s**: The Christmas tree ascends smoothly from bottom to top; foliage, garland spirals, and ornaments illuminate as a dynamic sparkle crest rides the leading edge.
  - **13.5s – 15.5s**: Crown star ignites at the apex with radiant light beams flaring into space!
  - **15.5s+**: Ongoing celebration with rippling garland lights, breathing star glow, and gentle white pixel snowfall.
- **Pixelated Snowfall**:
  - Swaying ASCII snowflakes (`*`, `·`, `.`, `+`, `o`, `❄`) drifting down across the canvas.
- **Music Soundtrack**:
  - Synchronized with Sia's *"Snowman"* starting cleanly at *"Don't cry snowman"*.
- **Python Engine**:
  - Generative engine [`tree_builder.py`](tree_builder.py).
  - Terminal console player [`main.py`](main.py) with ANSI truecolor.
  - HD video renderer [`render_video.py`](render_video.py) producing [`christmas_tree.mp4`](christmas_tree.mp4).
- **Web App on GitHub Pages**:
  - Interactive Canvas engine with CRT bloom and scanline overlay.
  - Mode switch: Toggle between live interactive Canvas and Python-rendered HD video.
  - Interactive click sparkles: Tap/click anywhere to scatter glowing holiday embers!

---

## 🚀 Running Locally with Python

### 1. Requirements
```bash
pip install pygame-ce colorama pillow opencv-python
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
