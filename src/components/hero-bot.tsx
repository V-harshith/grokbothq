"use client";

import { useEffect, useRef } from "react";

/**
 * The GrokBot HQ mascot: an anchored dark head shell whose face is a canvas
 * dot-matrix display. Dots brighten near the cursor, a quiet scan line sweeps
 * every few seconds, the eyes blink on their own schedule, and the head tilts
 * along a circular arc that tracks the pointer. Transform-only motion.
 */
export function HeroBot() {
  const headRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const head = headRef.current;
    const canvas = canvasRef.current;
    if (!head || !canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const COLS = 20;
    const ROWS = 14;
    const EYE_COLS = [6, 7, 12, 13]; // lit dot columns for the eyes
    const EYE_ROWS = [4, 5, 6, 7, 8, 9];

    const target = { rx: 0, ry: 0, px: 0.5, py: 0.5 };
    const current = { rx: 0, ry: 0, px: 0.5, py: 0.5 };
    let raf = 0;
    let visible = true;
    let lastMove = 0;
    let lastGlance = 0;

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function resize() {
      const rect = head!.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas!.width = rect.width * dpr;
      canvas!.height = rect.height * dpr;
      canvas!.style.width = `${rect.width}px`;
      canvas!.style.height = `${rect.height}px`;
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(head);

    const onMove = (e: MouseEvent) => {
      const rect = canvas!.getBoundingClientRect();
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = (e.clientY / window.innerHeight) * 2 - 1;
      target.ry = nx * 14;
      target.rx = -ny * 9;
      target.px = Math.min(Math.max((e.clientX - rect.left) / rect.width, 0), 1);
      target.py = Math.min(Math.max((e.clientY - rect.top) / rect.height, 0), 1);
      lastMove = performance.now();
    };
    window.addEventListener("mousemove", onMove, { passive: true });

    // when the cursor goes quiet, the display looks around on its own
    function glance() {
      target.px = 0.15 + Math.random() * 0.7;
      target.py = 0.25 + Math.random() * 0.5;
      target.ry = (target.px - 0.5) * 18;
      target.rx = -(target.py - 0.5) * 10;
    }

    const io = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
    });
    io.observe(head);

    const blinkPeriod = 4200;
    const blinkOffset = Math.random() * blinkPeriod;

    function draw(now: number) {
      const w = canvas!.clientWidth;
      const h = canvas!.clientHeight;
      ctx!.clearRect(0, 0, w, h);

      const sx = w / (COLS + 1);
      const sy = h / (ROWS + 1);

      // quiet scan line sweeping down the panel
      const scanRow = reduced ? -5 : ((now / 4500) % 1) * (ROWS + 8) - 4;

      // blink: every blinkPeriod the eyes compress for a moment
      const bt = ((now + blinkOffset) % blinkPeriod) / blinkPeriod;
      const blinking = !reduced && bt > 0.96;

      // focus point in grid space (cursor or idle glance)
      const focusX = current.px * (COLS - 1);
      const focusY = current.py * (ROWS - 1);

      for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
          const isEye = EYE_COLS.includes(c) && EYE_ROWS.includes(r);
          const dx = c - focusX;
          const dy = r - focusY;
          const dist = Math.hypot(dx * 0.8, dy);
          let alpha = isEye ? 0.95 : 0.13;
          let radius = isEye ? 2.6 : 1.5;

          // proximity glow around the focus point
          const glow = Math.max(0, 1 - dist / 5.5);
          alpha = Math.min(1, alpha + glow * (isEye ? 0.05 : 0.55));
          radius += glow * (isEye ? 0.4 : 0.9);

          // scan line brightness
          const scanDist = Math.abs(r - scanRow);
          if (scanDist < 1.2) alpha = Math.min(1, alpha + (1.2 - scanDist) * 0.35);

          // blink squashes the eyes into a thin row
          if (isEye && blinking) {
            if (r !== 6) continue;
            radius = 2.2;
          }

          const x = sx * (c + 1);
          const y = sy * (r + 1);
          ctx!.beginPath();
          ctx!.fillStyle = `rgba(255, 255, 255, ${alpha.toFixed(3)})`;
          ctx!.arc(x, y, radius, 0, Math.PI * 2);
          ctx!.fill();
        }
      }
    }

    const tick = () => {
      const now = performance.now();
      if (visible && !document.hidden) {
        if (now - lastMove > 2500 && now - lastGlance > 2200) {
          lastGlance = now;
          glance();
        }
        current.rx += (target.rx - current.rx) * 0.06;
        current.ry += (target.ry - current.ry) * 0.06;
        current.px += (target.px - current.px) * 0.1;
        current.py += (target.py - current.py) * 0.1;
        head!.style.setProperty("--rx", `${current.rx.toFixed(2)}deg`);
        head!.style.setProperty("--ry", `${current.ry.toFixed(2)}deg`);
        draw(now);
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener("mousemove", onMove);
      io.disconnect();
      ro.disconnect();
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div className="hero-bot" aria-hidden>
      <div ref={headRef} className="hero-bot-head" style={{ "--rx": "0deg", "--ry": "0deg" } as React.CSSProperties}>
        <canvas ref={canvasRef} className="absolute inset-3 rounded-[26px]" />
      </div>
      <div className="hero-bot-shadow" />
    </div>
  );
}
