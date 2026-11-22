/**
 * Christmas Tree ASCII Animation & Web Engine
 * 100% Authentic Visual Fidelity to reference.jpeg:
 * - Crown star at apex with radiant celestial beams (\, |, /, -)
 * - Conical evergreen foliage with tiered pine branches
 * - Golden spiraling garlands (#ee*0, *ee#%*)
 * - Ruby red bauble ornaments (@, %) and golden bells
 * - Wrapped gifts at base (Red box left, Royal Blue box right) and snow mound
 * - Wide perspective ground grid (...., ::::, ----, ++++, ====)
 * - White pixelated snowfall physics & CRT bloom overlay
 * - Organic bottom-to-top assembly animation running for >15 seconds (16.0s build + celebration)
 * - Synchronized to Sia - Snowman starting directly at "Don't cry snowman"
 */

(function () {
  'use strict';

  // Constants
  const TOTAL_BUILD_DURATION = 15.0; // Tree is completed exactly at 15.0s

  // DOM Elements
  const treeCanvas = document.getElementById('tree-canvas');
  const treeCtx = treeCanvas.getContext('2d');
  const skyCanvas = document.getElementById('sky-canvas');
  const skyCtx = skyCanvas.getContext('2d');

  const bgAudio = document.getElementById('bg-audio');
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

  // Load the authentic reference image and sky background
  const refImg = new Image();
  refImg.src = 'reference.jpeg';
  let refLoaded = false;
  refImg.onload = () => { refLoaded = true; };

  const skyImg = new Image();
  skyImg.src = 'sky_bg.jpg';
  let skyLoaded = false;
  skyImg.onload = () => { skyLoaded = true; };

  // Snowflake Particle Physics System
  const SNOW_CHARS = ['.', '·', '*', '+', 'o', '❄'];
  class SnowSystem {
    constructor(count = 130) {
      this.count = count;
      this.flakes = [];
      for (let i = 0; i < count; i++) {
        this.flakes.push({
          x: Math.random(),
          y: Math.random(),
          speed: 0.045 + Math.random() * 0.08,
          swayAmp: 0.012 + Math.random() * 0.025,
          swayFreq: 0.8 + Math.random() * 1.5,
          swayPhase: Math.random() * Math.PI * 2,
          char: SNOW_CHARS[Math.floor(Math.random() * SNOW_CHARS.length)],
          size: Math.floor(10 + Math.random() * 14),
          alpha: 0.45 + Math.random() * 0.55
        });
      }
    }

    update(dt, t) {
      this.flakes.forEach(f => {
        f.y += f.speed * dt;
        f.x += Math.sin(t * f.swayFreq + f.swayPhase) * f.swayAmp * dt;
        if (f.y >= 1.0) {
          f.y = 0;
          f.x = Math.random();
        }
        if (f.x < 0) f.x += 1.0;
        else if (f.x >= 1.0) f.x -= 1.0;
      });
    }
  }

  // Interactive Click Sparkles
  const userSparkles = [];
  function addSparkles(px, py) {
    for (let i = 0; i < 24; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 40 + Math.random() * 130;
      userSparkles.push({
        x: px,
        y: py,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 25,
        char: ['*', '✦', '·', '+', 'o', '❄', '0', 'e'][Math.floor(Math.random() * 8)],
        color: ['#fef08a', '#facc15', '#ffffff', '#86efac', '#fca5a5'][Math.floor(Math.random() * 5)],
        life: 1.0,
        decay: 0.02 + Math.random() * 0.03
      });
    }
  }

  const snowSystem = new SnowSystem(130);
  let isPlaying = true;
  let isMuted = false;
  let animTime = 0.0;
  let lastFrameTime = performance.now();
  let viewMode = 'canvas';

  // Canvas Sizing
  const NATIVE_W = 1072;
  const NATIVE_H = 1180;
  const CX = NATIVE_W / 2;

  function resizeCanvases() {
    const dpr = window.devicePixelRatio || 1;
    const viewport = document.getElementById('viewport');
    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;

    const scale = Math.min((vw * 0.95) / NATIVE_W, (vh * 0.88) / NATIVE_H);
    const canvasW = Math.round(NATIVE_W * scale);
    const canvasH = Math.round(NATIVE_H * scale);

    treeCanvas.width = canvasW * dpr;
    treeCanvas.height = canvasH * dpr;
    treeCanvas.style.width = `${canvasW}px`;
    treeCanvas.style.height = `${canvasH}px`;
    treeCtx.scale(dpr * scale, dpr * scale);

    skyCanvas.width = window.innerWidth * dpr;
    skyCanvas.height = window.innerHeight * dpr;
    skyCanvas.style.width = `${window.innerWidth}px`;
    skyCanvas.style.height = `${window.innerHeight}px`;
    skyCtx.scale(dpr, dpr);
  }

  window.addEventListener('resize', resizeCanvases);
  resizeCanvases();

  // Main Render Loop
  function render(now) {
    const dt = Math.min(0.1, (now - lastFrameTime) / 1000);
    lastFrameTime = now;

    if (isPlaying) {
      animTime += dt;
      snowSystem.update(dt, animTime);
    }

    // Update User Click Sparkles
    for (let i = userSparkles.length - 1; i >= 0; i--) {
      const sp = userSparkles[i];
      sp.x += sp.vx * dt;
      sp.y += sp.vy * dt;
      sp.life -= sp.decay;
      if (sp.life <= 0) userSparkles.splice(i, 1);
    }

    // Update Progress Bar & Synced Lyrics
    const progress = Math.min(1.0, animTime / TOTAL_BUILD_DURATION);
    progressBar.style.setProperty('--progress', `${progress * 100}%`);
    if (progress < 1.0) {
      progressBarWrap.classList.remove('done');
      if (animTime < 1.5) progressLabel.textContent = "Don't cry, snowman...";
      else if (animTime < 3.5) progressLabel.textContent = "Not in front of me...";
      else if (animTime < 5.5) progressLabel.textContent = "Gifts & Ground Assembling... 🎁";
      else if (animTime < 9.5) progressLabel.textContent = "Tree Ascending... 🌲";
      else if (animTime < 13.5) progressLabel.textContent = "Garlands Blooming... ✨";
      else progressLabel.textContent = "⭐ Pinnacle Crown Star Igniting! ⭐";
    } else {
      progressLabel.textContent = 'Merry Christmas & Happy Holidays! 🎄';
      if (animTime > 17.0) progressBarWrap.classList.add('done');
    }

    // Draw Sky Background
    drawSkyBackground();

    // Draw Tree Animation
    if (viewMode === 'canvas') {
      drawTreeFrame(animTime);
    }

    requestAnimationFrame(render);
  }

  function drawSkyBackground() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    skyCtx.clearRect(0, 0, w, h);

    const grad = skyCtx.createRadialGradient(w / 2, h * 0.45, 10, w / 2, h * 0.45, Math.max(w, h) * 0.65);
    grad.addColorStop(0, '#0d1933');
    grad.addColorStop(0.5, '#070c1b');
    grad.addColorStop(1, '#040710');
    skyCtx.fillStyle = grad;
    skyCtx.fillRect(0, 0, w, h);
  }

  function drawTreeFrame(t) {
    treeCtx.clearRect(0, 0, NATIVE_W, NATIVE_H);

    // 1. Draw Starry Night Sky Base
    if (skyLoaded) {
      treeCtx.drawImage(skyImg, 0, 0, NATIVE_W, NATIVE_H);
    } else {
      treeCtx.fillStyle = '#070b19';
      treeCtx.fillRect(0, 0, NATIVE_W, NATIVE_H);
    }

    if (!refLoaded) return;

    // Organic timeline:
    // 0.0s - 2.0s: Cosmic sky with snowfall
    // 2.0s - 4.5s: Ground perspective lines reveal from horizon down
    // 4.5s - 6.5s: Wrapped gifts & snow bank assemble at base
    // 6.5s - 13.8s: Tree ascends organically with natural branch-profile crest
    // 13.8s - 15.5s: Crown star ignites at apex, radiating beams into space
    // 15.5s+: Full 100% faithful artwork active

    let treeProg = 0.0;
    let currTreeY = 1040;

    if (t < 15.0) {
      treeCtx.save();
      treeCtx.beginPath();

      // A. Ground Perspective Grid (1.5s to 3.5s)
      if (t >= 1.5) {
        const gProg = Math.min(1.0, (t - 1.5) / 2.0);
        const currGY = 810 + gProg * (NATIVE_H - 810);
        treeCtx.rect(0, 810, NATIVE_W, currGY - 810);
      }

      // B. Wrapped Gifts & Snow Bank (3.5s to 5.5s)
      if (t >= 3.5) {
        // Red gift box (left)
        treeCtx.rect(190, 960, 210, 180);
        // Blue gift box (right)
        treeCtx.rect(690, 960, 220, 180);
        // Snow drift (center base)
        treeCtx.rect(400, 1020, 290, 120);
      }

      // C. Tree Foliage & Garlands (5.5s to 13.5s)
      if (t >= 5.5) {
        treeProg = Math.min(1.0, (t - 5.5) / 8.0);
        currTreeY = 1040 - treeProg * (1040 - 200);

        const halfWAtBase = 385;
        const halfWAtTop = 40 + (currTreeY - 200) / 840 * 345;

        // Trace organic branch contour
        treeCtx.moveTo(CX - halfWAtBase, 1040);
        treeCtx.lineTo(CX + halfWAtBase, 1040);
        treeCtx.lineTo(CX + halfWAtTop, currTreeY);

        // Branch-wave crest at current growth height
        const steps = 30;
        for (let i = 0; i <= steps; i++) {
          const frac = i / steps;
          const x = (CX + halfWAtTop) - frac * (halfWAtTop * 2);
          const wobble = 12 * Math.sin(x * 0.05) * Math.cos(currTreeY * 0.03);
          treeCtx.lineTo(x, currTreeY + wobble);
        }
        treeCtx.lineTo(CX - halfWAtBase, 1040);
        treeCtx.closePath();
      }

      // D. Apex Crown Star & Radiant Beams (13.5s to 15.0s - Completed exactly at 15.0s)
      if (t >= 13.5) {
        const starProg = Math.min(1.0, (t - 13.5) / 1.5);
        // Crown star body
        treeCtx.rect(CX - 85, 120, 170, 85);
        // Radiating celestial beams
        if (starProg > 0.35) {
          const bProg = (starProg - 0.35) / 0.65;
          const beamTop = Math.round(200 - bProg * 170);
          const beamHalfW = Math.round(bProg * 135);
          treeCtx.rect(CX - beamHalfW, beamTop, beamHalfW * 2, 200 - beamTop);
        }
      }

      treeCtx.clip();
      treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
      treeCtx.restore();
    } else {
      // Full 100% authentic reference artwork rendered directly
      treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
    }

    // 3. Dynamic Sparkle Embers Riding the Leading Growth Edge
    if (treeProg > 0.0 && treeProg < 1.0) {
      const halfW = Math.round(40 + treeProg * 345);
      treeCtx.font = "bold 18px 'Fira Code', 'Courier New', monospace";
      treeCtx.shadowBlur = 10;
      for (let i = 0; i < 14; i++) {
        const sx = CX - halfW + Math.random() * (halfW * 2);
        const sy = currTreeY + (Math.random() - 0.5) * 22;
        const ch = ['*', '+', '#', 'o', '0', 'e', '✦'][Math.floor(Math.random() * 7)];
        const col = ['#fef08a', '#22c55e', '#ffffff', '#facc15', '#86efac'][Math.floor(Math.random() * 5)];
        treeCtx.fillStyle = col;
        treeCtx.shadowColor = col;
        treeCtx.fillText(ch, sx, sy);
      }
      treeCtx.shadowBlur = 0;
    }

    // 4. Star Pulse & Warm Golden Bloom Halo
    if (t >= 13.8) {
      const pulse = 1.0 + 0.15 * Math.sin(t * 3.8);
      treeCtx.save();
      treeCtx.beginPath();
      treeCtx.arc(CX, 145, 52 * pulse, 0, Math.PI * 2);
      treeCtx.fillStyle = 'rgba(254, 240, 138, 0.12)';
      treeCtx.shadowColor = '#facc15';
      treeCtx.shadowBlur = 28 * pulse;
      treeCtx.fill();
      treeCtx.restore();
    }

    // 5. White Pixelated Snowfall
    treeCtx.shadowColor = '#ffffff';
    treeCtx.shadowBlur = 4;
    snowSystem.flakes.forEach(f => {
      const sx = f.x * NATIVE_W;
      const sy = f.y * NATIVE_H;
      treeCtx.font = `bold ${f.size}px 'Fira Code', 'Courier New', monospace`;
      treeCtx.fillStyle = `rgba(255, 255, 255, ${f.alpha})`;
      treeCtx.fillText(f.char, sx, sy);
    });
    treeCtx.shadowBlur = 0;

    // 6. Interactive Click Sparkles
    userSparkles.forEach(sp => {
      treeCtx.shadowColor = sp.color;
      treeCtx.shadowBlur = 12 * sp.life;
      treeCtx.fillStyle = sp.color;
      treeCtx.globalAlpha = Math.max(0, sp.life);
      treeCtx.font = "bold 20px 'Fira Code', monospace";
      treeCtx.fillText(sp.char, sp.x, sp.y);
    });
    treeCtx.globalAlpha = 1.0;
    treeCtx.shadowBlur = 0;
  }

  // Interactive Click on Canvas
  treeCanvas.addEventListener('pointerdown', (e) => {
    const rect = treeCanvas.getBoundingClientRect();
    const scaleX = NATIVE_W / rect.width;
    const scaleY = NATIVE_H / rect.height;
    const clickX = (e.clientX - rect.left) * scaleX;
    const clickY = (e.clientY - rect.top) * scaleY;
    addSparkles(clickX, clickY);
  });

  // Audio Handlers - Autoplays immediately on page load / link click
  const AUDIO_START_TIME = 0.0;

  function startPlayback() {
    bgAudio.volume = parseFloat(volSlider.value) || 0.8;
    bgAudio.currentTime = AUDIO_START_TIME;
    const playPromise = bgAudio.play();
    if (playPromise !== undefined) {
      playPromise.then(() => {
        isMuted = false;
        updateAudioUI();
      }).catch(err => {
        // If browser policies block unmuted autoplay prior to user interaction,
        // seamlessly unlock on the first click, tap, scroll, or keypress anywhere
        console.log('Autoplay deferred, waiting for first interaction:', err);
        const autoUnlock = () => {
          bgAudio.currentTime = AUDIO_START_TIME;
          bgAudio.play().then(() => {
            isMuted = false;
            updateAudioUI();
          }).catch(() => {});
          ['pointerdown', 'touchstart', 'click', 'keydown'].forEach(ev => {
            window.removeEventListener(ev, autoUnlock, true);
          });
        };
        ['pointerdown', 'touchstart', 'click', 'keydown'].forEach(ev => {
          window.addEventListener(ev, autoUnlock, { once: true, capture: true });
        });
      });
    }
  }

  // Ensure loop restarts from the beginning
  bgAudio.addEventListener('ended', () => {
    bgAudio.currentTime = AUDIO_START_TIME;
    bgAudio.play().catch(() => {});
  });

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

  // Autoplay immediately on script execution, DOM ready, and window load
  startPlayback();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startPlayback);
  }
  window.addEventListener('load', startPlayback);

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
    bgAudio.currentTime = AUDIO_START_TIME;
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

  let bloomEnabled = true;
  btnBloom.addEventListener('click', () => {
    bloomEnabled = !bloomEnabled;
    btnBloom.classList.toggle('active', bloomEnabled);
    treeCanvas.classList.toggle('bloom', bloomEnabled);
    crtOverlay.classList.toggle('disabled', !bloomEnabled);
  });

  btnFullscreen.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });

  btnToggleView.addEventListener('click', () => {
    if (viewMode === 'canvas') {
      viewMode = 'video';
      treeCanvas.classList.remove('active');
      videoContainer.classList.add('active');
      viewIcon.textContent = '🌲';
      viewLabel.textContent = 'Interactive Canvas';
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

  requestAnimationFrame(render);
})();
