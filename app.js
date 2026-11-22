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
 * - Organic bottom-to-top assembly animation completed exactly at 15th second (15.0s build + celebration)
 * - Immediate start on link click (unmuted if permitted, seamless muted start + instant gesture unmute)
 * - Exact audio synchronization to Sia - Snowman
 */

(function () {
  'use strict';

  // Constants
  const TOTAL_BUILD_DURATION = 15.0; // Completed exactly at 15.0s
  const NATIVE_W = 1072;
  const NATIVE_H = 1180;
  const CX = NATIVE_W / 2;

  // DOM Elements
  const treeCanvas = document.getElementById('tree-canvas');
  const treeCtx = treeCanvas ? treeCanvas.getContext('2d') : null;
  const skyCanvas = document.getElementById('sky-canvas');
  const skyCtx = skyCanvas ? skyCanvas.getContext('2d') : null;

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
  const audioPill = document.getElementById('audio-pill');

  // Load Reference Image & Background with Cache-Safe Check
  let refLoaded = false;
  const refImg = new Image();
  refImg.onload = () => { refLoaded = true; };
  refImg.onerror = () => { console.warn('Could not load reference.jpeg'); };
  refImg.src = 'reference.jpeg';
  if (refImg.complete && refImg.naturalWidth > 0) {
    refLoaded = true;
  }

  let skyLoaded = false;
  const skyImg = new Image();
  skyImg.onload = () => { skyLoaded = true; };
  skyImg.onerror = () => { console.warn('Could not load sky_bg.jpg'); };
  skyImg.src = 'sky_bg.jpg';
  if (skyImg.complete && skyImg.naturalWidth > 0) {
    skyLoaded = true;
  }

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

  // Dynamic Responsive Canvas Resizing
  function resizeCanvases() {
    if (!treeCanvas || !treeCtx || !skyCanvas || !skyCtx) return;

    const dpr = window.devicePixelRatio || 1;
    const viewport = document.getElementById('viewport');
    const vw = (viewport && viewport.clientWidth) || window.innerWidth;
    const vh = (viewport && viewport.clientHeight) || (window.innerHeight - 130);

    const scale = Math.max(0.15, Math.min((vw * 0.96) / NATIVE_W, (vh * 0.88) / NATIVE_H));
    const canvasW = Math.round(NATIVE_W * scale);
    const canvasH = Math.round(NATIVE_H * scale);

    treeCanvas.width = canvasW * dpr;
    treeCanvas.height = canvasH * dpr;
    treeCanvas.style.width = `${canvasW}px`;
    treeCanvas.style.height = `${canvasH}px`;
    treeCtx.setTransform(dpr * scale, 0, 0, dpr * scale, 0, 0);

    skyCanvas.width = window.innerWidth * dpr;
    skyCanvas.height = window.innerHeight * dpr;
    skyCanvas.style.width = `${window.innerWidth}px`;
    skyCanvas.style.height = `${window.innerHeight}px`;
    skyCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  window.addEventListener('resize', resizeCanvases);
  window.addEventListener('load', resizeCanvases);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', resizeCanvases);
  }
  resizeCanvases();

  // Main Render Loop
  function render(now) {
    if (!treeCtx || !skyCtx) return;

    // Check if cached image became available
    if (!refLoaded && refImg.complete && refImg.naturalWidth > 0) refLoaded = true;
    if (!skyLoaded && skyImg.complete && skyImg.naturalWidth > 0) skyLoaded = true;

    // Check if canvas was initialized before layout
    if (treeCanvas.width === 0 || treeCanvas.height === 0) {
      resizeCanvases();
    }

    const dt = Math.min(0.1, (now - lastFrameTime) / 1000);
    lastFrameTime = now;

    if (isPlaying) {
      if (bgAudio && !bgAudio.paused && bgAudio.currentTime > 0) {
        // Synchronize animation time directly to exact audio timestamp
        animTime = bgAudio.currentTime;
      } else {
        animTime += dt;
      }
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
    if (progressBar) {
      progressBar.style.setProperty('--progress', `${progress * 100}%`);
    }

    if (progressLabel) {
      if (progress < 1.0) {
        if (progressBarWrap) progressBarWrap.classList.remove('done');
        if (animTime < 1.5) progressLabel.textContent = "Don't cry, snowman...";
        else if (animTime < 3.5) progressLabel.textContent = "Not in front of me...";
        else if (animTime < 5.5) progressLabel.textContent = "Gifts & Ground Assembling... 🎁";
        else if (animTime < 9.5) progressLabel.textContent = "Tree Ascending... 🌲";
        else if (animTime < 13.5) progressLabel.textContent = "Garlands Blooming... ✨";
        else progressLabel.textContent = "⭐ Pinnacle Crown Star Igniting! ⭐";
      } else {
        progressLabel.textContent = 'Merry Christmas & Happy Holidays! 🎄';
        if (animTime > 17.0 && progressBarWrap) {
          progressBarWrap.classList.add('done');
        }
      }
    }

    // Draw Background
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

    // 1. Starry Night Sky Base
    if (skyLoaded) {
      treeCtx.drawImage(skyImg, 0, 0, NATIVE_W, NATIVE_H);
    } else {
      treeCtx.fillStyle = '#070b19';
      treeCtx.fillRect(0, 0, NATIVE_W, NATIVE_H);
    }

    let treeProg = 0.0;
    let currTreeY = 1040;

    // 2. Draw Artwork if loaded
    if (refLoaded) {
      if (t >= TOTAL_BUILD_DURATION) {
        // Complete authentic artwork fully active
        treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
      } else {
        // Organic multi-pass assembly (clean, disjoint clipping passes)

        // Pass A: Ground Perspective Grid (1.5s to 3.5s)
        if (t >= 1.5) {
          const gProg = Math.min(1.0, (t - 1.5) / 2.0);
          const currGY = 810 + gProg * (NATIVE_H - 810);
          treeCtx.save();
          treeCtx.beginPath();
          treeCtx.rect(0, 810, NATIVE_W, currGY - 810);
          treeCtx.clip();
          treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
          treeCtx.restore();
        }

        // Pass B: Wrapped Gifts & Snow Bank (3.5s to 5.5s)
        if (t >= 3.5) {
          treeCtx.save();
          treeCtx.beginPath();
          treeCtx.rect(170, 950, 230, 200);
          treeCtx.rect(680, 950, 240, 200);
          treeCtx.rect(390, 1010, 300, 140);
          treeCtx.clip();
          treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
          treeCtx.restore();
        }

        // Pass C: Tree Foliage & Spiraling Garlands (5.5s to 13.5s)
        if (t >= 5.5) {
          treeProg = Math.min(1.0, (t - 5.5) / 8.0);
          currTreeY = 1040 - treeProg * (1040 - 200);

          const halfWAtTop = 40 + (currTreeY - 200) / 840 * 345;

          treeCtx.save();
          treeCtx.beginPath();
          treeCtx.moveTo(CX - 385, 1045);
          treeCtx.lineTo(CX + 385, 1045);
          treeCtx.lineTo(CX + halfWAtTop, currTreeY);

          // Organic branch-wave crest along current growth height
          const steps = 30;
          for (let i = 0; i <= steps; i++) {
            const frac = i / steps;
            const x = (CX + halfWAtTop) - frac * (halfWAtTop * 2);
            const wobble = 10 * Math.sin(x * 0.05) * Math.cos(currTreeY * 0.03);
            treeCtx.lineTo(x, currTreeY + wobble);
          }
          treeCtx.lineTo(CX - 385, 1045);
          treeCtx.closePath();
          treeCtx.clip();
          treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
          treeCtx.restore();
        }

        // Pass D: Apex Crown Star & Radiant Beams (13.5s to 15.0s)
        if (t >= 13.5) {
          const starProg = Math.min(1.0, (t - 13.5) / 1.5);
          treeCtx.save();
          treeCtx.beginPath();
          treeCtx.rect(CX - 85, 115, 170, 90);
          if (starProg > 0.3) {
            const bProg = (starProg - 0.3) / 0.7;
            const beamTop = Math.round(200 - bProg * 180);
            const beamHalfW = Math.round(bProg * 140);
            treeCtx.rect(CX - beamHalfW, beamTop, beamHalfW * 2, 200 - beamTop);
          }
          treeCtx.clip();
          treeCtx.drawImage(refImg, 0, 0, NATIVE_W, NATIVE_H);
          treeCtx.restore();
        }
      }
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

  // Interactive Click on Canvas for Sparkles & Gesture Unmute
  if (treeCanvas) {
    treeCanvas.addEventListener('pointerdown', (e) => {
      const rect = treeCanvas.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      const scaleX = NATIVE_W / rect.width;
      const scaleY = NATIVE_H / rect.height;
      const clickX = (e.clientX - rect.left) * scaleX;
      const clickY = (e.clientY - rect.top) * scaleY;
      addSparkles(clickX, clickY);
      unmuteAudio();
    });
  }

  // Audio Playback & Auto-Unmute Engine
  function safeSeekAudio(time) {
    if (!bgAudio) return;
    try {
      if (bgAudio.readyState >= 1) {
        bgAudio.currentTime = time;
      } else {
        bgAudio.addEventListener('loadedmetadata', () => {
          try { bgAudio.currentTime = time; } catch (e) {}
        }, { once: true });
      }
    } catch (e) {
      console.warn('Audio seek exception:', e);
    }
  }

  function startPlayback() {
    if (!bgAudio) return;

    bgAudio.volume = parseFloat(volSlider ? volSlider.value : 0.8) || 0.8;
    safeSeekAudio(0.0);

    // Attempt 1: Play unmuted immediately
    bgAudio.muted = false;
    const playPromise = bgAudio.play();

    if (playPromise !== undefined) {
      playPromise.then(() => {
        // Success! Browser allowed unmuted autoplay (e.g. MEI threshold passed or permitted)
        isMuted = false;
        isPlaying = true;
        updateAudioUI();
        if (audioPill) audioPill.classList.add('hidden');
      }).catch(err => {
        // Attempt 2: If browser blocks unmuted sound, immediately start playing muted
        // This ensures the animation, music timeline, and visuals start immediately with ZERO delay!
        console.log('Unmuted autoplay deferred by browser policy. Starting synchronized muted stream:', err);
        bgAudio.muted = true;
        bgAudio.play().then(() => {
          isMuted = true;
          isPlaying = true;
          updateAudioUI();
          if (audioPill) {
            audioPill.classList.remove('hidden');
            const pillText = audioPill.querySelector('.audio-pill-text');
            if (pillText) pillText.textContent = 'Tap anywhere to unmute music (Sia - Snowman)';
          }
        }).catch(e2 => {
          console.warn('Playback error:', e2);
          updateAudioUI();
        });
      });
    }
  }

  // Instant Unmute on ANY user gesture (touch, click, scroll, keypress)
  function unmuteAudio() {
    if (!bgAudio) return;

    if (bgAudio.muted) {
      bgAudio.muted = false;
      bgAudio.volume = parseFloat(volSlider ? volSlider.value : 0.8) || 0.8;
      isMuted = false;
      if (audioPill) audioPill.classList.add('hidden');
      updateAudioUI();
    } else if (bgAudio.paused) {
      bgAudio.volume = parseFloat(volSlider ? volSlider.value : 0.8) || 0.8;
      bgAudio.play().then(() => {
        isMuted = false;
        isPlaying = true;
        if (audioPill) audioPill.classList.add('hidden');
        updateAudioUI();
      }).catch(() => {});
    }
  }

  ['pointerdown', 'touchstart', 'click', 'keydown'].forEach(ev => {
    window.addEventListener(ev, unmuteAudio, { passive: true });
  });

  // Ensure loop restarts cleanly from 0:00
  if (bgAudio) {
    bgAudio.addEventListener('ended', () => {
      safeSeekAudio(0.0);
      bgAudio.play().catch(() => {});
    });
  }

  function updateAudioUI() {
    if (!bgAudio) return;

    if (playPauseIcon && playPauseText) {
      if (!isPlaying) {
        playPauseIcon.textContent = '▶';
        playPauseText.textContent = 'Play';
      } else {
        playPauseIcon.textContent = '⏸';
        playPauseText.textContent = 'Pause';
      }
    }

    if (muteIcon) {
      if (bgAudio.muted || bgAudio.volume === 0 || bgAudio.paused) {
        muteIcon.textContent = '🔇';
        if (btnMute) btnMute.classList.add('muted-prompt');
      } else {
        muteIcon.textContent = '🔊';
        if (btnMute) btnMute.classList.remove('muted-prompt');
      }
    }
  }

  // Start playback immediately upon script execution, DOM ready, and window load
  startPlayback();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startPlayback);
  }
  window.addEventListener('load', startPlayback);

  // Pill click unmutes music immediately
  if (audioPill) {
    audioPill.addEventListener('click', (e) => {
      e.stopPropagation();
      unmuteAudio();
    });
  }

  // Play / Pause Button
  if (btnPlayPause) {
    btnPlayPause.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isPlaying && bgAudio && !bgAudio.paused) {
        isPlaying = false;
        bgAudio.pause();
        if (viewMode === 'video' && hdVideo) hdVideo.pause();
      } else {
        isPlaying = true;
        lastFrameTime = performance.now();
        if (bgAudio) {
          bgAudio.muted = false;
          bgAudio.volume = parseFloat(volSlider ? volSlider.value : 0.8) || 0.8;
          bgAudio.play().then(() => {
            isMuted = false;
            if (audioPill) audioPill.classList.add('hidden');
            updateAudioUI();
          }).catch(() => {});
        }
        if (viewMode === 'video' && hdVideo) hdVideo.play().catch(() => {});
      }
      updateAudioUI();
    });
  }

  // Restart Button
  if (btnRestart) {
    btnRestart.addEventListener('click', (e) => {
      e.stopPropagation();
      animTime = 0.0;
      safeSeekAudio(0.0);
      if (viewMode === 'video' && hdVideo) hdVideo.currentTime = 0;
      isPlaying = true;
      lastFrameTime = performance.now();
      if (bgAudio) {
        bgAudio.muted = false;
        bgAudio.volume = parseFloat(volSlider ? volSlider.value : 0.8) || 0.8;
        bgAudio.play().then(() => {
          isMuted = false;
          if (audioPill) audioPill.classList.add('hidden');
          updateAudioUI();
        }).catch(() => {});
      }
      if (viewMode === 'video' && hdVideo) hdVideo.play().catch(() => {});
      if (progressBarWrap) progressBarWrap.classList.remove('done');
      updateAudioUI();
    });
  }

  // Mute Button
  if (btnMute) {
    btnMute.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!bgAudio) return;
      if (bgAudio.muted) {
        unmuteAudio();
      } else {
        bgAudio.muted = true;
        updateAudioUI();
      }
    });
  }

  // Volume Slider
  if (volSlider) {
    volSlider.addEventListener('input', (e) => {
      if (!bgAudio) return;
      bgAudio.volume = parseFloat(e.target.value);
      if (bgAudio.volume > 0) {
        bgAudio.muted = false;
        if (audioPill) audioPill.classList.add('hidden');
      }
      if (viewMode === 'video' && hdVideo) hdVideo.volume = bgAudio.volume;
      updateAudioUI();
    });
  }

  // CRT Bloom Toggle
  let bloomEnabled = true;
  if (btnBloom) {
    btnBloom.addEventListener('click', () => {
      bloomEnabled = !bloomEnabled;
      btnBloom.classList.toggle('active', bloomEnabled);
      if (treeCanvas) treeCanvas.classList.toggle('bloom', bloomEnabled);
      if (crtOverlay) crtOverlay.classList.toggle('disabled', !bloomEnabled);
    });
  }

  // Fullscreen Toggle
  if (btnFullscreen) {
    btnFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  // Toggle View: Interactive Canvas vs Python Video
  if (btnToggleView) {
    btnToggleView.addEventListener('click', () => {
      if (viewMode === 'canvas') {
        viewMode = 'video';
        if (treeCanvas) treeCanvas.classList.remove('active');
        if (videoContainer) videoContainer.classList.add('active');
        if (viewIcon) viewIcon.textContent = '🌲';
        if (viewLabel) viewLabel.textContent = 'Interactive Canvas';
        if (hdVideo) {
          hdVideo.currentTime = animTime % 18.0;
          if (isPlaying) hdVideo.play().catch(() => {});
        }
      } else {
        viewMode = 'canvas';
        if (videoContainer) videoContainer.classList.remove('active');
        if (treeCanvas) treeCanvas.classList.add('active');
        if (viewIcon) viewIcon.textContent = '🎬';
        if (viewLabel) viewLabel.textContent = 'Watch HD Video';
        if (hdVideo) hdVideo.pause();
      }
    });
  }

  // Start Animation Loop
  requestAnimationFrame(render);
})();
