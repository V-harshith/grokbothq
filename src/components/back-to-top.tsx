"use client";

import { useEffect, useState } from "react";

/** Floating back-to-top button - appears after the first viewport of scroll. */
export function BackToTop() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    function onScroll() {
      setShow(window.scrollY > window.innerHeight);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (!show) return null;

  return (
    <button
      type="button"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      aria-label="Back to top"
      className="fixed bottom-4 right-4 z-[60] hidden max-sm:hidden rounded-full border border-border bg-surface p-3 text-muted shadow-xl transition-colors hover:border-accent hover:text-foreground sm:block"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
        <path d="M12 19V5M5 12l7-7 7 7" />
      </svg>
    </button>
  );
}
