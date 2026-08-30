"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { BotFace } from "./bot-face";

export type RouletteBot = { slug: string; name: string; tagline: string; category: string; url: string };

/**
 * "Surprise me" - cycles bot faces slot-machine style and lands on one.
 * Pure client-side theater over the real directory. Reduced motion skips
 * the roll and picks instantly.
 */
export function BotRoulette({ bots }: { bots: RouletteBot[] }) {
  const [phase, setPhase] = useState<"idle" | "rolling" | "done">("idle");
  const [current, setCurrent] = useState<RouletteBot | null>(null);
  const result = useRef<RouletteBot | null>(null);
  const timers = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => () => { if (timers.current) clearInterval(timers.current); }, []);

  function roll() {
    if (!bots.length) return;
    result.current = bots[Math.floor(Math.random() * bots.length)];
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setCurrent(result.current);
      setPhase("done");
      return;
    }
    setPhase("rolling");
    let ticks = 0;
    const delay = 70;
    const iv = setInterval(() => {
      ticks++;
      setCurrent(bots[Math.floor(Math.random() * bots.length)]);
      if (ticks >= 16) {
        clearInterval(iv);
        timers.current = null;
        setCurrent(result.current);
        setPhase("done");
      }
    }, delay);
    timers.current = iv;
  }

  return (
    <>
      <button type="button" onClick={roll} className="btn btn-ghost !px-6 !py-3 !text-base">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden>
          <rect x="3" y="3" width="18" height="18" rx="5" />
          <circle cx="8.2" cy="8.2" r="1.4" fill="currentColor" stroke="none" />
          <circle cx="15.8" cy="15.8" r="1.4" fill="currentColor" stroke="none" />
          <circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none" />
        </svg>
        Surprise me
      </button>

      {phase !== "idle" && current && (
        <div
          className="fixed inset-0 z-[70] grid place-items-center bg-black/70 p-4 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label="Random Grok bot"
          onClick={() => setPhase("idle")}
        >
          <div className="card relative w-full max-w-md p-8 text-center" onClick={(e) => e.stopPropagation()}>
            <div className="mx-auto w-fit" style={phase === "rolling" ? { opacity: 0.9 } : undefined}>
              <BotFace slug={current.slug} name={current.name} size={96} />
            </div>
            <p className="kicker mt-5 !text-[10px]">{phase === "rolling" ? "Rolling the directory…" : "Tonight's pick"}</p>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight">{current.name}</h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">{current.tagline}</p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <a href={current.url} target="_blank" rel="noopener noreferrer nofollow" className="btn btn-accent">
                Open in Grok
              </a>
              <Link href={`/bots/${current.slug}`} onClick={() => setPhase("idle")} className="btn btn-ghost">
                Details
              </Link>
            </div>
            <button
              type="button"
              onClick={roll}
              className="mt-4 text-xs font-medium text-muted underline underline-offset-4 hover:text-foreground"
            >
              Roll again
            </button>
            <button
              type="button"
              onClick={() => setPhase("idle")}
              aria-label="Close"
              className="absolute right-4 top-4 text-muted hover:text-foreground"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
                <path d="M6 6l12 12M18 6 6 18" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  );
}
