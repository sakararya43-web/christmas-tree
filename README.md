# 🎄 Festive Christmas Tree ASCII Animation

> A nostalgic, glowing ASCII art Christmas tree animation with bottom-to-top growth, white pixelated snowfall, bells, wrapped gifts, and synchronized to **"Snowman" by Sia**.

[![Deploy to GitHub Pages](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml/badge.svg)](https://github.com/sakararya43-web/christmas-tree/actions/workflows/deploy.yml)
**Live Demo on GitHub Pages**: [https://sakararya43-web.github.io/christmas-tree/](https://sakararya43-web.github.io/christmas-tree/)

---

## ✨ Features

- **Bottom-to-Top Assembly (16+ Seconds)**:
  - **Phase 1 (0.0s - 1.5s)**: Quiet starry sky with gentle drifting snowfall.
  - **Phase 2 (1.5s - 3.5s)**: Perspective ground plane lines settle and frost over.
  - **Phase 3 (3.5s - 5.5s)**: Red & blue gift boxes assemble at the base with ribbons and bow ties.
  - **Phase 4 (5.5s - 13.5s)**: Pine tree trunk emerges, and emerald foliage sweeps upward layer by layer. Golden garlands ignite along spiraling paths, and red baubles & golden bells chime into place.
  - **Phase 5 (13.5s - 15.5s)**: Crown reached! The golden star takes form, flares up, and radiant celestial beams (`\`, `|`, `/`, `-`) burst into the night sky!
  - **Phase 6 (15.5s+ Celebration)**: Garland lights ripple in rhythm with the music, bells glint, the star gently breathes, and snow continues falling.
- **Bells, Gifts & Ornaments**:
  - Detailed wrapped gifts with ribbons and bows at the base.
  - Golden hanging bells and vibrant crimson baubles.
- **Pixelated Snowfall & Starry Sky**:
  - White ASCII snowflakes (`*`, `·`, `.`, `+`, `o`, `❄`) with dynamic drifting and sway physics.
- **Music Soundtrack**:
  - Synchronized with **"Snowman" by Sia**.
- **Python-Powered**:
  - Generative mathematical model (`tree_builder.py`).
  - Terminal console player (`main.py`) with ANSI truecolor and audio via Pygame.
  - HD video renderer (`render_video.py`) generating `christmas_tree.mp4` with FFmpeg.
- **Web App (GitHub Pages)**:
  - Interactive Canvas engine with CRT bloom and scanlines.
  - Mode toggle: Switch between live interactive ASCII Canvas and Python-rendered HD video.
  - Interactive click sparkles: Tap/click anywhere to scatter glowing holiday embers!
  - Audio playback controls with autoplay safety and volume slider.

---

## 🚀 Running Locally with Python

### 1. Requirements
Ensure you have Python 3.10+ installed with the following packages:
```bash
pip install pygame colorama pillow
```

### 2. Run the Terminal Animation
Enjoy the glowing ASCII animation with music directly in your console:
```bash
python main.py
```

### 3. Re-render the High-Definition MP4 Video
To render a new HD video (`christmas_tree.mp4`) with Python and FFmpeg:
```bash
python render_video.py
```

---

## 🌐 GitHub Pages Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys the web app to GitHub Pages.

To access the live web app:
👉 **[https://sakararya43-web.github.io/christmas-tree/](https://sakararya43-web.github.io/christmas-tree/)**

If GitHub Pages is not yet enabled on the repo, go to:
1. **GitHub Repository Settings** -> **Pages**
2. Under **Build and deployment** > **Source**, select **GitHub Actions** (or select **Deploy from a branch** -> branch `main` -> folder `/ (root)`).

---

## 🎵 Music Credits
- **Song**: *"Snowman"*
- **Artist**: Sia
- **Album**: *Everyday Is Christmas*

---

*Merry Christmas and Happy Holidays!* 🎄❄️✨
