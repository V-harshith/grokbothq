"use client";

import { useEffect, useRef } from "react";

/**
 * The GrokBot HQ mascot, modeled on the Grok app bot: a dark squircle head
 * with two glowing pill eyes. It stays anchored in place (no vertical bob);
 * the head tilts along a circular arc that tracks the cursor, the eyes follow,
 * and it blinks and glances around when the cursor is idle. Transform-only,
 * no layout animation, no libraries.
 */
export function HeroBot() {
  const headRef = useRef<HTMLDivElement>(null);
  const eyesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const head = headRef.current;
    const eyes = eyesRef.current;
    if (!head || !eyes) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    // squishy blink on its own schedule, eyes slightly out of phase
    for (const el of eyes.children) {
      const node = el as HTMLElement;
      node.style.setProperty("--bd", `${(3.6 + Math.random() * 3).toFixed(2)}s`);
      node.style.setProperty("--bdel", `${(Math.random() * 4).toFixed(2)}s`);
    }

    const target = { rx: 0, ry: 0, ex: 0, ey: 0 };
    const current = { rx: 0, ry: 0, ex: 0, ey: 0 };
    let raf = 0;
    let visible = true;
    let lastMove = 0;
    let lastGlance = 0;

    // the head's tilt traces the cursor around it like a circular dial
    const onMove = (e: MouseEvent) => {
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = (e.clientY / window.innerHeight) * 2 - 1;
      const ang = Math.atan2(ny, nx);
      const mag = Math.min(Math.hypot(nx, ny), 1);
      target.ry = Math.cos(ang) * mag * 16;
      target.rx = -Math.sin(ang) * mag * 11;
      target.ex = Math.cos(ang) * mag * 7;
      target.ey = Math.sin(ang) * mag * 5;
      lastMove = performance.now();
    };

    // when the cursor goes quiet, it looks around on its own
    const glance = (now: number) => {
      if (now - lastMove < 2500 || now - lastGlance < 2200) return;
      lastGlance = now;
      const ang = Math.random() * Math.PI * 2;
      target.ex = Math.cos(ang) * 7;
      target.ey = Math.sin(ang) * 4;
      target.ry = Math.cos(ang) * 9;
      target.rx = -Math.sin(ang) * 5;
    };

    const tick = () => {
      const now = performance.now();
      if (visible && !document.hidden) {
        glance(now);
        current.rx += (target.rx - current.rx) * 0.06;
        current.ry += (target.ry - current.ry) * 0.06;
        current.ex += (target.ex - current.ex) * 0.1;
        current.ey += (target.ey - current.ey) * 0.1;
        head.style.setProperty("--rx", `${current.rx.toFixed(2)}deg`);
        head.style.setProperty("--ry", `${current.ry.toFixed(2)}deg`);
        eyes.style.transform = `translate(${current.ex.toFixed(2)}px, ${current.ey.toFixed(2)}px)`;
      }
      raf = requestAnimationFrame(tick);
    };

    const io = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
    });
    io.observe(head);

    window.addEventListener("mousemove", onMove, { passive: true });
    raf = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener("mousemove", onMove);
      io.disconnect();
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div className="hero-bot" aria-hidden>
      <div ref={headRef} className="hero-bot-head" style={{ "--rx": "0deg", "--ry": "0deg" } as React.CSSProperties}>
        <div ref={eyesRef} className="hero-bot-eyes">
          <div className="hero-bot-eye" />
          <div className="hero-bot-eye" />
        </div>
      </div>
      <div className="hero-bot-shadow" />
    </div>
  );
}
