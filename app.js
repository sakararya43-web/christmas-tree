/**
 * Christmas Tree ASCII Animation & Web Engine
 * Renders the authentic visual artwork from reference.jpeg with:
 * - Bottom-to-top progressive reveal animation
 * - Dynamic sparkling ascent crest
 * - White pixelated snowfall physics
 * - Synchronized to Sia - Snowman starting directly at "Don't cry snowman"
 */

(function () {
  'use strict';

  // Constants
  const TOTAL_BUILD_DURATION = 15.5; // Seconds for bottom-to-top assembly

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
    constructor(count = 120) {
      this.count = count;
      this.flakes = [];
      for (let i = 0; i < count; i++) {
        this.flakes.push({
          x: Math.random(),
          y: Math.random(),
          speed: 0.04 + Math.random() * 0.08,
          swayAmp: 0.01 + Math.random() * 0.025,
          swayFreq: 0.8 + Math.random() * 1.5,
          swayPhase: Math.random() * Math.PI * 2,
          char: SNOW_CHARS[Math.floor(Math.random() * SNOW_CHARS.length)],
          size: Math.floor(10 + Math.random() * 12),
          alpha: 0.4 + Math.random() * 0.55
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
    for (let i = 0; i < 22; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 40 + Math.random() * 120;
      userSparkles.push({
        x: px,
        y: py,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 20,
        char: ['*', '✦', '·', '+', 'o', '❄', '0'][Math.floor(Math.random() * 7)],
        color: ['#fef08a', '#facc15', '#ffffff', '#86efac', '#fca5a5'][Math.floor(Math.random() * 5)],
        life: 1.0,
        decay: 0.02 + Math.random() * 0.03
      });
    }
  }

  const snowSystem = new SnowSystem(120);
  let isPlaying = true;
  let isMuted = false;
  let animTime = 0.0;
  let lastFrameTime = performance.now();
  let viewMode = 'canvas';

  // Canvas Sizing
  const NATIVE_W = 1072;
  const NATIVE_H = 1180;

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

    // Update Sparkles
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
      if (animTime < 2.0) progressLabel.textContent = "Don't cry, snowman...";
      else if (animTime < 4.0) progressLabel.textContent = "Not in front of me...";
      else if (animTime < 7.5) progressLabel.textContent = "Tree Ascending... 🌲";
      else if (animTime < 12.0) progressLabel.textContent = "Branches Blooming... ✨";
      else progressLabel.textContent = "⭐ Pinnacle Star Igniting! ⭐";
    } else {
      progressLabel.textContent = 'Merry Christmas! 🎄';
      if (animTime > 18.0) progressBarWrap.classList.add('done');
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

    // 1. Draw Starry Night Base
    if (skyLoaded) {
      treeCtx.drawImage(skyImg, 0, 0, NATIVE_W, NATIVE_H);
    } else {
      treeCtx.fillStyle = '#0a0e1a';
      treeCtx.fillRect(0, 0, NATIVE_W, NATIVE_H);
    }

    if (!refLoaded) return;

    // 2. Progressive Bottom-to-Top Reveal Calculation
    const groundYBottom = 1180;
    const groundYTop = 820;
    const treeYBottom = 1060;
    const treeYTop = 180;

    const groundProg = Math.min(1.0, t / 2.0);
    const currGroundY = Math.round(groundYBottom - groundProg * (groundYBottom - groundYTop));

    const treeProg = Math.min(1.0, Math.max(0.0, (t - 3.5) / 9.0));
    const currTreeY = Math.round(treeYBottom - treeProg * (treeYBottom - treeYTop));

    const starProg = Math.min(1.0, Math.max(0.0, (t - 12.5) / 2.0));

    // Save context for clipping mask
    treeCtx.save();
    treeCtx.beginPath();

    // Reveal ground from bottom up
    if (groundProg > 0) {
      treeCtx.rect(0, currGroundY, NATIVE_W, NATIVE_H - currGroundY);
    }

    // Reveal tree from bottom up
    if (treeProg > 0) {
      treeCtx.rect(170, currTreeY, 730, treeYBottom - currTreeY);
    }

    // Reveal crown star and celestial beams
    if (starProg > 0) {
      const starY = Math.round(treeYTop - starProg * treeYTop);
      treeCtx.rect(340, starY, 400, treeYTop + 40 - starY);
    }

    if (t >= 14.5) {
      // Entire reference image fully active
      treeCtx.rect(0, 0, NATIVE_W, NATIVE_H);
    }

    treeCtx.clip();

    // Draw the authentic reference image
    treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
    treeCtx.restore();

    // 3. Dynamic Sparkle Embers Riding the Leading Edge
    if (treeProg > 0.0 && treeProg < 1.0) {
      const halfW = 20 + Math.round(330 * Math.pow(treeProg, 0.85));
      const cx = NATIVE_W / 2;
      treeCtx.font = "bold 18px 'Fira Code', 'Courier New', monospace";
      treeCtx.shadowBlur = 10;
      for (let i = 0; i < 12; i++) {
        const sx = cx - halfW + Math.random() * (halfW * 2);
        const sy = currTreeY + (Math.random() - 0.5) * 16;
        const ch = ['*', '+', '#', 'o', '0', 'e'][Math.floor(Math.random() * 6)];
        const col = ['#fef08a', '#22c55e', '#ffffff', '#facc15'][Math.floor(Math.random() * 4)];
        treeCtx.fillStyle = col;
        treeCtx.shadowColor = col;
        treeCtx.fillText(ch, sx, sy);
      }
      treeCtx.shadowBlur = 0;
    }

    // 4. Star Pulse & Radiant Glow after Apex Reached
    if (starProg > 0.0) {
      const pulse = 1.0 + 0.15 * Math.sin(t * 4.5);
      treeCtx.save();
      treeCtx.beginPath();
      treeCtx.arc(536, 110, 45 * pulse, 0, Math.PI * 2);
      treeCtx.fillStyle = 'rgba(254, 240, 138, 0.12)';
      treeCtx.shadowColor = '#facc15';
      treeCtx.shadowBlur = 25 * pulse;
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

  // Audio Handlers
  function startPlayback() {
    audioPrompt.classList.add('hidden');
    bgAudio.volume = parseFloat(volSlider.value);
    bgAudio.currentTime = 0;
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
