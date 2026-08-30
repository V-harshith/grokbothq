"use client";

import { useEffect, useRef } from "react";

/**
 * The GrokBot HQ mascot, modeled on the Grok app bot: a dark squircle head
 * with two glowing pill eyes. It bobs on transform-only keyframes, tilts in
 * 3D toward the cursor, glances around on its own when the cursor is idle,
 * and blinks with a squishy overshoot. No libraries, no layout animation.
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
    for (const el of [head, eyes.children[0], eyes.children[1]]) {
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

    const onMove = (e: MouseEvent) => {
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = (e.clientY / window.innerHeight) * 2 - 1;
      target.ry = nx * 14;
      target.rx = -ny * 9;
      target.ex = nx * 6;
      target.ey = ny * 4;
      lastMove = performance.now();
    };

    // when the cursor goes quiet, the bot looks around on its own
    const glance = (now: number) => {
      if (now - lastMove < 2500 || now - lastGlance < 2200) return;
      lastGlance = now;
      target.ex = (Math.random() * 2 - 1) * 7;
      target.ey = (Math.random() * 2 - 1) * 4;
      target.ry = (Math.random() * 2 - 1) * 9;
      target.rx = (Math.random() * 2 - 1) * 5;
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
      <div className="hero-bot-float">
        <div ref={headRef} className="hero-bot-head" style={{ "--rx": "0deg", "--ry": "0deg" } as React.CSSProperties}>
          <div ref={eyesRef} className="hero-bot-eyes">
            <div className="hero-bot-eye" />
            <div className="hero-bot-eye" />
          </div>
        </div>
      </div>
      <div className="hero-bot-shadow" />
    </div>
  );
}
