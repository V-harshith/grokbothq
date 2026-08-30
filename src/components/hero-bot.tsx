"use client";

import { useEffect, useRef } from "react";

/**
 * The GrokBot HQ mascot: a 3D-tilting bot head that floats, follows the
 * cursor with its eyes, and blinks on its own randomized schedule.
 * Pure CSS transforms driven by two rAF-lerped CSS vars — no libraries.
 */
export function HeroBot() {
  const headRef = useRef<HTMLDivElement>(null);
  const eyesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const head = headRef.current;
    const eyes = eyesRef.current;
    if (!head || !eyes) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    // each eye (and the antenna light) gets its own blink rhythm
    head.style.setProperty("--bd", `${(4.5 + Math.random() * 2.5).toFixed(2)}s`);
    head.style.setProperty("--bdel", `${(Math.random() * 4).toFixed(2)}s`);
    for (const eye of eyes.children) {
      (eye as HTMLElement).style.setProperty("--bd", `${(4.5 + Math.random() * 2.5).toFixed(2)}s`);
      (eye as HTMLElement).style.setProperty("--bdel", `${(Math.random() * 4).toFixed(2)}s`);
    }

    const target = { rx: 0, ry: 0, ex: 0, ey: 0 };
    const current = { rx: 0, ry: 0, ex: 0, ey: 0 };
    let raf = 0;
    let visible = true;

    const onMove = (e: MouseEvent) => {
      const nx = (e.clientX / window.innerWidth) * 2 - 1;
      const ny = (e.clientY / window.innerHeight) * 2 - 1;
      target.ry = nx * 16;
      target.rx = -ny * 10;
      target.ex = nx * 7;
      target.ey = ny * 5;
    };

    const tick = () => {
      if (visible && !document.hidden) {
        current.rx += (target.rx - current.rx) * 0.08;
        current.ry += (target.ry - current.ry) * 0.08;
        current.ex += (target.ex - current.ex) * 0.12;
        current.ey += (target.ey - current.ey) * 0.12;
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
        <div className="hero-bot-antenna" />
        <div ref={eyesRef} className="hero-bot-eyes">
          <div className="hero-bot-eye" />
          <div className="hero-bot-eye" />
        </div>
      </div>
      <div className="hero-bot-shadow" />
    </div>
  );
}
