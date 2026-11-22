/**
 * Christmas Tree ASCII Animation & Web Engine
 * Inspired by reference ASCII art with bottom-to-top growth animation,
 * white pixelated snowfall, bells, gifts, and Sia - Snowman soundtrack.
 */

(function () {
  'use strict';

  // Constants & Scene Grid Dimensions
  const COLS = 84;
  const ROWS = 62;
  const TOTAL_BUILD_DURATION = 16.0; // Seconds for bottom-to-top assembly

  // Character palettes matching reference
  const PINE_CHARS_DENSE = ['%', '#', '@', '8', '&', 'X'];
  const PINE_CHARS_MID = ['*', '%', '+', '#', 'x', 's', 'o'];
  const PINE_CHARS_LIGHT = ['*', '+', '-', '=', '.', '^', '~'];
  const GARLAND_CHARS = ['e', '@', '#', '*', '+', 'o', '=', '%'];
  const STAR_CHARS = ['e', '@', '#', '*'];
  const SNOW_CHARS = ['.', '·', '*', '+', 'o', '❄'];

  // Colors
  const COLOR_PINE_DEEP = '#0f3e1a';
  const COLOR_PINE_MID = '#166534';
  const COLOR_PINE_BRIGHT = '#22c55e';
  const COLOR_PINE_TIP = '#4ade80';
  const COLOR_PINE_HIGHLIGHT = '#86efac';

  const COLOR_GARLAND_GOLD = '#facc15';
  const COLOR_GARLAND_BRIGHT = '#fef08a';
  const COLOR_GARLAND_WARM = '#eab308';

  const COLOR_ORNAMENT_RED = '#ef4444';
  const COLOR_ORNAMENT_DARK_RED = '#b91c1c';
  const COLOR_ORNAMENT_SHINE = '#fca5a5';

  const COLOR_BELL_GOLD = '#fde047';
  const COLOR_STAR_CORE = '#ffffff';
  const COLOR_STAR_GOLD = '#fef08a';
  const COLOR_STAR_BEAM = '#fde047';

  const COLOR_GIFT_RED = '#dc2626';
  const COLOR_GIFT_DARK_RED = '#991b1b';
  const COLOR_GIFT_BLUE = '#2563eb';
  const COLOR_GIFT_DARK_BLUE = '#1e3a8a';
  const COLOR_GIFT_RIBBON_GOLD = '#fde047';
  const COLOR_GIFT_RIBBON_CYAN = '#38bdf8';

  // DOM Elements
  const treeCanvas = document.getElementById('tree-canvas');
  const treeCtx = treeCanvas.getContext('2d');
  const skyCanvas = document.getElementById('sky-canvas');
  const skyCtx = skyCanvas.getContext('2d');

  const bgAudio = document.getElementById('bg-audio');
  const audioPrompt = document.getElementById('audio-prompt');
  const btnStart = document.getElementById('btn-start');
  const btnPlayPause = document.getElementById('btn-play-pause');
  const playPauseIcon = document.getElementById('play-pause-icon');
  const playPauseText = document.getElementById('play-pause-text');
  const btnRestart = document.getElementById('btn-restart');
  const btnMute = document.getElementById('btn-mute');
  const muteIcon = document.getElementById('mute-icon');
  const volSlider = document.getElementById('volume-slider');
  const btnBloom = document.getElementById('btn-bloom');
  const btnFullscreen = document.getElementById('btn-fullscreen');
  const btnToggleView = document.getElementById('btn-toggle-view');
  const viewIcon = document.getElementById('view-icon');
  const viewLabel = document.getElementById('view-label');
  const crtOverlay = document.getElementById('crt-overlay');
  const videoContainer = document.getElementById('video-container');
  const hdVideo = document.getElementById('hd-video');
  const progressBarWrap = document.getElementById('progress-bar-wrap');
  const progressBar = document.getElementById('progress-bar');
  const progressLabel = document.getElementById('progress-label');
  const unmuteToast = document.getElementById('unmute-toast');
  const toastUnmuteBtn = document.getElementById('toast-unmute-btn');

  // Pseudo-random generator with seed
  function createRng(seed = 42) {
    let s = seed % 2147483647;
    if (s <= 0) s += 2147483646;
    return function () {
      s = (s * 16807) % 2147483647;
      return (s - 1) / 2147483646;
    };
  }

  // Build the complete static scene model
  function buildSceneModel() {
    const rng = createRng(42);
    const grid = [];
    for (let y = 0; y < ROWS; y++) {
      const row = [];
      for (let x = 0; x < COLS; x++) {
        row.push({
          char: ' ',
          color: '#070b19',
          glow: 0.0,
          layer: 'sky',
          y: y
        });
      }
      grid.push(row);
    }

    const centerX = Math.floor(COLS / 2); // 42

    // 1. Sky Stars
    for (let y = 0; y < ROWS; y++) {
      for (let x = 0; x < COLS; x++) {
        if (rng() < 0.038) {
          const starChars = ['.', '·', '+', '*'];
          const starCols = ['#64748b', '#94a3b8', '#cbd5e1', '#e2e8f0', '#93c5fd'];
          grid[y][x] = {
            char: starChars[Math.floor(rng() * starChars.length)],
            color: starCols[Math.floor(rng() * starCols.length)],
            glow: rng() * 0.4,
            layer: 'sky',
            y: y
          };
        }
      }
    }

    // 2. Ground Perspective Plane (Rows 48 to 61)
    const groundTop = 48;
    for (let y = groundTop; y < ROWS; y++) {
      let mainChar, subChar, step, col, glowVal;
      if (y >= ROWS - 3) {
        mainChar = '='; subChar = '+'; step = 2; col = '#64748b'; glowVal = 0.4;
      } else if (y >= ROWS - 7) {
        mainChar = y % 2 === 0 ? '=' : '-'; subChar = y % 2 === 0 ? '+' : ':'; step = 3; col = '#475569'; glowVal = 0.25;
      } else if (y >= ROWS - 11) {
        mainChar = y % 2 === 0 ? '-' : ':'; subChar = y % 2 === 0 ? ':' : '.'; step = 4; col = '#334155'; glowVal = 0.15;
      } else {
        mainChar = y % 2 === 0 ? ':' : '.'; subChar = '.'; step = 5; col = '#1e293b'; glowVal = 0.08;
      }

      for (let x = 0; x < COLS; x++) {
        let ch = (x % step === 0) ? subChar : mainChar;
        let c = (rng() < 0.05) ? '#e2e8f0' : col;
        grid[y][x] = {
          char: ch,
          color: c,
          glow: glowVal,
          layer: 'ground',
          y: y
        };
      }
    }

    // 3. Gifts at the Base
    // Left Red Gift Box: x: 17-29, y: 51-58
    const leftRibbonX = 23;
    const leftRibbonY = 54;
    for (let y = 51; y <= 58; y++) {
      for (let x = 17; x <= 29; x++) {
        if (x === leftRibbonX || y === leftRibbonY) {
          const ch = (x === leftRibbonX && y === leftRibbonY) ? '+' : (x === leftRibbonX ? '|' : '=');
          grid[y][x] = { char: ch, color: COLOR_GIFT_RIBBON_GOLD, glow: 0.75, layer: 'gift', y: y };
        } else {
          const ch = PINE_CHARS_DENSE[Math.floor(rng() * PINE_CHARS_DENSE.length)];
          const c = (x < leftRibbonX) ? COLOR_GIFT_RED : COLOR_GIFT_DARK_RED;
          grid[y][x] = { char: ch, color: c, glow: 0.35, layer: 'gift', y: y };
        }
      }
    }
    // Left Bow
    grid[50][leftRibbonX - 1] = { char: '(', color: COLOR_GIFT_RIBBON_GOLD, glow: 0.8, layer: 'gift', y: 50 };
    grid[50][leftRibbonX]     = { char: 'o', color: COLOR_STAR_CORE, glow: 0.95, layer: 'gift', y: 50 };
    grid[50][leftRibbonX + 1] = { char: ')', color: COLOR_GIFT_RIBBON_GOLD, glow: 0.8, layer: 'gift', y: 50 };

    // Small Burgundy Box (x: 29-35, y: 53-58)
    for (let y = 53; y <= 58; y++) {
      for (let x = 29; x <= 35; x++) {
        if (x === 32 || y === 56) {
          grid[y][x] = { char: '#', color: '#fca5a5', glow: 0.5, layer: 'gift', y: y };
        } else {
          grid[y][x] = { char: '%', color: '#881337', glow: 0.2, layer: 'gift', y: y };
        }
      }
    }

    // Right Blue Gift Box: x: 57-68, y: 51-58
    const rightRibbonX = 62;
    const rightRibbonY = 54;
    for (let y = 51; y <= 58; y++) {
      for (let x = 57; x <= 68; x++) {
        if (x === rightRibbonX || y === rightRibbonY) {
          const ch = (x === rightRibbonX && y === rightRibbonY) ? '+' : (x === rightRibbonX ? '|' : '=');
          grid[y][x] = { char: ch, color: COLOR_GIFT_RIBBON_CYAN, glow: 0.75, layer: 'gift', y: y };
        } else {
          const ch = PINE_CHARS_DENSE[Math.floor(rng() * PINE_CHARS_DENSE.length)];
          const c = (x < rightRibbonX) ? COLOR_GIFT_BLUE : COLOR_GIFT_DARK_BLUE;
          grid[y][x] = { char: ch, color: c, glow: 0.35, layer: 'gift', y: y };
        }
      }
    }
    // Right Bow
    grid[50][rightRibbonX - 1] = { char: '{', color: COLOR_GIFT_RIBBON_CYAN, glow: 0.8, layer: 'gift', y: 50 };
    grid[50][rightRibbonX]     = { char: '*', color: COLOR_STAR_CORE, glow: 0.95, layer: 'gift', y: 50 };
    grid[50][rightRibbonX + 1] = { char: '}', color: COLOR_GIFT_RIBBON_CYAN, glow: 0.8, layer: 'gift', y: 50 };

    // 4. Tree Trunk
    for (let y = 49; y <= 56; y++) {
      for (let dx = -3; dx <= 3; dx++) {
        const x = centerX + dx;
        const shade = Math.abs(dx) <= 1 ? '#78350f' : '#451a03';
        grid[y][x] = { char: rng() < 0.5 ? '#' : '%', color: shade, glow: 0.2, layer: 'trunk', y: y };
      }
    }

    // 5. Tree Foliage (Pine branches)
    const treeApexY = 11;
    const treeBaseY = 50;
    const foliageSet = new Set();

    for (let y = treeApexY; y <= treeBaseY; y++) {
      const v = (y - treeApexY) / (treeBaseY - treeApexY);
      const tierPhase = (v * 5.5) % 1.0;
      const tierScallop = Math.pow(tierPhase, 0.65) * 3.2;
      let halfW = 1.6 + 24.5 * Math.pow(v, 0.94) + tierScallop;
      halfW = Math.min(halfW, 28.5);

      const xStart = Math.round(centerX - halfW);
      const xEnd = Math.round(centerX + halfW);

      for (let x = xStart; x <= xEnd; x++) {
        if (x < 0 || x >= COLS) continue;
        foliageSet.add(`${x},${y}`);

        const dist = Math.abs(x - centerX);
        const normR = dist / Math.max(0.5, halfW);

        let ch, c, glow;
        if (normR < 0.35) {
          ch = PINE_CHARS_DENSE[Math.floor(rng() * PINE_CHARS_DENSE.length)];
          c = rng() < 0.5 ? COLOR_PINE_DEEP : COLOR_PINE_MID;
          glow = 0.25;
        } else if (normR < 0.72) {
          ch = PINE_CHARS_MID[Math.floor(rng() * PINE_CHARS_MID.length)];
          c = rng() < 0.5 ? COLOR_PINE_MID : COLOR_PINE_BRIGHT;
          glow = 0.4;
        } else {
          ch = PINE_CHARS_LIGHT[Math.floor(rng() * PINE_CHARS_LIGHT.length)];
          c = rng() < 0.5 ? COLOR_PINE_BRIGHT : (rng() < 0.5 ? COLOR_PINE_TIP : COLOR_PINE_HIGHLIGHT);
          glow = 0.55;
        }
        grid[y][x] = { char: ch, color: c, glow: glow, layer: 'foliage', y: y };
      }
    }

    // 6. Spiraling Garland Lights
    const garlandCount = 260;
    for (let i = 0; i < garlandCount; i++) {
      const frac = i / garlandCount;
      const y = Math.round(treeApexY + frac * (treeBaseY - treeApexY));
      const v = (y - treeApexY) / (treeBaseY - treeApexY);
      const angle = v * 5.2 * 2.0 * Math.PI - 0.4;
      const halfW = 1.6 + 24.5 * Math.pow(v, 0.94);
      const z = Math.cos(angle);

      if (z > -0.25) {
        const xOffset = halfW * Math.sin(angle) * 0.88;
        const x = Math.round(centerX + xOffset);

        for (const dy of [-1, 0]) {
          const cy = y + dy;
          if (foliageSet.has(`${x},${cy}`)) {
            const gChar = GARLAND_CHARS[Math.floor(rng() * GARLAND_CHARS.length)];
            const col = z > 0.4 ? COLOR_GARLAND_BRIGHT : COLOR_GARLAND_GOLD;
            grid[cy][x] = { char: gChar, color: col, glow: 0.85 + z * 0.15, layer: 'garland', y: cy };
          }
        }
      }
    }

    // 7. Bells & Baubles
    const ornaments = [
      [-0.35, 0.22, 'red'], [0.32, 0.25, 'red'], [0.05, 0.28, 'bell'],
      [-0.52, 0.38, 'bell'], [0.48, 0.39, 'red'], [-0.15, 0.42, 'red'],
      [0.22, 0.45, 'bell'], [-0.42, 0.52, 'red'], [0.38, 0.53, 'red'],
      [0.02, 0.56, 'bell'], [-0.62, 0.62, 'red'], [0.58, 0.63, 'bell'],
      [-0.25, 0.65, 'red'], [0.28, 0.68, 'red'], [-0.50, 0.74, 'bell'],
      [0.45, 0.75, 'red'], [-0.08, 0.78, 'bell'], [0.12, 0.81, 'red'],
      [-0.35, 0.85, 'bell'], [0.35, 0.86, 'red'], [-0.68, 0.89, 'red'],
      [0.65, 0.90, 'bell'], [-0.18, 0.93, 'bell'], [0.20, 0.94, 'red'],
    ];

    ornaments.forEach(([xRat, yRat, otype]) => {
      const oy = Math.round(treeApexY + yRat * (treeBaseY - treeApexY));
      const v = (oy - treeApexY) / (treeBaseY - treeApexY);
      const halfW = 1.6 + 24.5 * Math.pow(v, 0.94);
      const ox = Math.round(centerX + xRat * halfW);

      if (foliageSet.has(`${ox},${oy}`)) {
        if (otype === 'red') {
          for (const ddx of [-1, 0]) {
            const px = ox + ddx;
            if (foliageSet.has(`${px},${oy}`)) {
              const ch = ddx === 0 ? '@' : '%';
              const col = ddx === 0 ? COLOR_ORNAMENT_RED : COLOR_ORNAMENT_DARK_RED;
              grid[oy][px] = { char: ch, color: col, glow: 0.85, layer: 'ornament', y: oy };
            }
          }
          if (foliageSet.has(`${ox},${oy - 1}`)) {
            grid[oy - 1][ox] = { char: '.', color: COLOR_ORNAMENT_SHINE, glow: 0.95, layer: 'ornament', y: oy - 1 };
          }
        } else if (otype === 'bell') {
          if (foliageSet.has(`${ox},${oy - 1}`)) {
            grid[oy - 1][ox] = { char: '^', color: COLOR_GARLAND_WARM, glow: 0.8, layer: 'bell', y: oy - 1 };
          }
          grid[oy][ox] = { char: 'e', color: COLOR_BELL_GOLD, glow: 0.95, layer: 'bell', y: oy };
          if (foliageSet.has(`${ox - 1},${oy}`)) {
            grid[oy][ox - 1] = { char: 'o', color: COLOR_BELL_GOLD, glow: 0.85, layer: 'bell', y: oy };
          }
          if (foliageSet.has(`${ox + 1},${oy}`)) {
            grid[oy][ox + 1] = { char: 'o', color: COLOR_BELL_GOLD, glow: 0.85, layer: 'bell', y: oy };
          }
          if (foliageSet.has(`${ox},${oy + 1}`)) {
            grid[oy + 1][ox] = { char: '.', color: COLOR_STAR_CORE, glow: 0.9, layer: 'bell', y: oy + 1 };
          }
        }
      }
    });

    // 8. Top Star
    const starRows = [
      [5, ['e']],
      [6, ['e', 'e', 'e']],
      [7, ['e', 'e', 'e', 'e', 'e']],
      [8, ['e', 'e', 'e', 'e', 'e', 'e', 'e']],
      [9, ['e', 'e', 'e', 'e', 'e']],
      [10, ['e', 'e', 'e']],
    ];
    starRows.forEach(([sy, chars]) => {
      const len = chars.length;
      const startX = centerX - Math.floor(len / 2);
      chars.forEach((ch, idx) => {
        const sx = startX + idx;
        const isCore = (idx === Math.floor(len / 2) && sy === 8);
        grid[sy][sx] = {
          char: isCore ? '@' : ch,
          color: isCore ? COLOR_STAR_CORE : COLOR_STAR_GOLD,
          glow: 1.0,
          layer: 'star',
          y: sy
        };
      });
    });

    // 9. Radiant Star Rays
    for (let dy = 1; dy <= 4; dy++) {
      grid[5 - dy][centerX] = { char: '|', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 1.0 - dy * 0.18), layer: 'beam', y: 5 - dy };
    }
    for (let d = 1; d <= 4; d++) {
      grid[5 - d][centerX - d * 2] = { char: '\\', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 1.0 - d * 0.18), layer: 'beam', y: 5 - d };
      grid[5 - d][centerX + d * 2] = { char: '/', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 1.0 - d * 0.18), layer: 'beam', y: 5 - d };
    }
    for (let dx = 1; dx <= 5; dx++) {
      grid[8][centerX - 4 - dx] = { char: '-', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 1.0 - dx * 0.15), layer: 'beam', y: 8 };
      grid[8][centerX + 4 + dx] = { char: '-', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 1.0 - dx * 0.15), layer: 'beam', y: 8 };
    }
    for (let d = 1; d <= 3; d++) {
      grid[10 + d][centerX - d * 2] = { char: '/', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 0.9 - d * 0.2), layer: 'beam', y: 10 + d };
      grid[10 + d][centerX + d * 2] = { char: '\\', color: COLOR_STAR_BEAM, glow: Math.max(0.3, 0.9 - d * 0.2), layer: 'beam', y: 10 + d };
    }

    return grid;
  }

  // Snowfall Particle Engine
  class SnowSystem {
    constructor(count = 110) {
      this.count = count;
      this.flakes = [];
      const rng = createRng(99);
      for (let i = 0; i < count; i++) {
        this.flakes.push({
          x: rng() * COLS,
          y: rng() * ROWS,
          speed: 0.35 + rng() * 0.75,
          swayAmp: 0.3 + rng() * 1.4,
          swayFreq: 0.5 + rng() * 1.5,
          swayPhase: rng() * Math.PI * 2,
          char: SNOW_CHARS[Math.floor(rng() * SNOW_CHARS.length)],
          color: rng() < 0.3 ? '#ffffff' : (rng() < 0.6 ? '#e2e8f0' : '#cbd5e1'),
          glow: 0.4 + rng() * 0.5
        });
      }
    }

    update(dt, t) {
      this.flakes.forEach(f => {
        f.y += f.speed * dt * 8.5;
        f.x += Math.sin(t * f.swayFreq + f.swayPhase) * f.swayAmp * dt * 2.8;
        if (f.y >= ROWS) {
          f.y = 0;
          f.x = Math.random() * COLS;
        }
        if (f.x < 0) f.x += COLS;
        else if (f.x >= COLS) f.x -= COLS;
      });
    }
  }

  // Interactive Click Sparkles
  const userSparkles = [];
  function addSparkles(gridX, gridY) {
    for (let i = 0; i < 18; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.0 + Math.random() * 4.0;
      userSparkles.push({
        x: gridX,
        y: gridY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 0.5,
        char: ['*', '✦', '·', '+', 'o', '❄'][Math.floor(Math.random() * 6)],
        color: ['#fef08a', '#facc15', '#ffffff', '#86efac', '#fca5a5'][Math.floor(Math.random() * 5)],
        life: 1.0,
        decay: 0.02 + Math.random() * 0.03
      });
    }
  }

  // Application State
  const staticScene = buildSceneModel();
  const snowSystem = new SnowSystem(110);

  let isPlaying = true;
  let isMuted = false;
  let animTime = 0.0;
  let lastFrameTime = performance.now();
  let viewMode = 'canvas'; // 'canvas' | 'video'

  // Canvas Sizing & Font Metrics
  let cellWidth = 11;
  let cellHeight = 18;
  let fontSize = 16;

  function resizeCanvases() {
    const dpr = window.devicePixelRatio || 1;
    const viewport = document.getElementById('viewport');
    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;

    // Calculate maximum monospace font that fits
    cellWidth = Math.max(7, Math.floor(vw / (COLS + 4)));
    cellHeight = Math.floor(cellWidth * 1.62);
    if (cellHeight * (ROWS + 4) > vh) {
      cellHeight = Math.max(10, Math.floor(vh / (ROWS + 4)));
      cellWidth = Math.max(6, Math.floor(cellHeight / 1.62));
    }
    fontSize = Math.floor(cellHeight * 0.88);

    const canvasW = COLS * cellWidth;
    const canvasH = ROWS * cellHeight;

    treeCanvas.width = canvasW * dpr;
    treeCanvas.height = canvasH * dpr;
    treeCanvas.style.width = `${canvasW}px`;
    treeCanvas.style.height = `${canvasH}px`;
    treeCtx.scale(dpr, dpr);

    // Sky canvas covers full background
    skyCanvas.width = window.innerWidth * dpr;
    skyCanvas.height = window.innerHeight * dpr;
    skyCanvas.style.width = `${window.innerWidth}px`;
    skyCanvas.style.height = `${window.innerHeight}px`;
    skyCtx.scale(dpr, dpr);
  }

  window.addEventListener('resize', resizeCanvases);
  resizeCanvases();

  // Animation Loop
  function render(now) {
    const dt = Math.min(0.1, (now - lastFrameTime) / 1000);
    lastFrameTime = now;

    if (isPlaying) {
      animTime += dt;
      snowSystem.update(dt, animTime);
    }

    // Update Sparkles
    for (let i = userSparkles.length - 1; i >= 0; i--) {
      const sp = userSparkles[i];
      sp.x += sp.vx * dt * 5.0;
      sp.y += sp.vy * dt * 5.0;
      sp.life -= sp.decay;
      if (sp.life <= 0) userSparkles.splice(i, 1);
    }

    // Update Growth Progress Bar
    const progress = Math.min(1.0, animTime / TOTAL_BUILD_DURATION);
    progressBar.style.setProperty('--progress', `${progress * 100}%`);
    if (progress < 1.0) {
      progressBarWrap.classList.remove('done');
      if (animTime < 1.5) progressLabel.textContent = 'Snowy Night...';
      else if (animTime < 3.5) progressLabel.textContent = 'Frost Settling...';
      else if (animTime < 5.5) progressLabel.textContent = 'Gifts Wrapping...';
      else if (animTime < 13.5) progressLabel.textContent = `Tree Ascending (${Math.round(progress * 100)}%)...`;
      else progressLabel.textContent = 'Star Igniting! ⭐';
    } else {
      progressLabel.textContent = 'Merry Christmas! 🎄';
      if (animTime > 18.0) progressBarWrap.classList.add('done');
    }

    // Draw Sky Background
    drawSkyBackground();

    // Draw Tree ASCII Canvas
    if (viewMode === 'canvas') {
      drawTreeFrame(animTime);
    }

    requestAnimationFrame(render);
  }

  // Draw Sky Background
  function drawSkyBackground() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    skyCtx.clearRect(0, 0, w, h);

    // Radial gradient glow behind tree center
    const grad = skyCtx.createRadialGradient(w / 2, h * 0.45, 10, w / 2, h * 0.45, Math.max(w, h) * 0.65);
    grad.addColorStop(0, '#0d1933');
    grad.addColorStop(0.5, '#070c1b');
    grad.addColorStop(1, '#040710');
    skyCtx.fillStyle = grad;
    skyCtx.fillRect(0, 0, w, h);
  }

  // Draw Foreground Tree Canvas
  function drawTreeFrame(t) {
    const canvasW = COLS * cellWidth;
    const canvasH = ROWS * cellHeight;
    treeCtx.clearRect(0, 0, canvasW, canvasH);

    treeCtx.font = `bold ${fontSize}px 'Fira Code', 'Courier New', monospace`;
    treeCtx.textBaseline = 'top';

    // Animation progress values
    const groundProgress = t >= 1.5 ? Math.min(1.0, (t - 1.5) / 2.0) : 0.0;
    const groundCutoffY = (ROWS - 1) - groundProgress * ((ROWS - 1) - 48);

    const giftProgress = t >= 3.0 ? Math.min(1.0, (t - 3.0) / 2.0) : 0.0;
    const giftCutoffY = (ROWS - 2) - giftProgress * 10;

    const treeProgress = t >= 5.0 ? Math.min(1.0, (t - 5.0) / 8.5) : 0.0;
    const treeGrowthY = 56 - treeProgress * (56 - 11);

    const starProgress = t >= 13.5 ? Math.min(1.0, (t - 13.5) / 2.0) : 0.0;

    // Render cells
    for (let y = 0; y < ROWS; y++) {
      for (let x = 0; x < COLS; x++) {
        const cell = staticScene[y][x];
        let visible = false;
        let char = cell.char;
        let color = cell.color;
        let glow = cell.glow;

        if (cell.layer === 'sky') {
          visible = (char !== ' ');
          if (visible) {
            const twinkle = 0.5 + 0.5 * Math.sin(t * 2.5 + x * 0.7 + y * 1.3);
            glow *= twinkle;
          }
        } else if (cell.layer === 'ground') {
          if (y >= groundCutoffY) {
            visible = true;
            const age = y - groundCutoffY;
            const flash = 1.0 + Math.max(0, 1.0 - age) * 0.5;
            glow *= flash;
          }
        } else if (cell.layer === 'gift') {
          if (y >= giftCutoffY) {
            visible = true;
          }
        } else if (['trunk', 'foliage', 'garland', 'ornament', 'bell'].includes(cell.layer)) {
          if (y >= treeGrowthY) {
            visible = true;
            const dist = Math.abs(y - treeGrowthY);

            // Leading crest flash as layer grows
            if (dist < 1.8 && treeProgress < 1.0) {
              glow = 1.0;
              if (Math.random() < 0.25) {
                char = ['*', '+', '#', 'o'][Math.floor(Math.random() * 4)];
                color = COLOR_STAR_CORE;
              }
            }

            // Post-growth twinkling
            if (t > 13.5) {
              if (cell.layer === 'garland') {
                const wave = Math.sin(t * 4.0 - y * 0.4 + x * 0.1);
                glow = 0.7 + 0.3 * wave;
              } else if (['ornament', 'bell'].includes(cell.layer)) {
                const shimmer = Math.sin(t * 3.0 + x * 0.5 + y * 0.8);
                glow = 0.75 + 0.25 * shimmer;
              }
            }
          }
        } else if (cell.layer === 'star') {
          if (starProgress > 0.0) {
            visible = true;
            const pulse = 1.0 + 0.25 * Math.sin(t * 5.0);
            glow *= pulse;
          }
        } else if (cell.layer === 'beam') {
          if (starProgress >= 0.5) {
            const beamFrac = (starProgress - 0.5) / 0.5;
            const dist = Math.sqrt(Math.pow(x - COLS / 2, 2) + Math.pow(y - 8, 2));
            if (dist <= beamFrac * 12.0) {
              visible = true;
              const pulse = 0.7 + 0.3 * Math.sin(t * 3.5 + dist * 0.5);
              glow *= pulse;
            }
          }
        }

        if (visible && char !== ' ') {
          const px = x * cellWidth;
          const py = y * cellHeight;

          // Character glow shadow
          if (glow > 0.4) {
            treeCtx.shadowColor = color;
            treeCtx.shadowBlur = Math.round(glow * 10);
          } else {
            treeCtx.shadowBlur = 0;
          }

          treeCtx.fillStyle = color;
          treeCtx.fillText(char, px, py);
        }
      }
    }

    // Render Snowflakes
    treeCtx.shadowBlur = 4;
    treeCtx.shadowColor = '#ffffff';
    snowSystem.flakes.forEach(f => {
      const sx = Math.floor(f.x) * cellWidth;
      const sy = Math.floor(f.y) * cellHeight;
      treeCtx.fillStyle = f.color;
      treeCtx.fillText(f.char, sx, sy);
    });

    // Render Interactive User Sparkles
    userSparkles.forEach(sp => {
      const px = sp.x * cellWidth;
      const py = sp.y * cellHeight;
      treeCtx.shadowColor = sp.color;
      treeCtx.shadowBlur = 12 * sp.life;
      treeCtx.fillStyle = sp.color;
      treeCtx.globalAlpha = Math.max(0, sp.life);
      treeCtx.fillText(sp.char, px, py);
    });
    treeCtx.globalAlpha = 1.0;
    treeCtx.shadowBlur = 0;
  }

  // Interactive Click on Canvas for Sparkles
  treeCanvas.addEventListener('pointerdown', (e) => {
    const rect = treeCanvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const gridX = clickX / cellWidth;
    const gridY = clickY / cellHeight;
    addSparkles(gridX, gridY);
  });

  // Audio Control Handlers
  function startPlayback() {
    audioPrompt.classList.add('hidden');
    bgAudio.volume = parseFloat(volSlider.value);
    bgAudio.play().then(() => {
      isMuted = false;
      updateAudioUI();
    }).catch(err => {
      console.log('Audio autoplay prevented:', err);
      unmuteToast.classList.remove('hidden');
    });
  }

  function updateAudioUI() {
    if (bgAudio.paused) {
      playPauseIcon.textContent = '▶';
      playPauseText.textContent = 'Play';
    } else {
      playPauseIcon.textContent = '⏸';
      playPauseText.textContent = 'Pause';
    }

    if (bgAudio.muted || bgAudio.volume === 0) {
      muteIcon.textContent = '🔇';
    } else if (bgAudio.volume < 0.5) {
      muteIcon.textContent = '🔉';
    } else {
      muteIcon.textContent = '🔊';
    }
  }

  btnStart.addEventListener('click', startPlayback);

  toastUnmuteBtn.addEventListener('click', () => {
    bgAudio.muted = false;
    bgAudio.play();
    unmuteToast.classList.add('hidden');
    updateAudioUI();
  });

  btnPlayPause.addEventListener('click', () => {
    if (isPlaying) {
      isPlaying = false;
      bgAudio.pause();
      if (viewMode === 'video') hdVideo.pause();
    } else {
      isPlaying = true;
      lastFrameTime = performance.now();
      bgAudio.play().catch(() => {});
      if (viewMode === 'video') hdVideo.play().catch(() => {});
    }
    updateAudioUI();
  });

  btnRestart.addEventListener('click', () => {
    animTime = 0.0;
    bgAudio.currentTime = 0;
    if (viewMode === 'video') hdVideo.currentTime = 0;
    if (!isPlaying) {
      isPlaying = true;
      lastFrameTime = performance.now();
      bgAudio.play().catch(() => {});
    }
    progressBarWrap.classList.remove('done');
    updateAudioUI();
  });

  btnMute.addEventListener('click', () => {
    bgAudio.muted = !bgAudio.muted;
    if (viewMode === 'video') hdVideo.muted = bgAudio.muted;
    updateAudioUI();
  });

  volSlider.addEventListener('input', (e) => {
    bgAudio.volume = parseFloat(e.target.value);
    if (bgAudio.volume > 0) bgAudio.muted = false;
    if (viewMode === 'video') hdVideo.volume = bgAudio.volume;
    updateAudioUI();
  });

  // CRT Bloom Toggle
  let bloomEnabled = true;
  btnBloom.addEventListener('click', () => {
    bloomEnabled = !bloomEnabled;
    btnBloom.classList.toggle('active', bloomEnabled);
    treeCanvas.classList.toggle('bloom', bloomEnabled);
    crtOverlay.classList.toggle('disabled', !bloomEnabled);
  });

  // Fullscreen Toggle
  btnFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  // Toggle View: Canvas vs Python-rendered Video
  btnToggleView.addEventListener('click', () => {
    if (viewMode === 'canvas') {
      viewMode = 'video';
      treeCanvas.classList.remove('active');
      videoContainer.classList.add('active');
      viewIcon.textContent = '🌲';
      viewLabel.textContent = 'Interactive Canvas';

      // Sync video with audio
      hdVideo.currentTime = animTime % 18.0;
      if (isPlaying) hdVideo.play().catch(() => {});
    } else {
      viewMode = 'canvas';
      videoContainer.classList.remove('active');
      treeCanvas.classList.add('active');
      viewIcon.textContent = '🎬';
      viewLabel.textContent = 'Watch HD Video';
      hdVideo.pause();
    }
  });

  // Start animation loop
  requestAnimationFrame(render);
})();
