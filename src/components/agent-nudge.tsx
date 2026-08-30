"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

const KEY = "gbh-nudge-cooldown";
const WEEK = 7 * 24 * 60 * 60 * 1000;

/**
 * Ambient CTA, built on the four nudge rules: never on first paint (appears
 * only past ~40% scroll depth), never covers the page (small corner card,
 * slim strip on mobile), dismissal means dismissed (7-day cooldown), and it
 * stays out of the homepage - the hero already makes the same ask.
 */
export function AgentNudge() {
  const pathname = usePathname();
  const [show, setShow] = useState(false);

  useEffect(() => {
    setShow(false);
    if (pathname === "/") return;
    try {
      const until = Number(localStorage.getItem(KEY) ?? 0);
      if (Date.now() < until) return;
    } catch {
      /* storage blocked - show the nudge, dismissal just won't persist */
    }

    function onScroll() {
      const doc = document.documentElement;
      const scrollable = doc.scrollHeight - window.innerHeight;
      if (scrollable <= 0) return;
      if (window.scrollY / scrollable >= 0.4) {
        setShow(true);
        window.removeEventListener("scroll", onScroll);
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [pathname]);

  function dismiss() {
    setShow(false);
    try {
      localStorage.setItem(KEY, String(Date.now() + WEEK));
    } catch {}
  }

  if (!show) return null;

  return (
    <aside
      className="fixed bottom-4 right-4 z-[60] w-72 rounded-xl border border-border bg-surface p-4 shadow-2xl max-sm:bottom-0 max-sm:right-0 max-sm:w-full max-sm:rounded-b-none"
      role="complementary"
      aria-label="Agent routines"
    >
      <button
        type="button"
        onClick={dismiss}
        aria-label="Dismiss"
        className="absolute right-3 top-3 text-muted hover:text-foreground"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
          <path d="M6 6l12 12M18 6 6 18" />
        </svg>
      </button>
      <p className="text-sm font-semibold">Your Grok Bot can read this site</p>
      <p className="mt-1 text-xs leading-relaxed text-muted">
        One copied prompt turns it into a client of the directory.
      </p>
      <Link href="/agent" onClick={dismiss} className="btn btn-accent mt-3 !py-1.5 !text-xs">
        Get the routines →
      </Link>
    </aside>
  );
}
