"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

const PILL_KEY = "gbh-bookmark-pill";
const MONTH = 30 * 24 * 60 * 60 * 1000;

/**
 * The bookmark layer: a dismissible "Bookmark GrokBot HQ" pill (bottom-left),
 * a Ctrl/Cmd+D detector that thanks you the moment you bookmark, and the "/"
 * shortcut that jumps focus to the directory search.
 */
export function SiteKeys() {
  const pathname = usePathname();
  const [showPill, setShowPill] = useState(false);
  const [thanked, setThanked] = useState(false);

  useEffect(() => {
    function isTyping() {
      const el = document.activeElement;
      return (
        el instanceof HTMLElement &&
        (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT" || el.isContentEditable)
      );
    }

    function onKeyDown(e: KeyboardEvent) {
      // Ctrl/Cmd + D - the browser's own dialog opens alongside; we just say thanks
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "d") {
        setThanked(true);
        setShowPill(false);
        try {
          localStorage.setItem(PILL_KEY, String(Date.now() + MONTH));
        } catch {}
        setTimeout(() => setThanked(false), 2600);
        return;
      }
      // "/" focuses the directory search
      if (e.key === "/" && !e.ctrlKey && !e.metaKey && !e.altKey && !isTyping()) {
        if (pathname === "/bots") {
          const input = document.getElementById("bot-search");
          if (input) {
            e.preventDefault();
            input.focus();
          }
        }
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [pathname]);

  useEffect(() => {
    try {
      const until = Number(localStorage.getItem(PILL_KEY) ?? 0);
      if (Date.now() < until) return;
    } catch {}
    const t = setTimeout(() => setShowPill(true), 4000);
    return () => clearTimeout(t);
  }, []);

  function dismiss() {
    setShowPill(false);
    try {
      localStorage.setItem(PILL_KEY, String(Date.now() + MONTH));
    } catch {}
  }

  return (
    <>
      {showPill && (
        <aside
          className="fixed bottom-4 left-4 z-[60] flex items-center gap-3 rounded-full border border-border bg-surface py-2 pl-4 pr-2 shadow-xl max-sm:left-3 max-sm:right-3"
          role="complementary"
          aria-label="Bookmark this site"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="shrink-0 text-accent" aria-hidden>
            <path d="M12 2.5l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.3l-5.8 3.1 1.1-6.5L2.6 9.3l6.5-.9L12 2.5z" />
          </svg>
          <p className="text-xs text-muted">
            <span className="font-medium text-foreground">Bookmark GrokBot HQ</span>
            <span className="ml-2 hidden sm:inline">
              press{" "}
              <kbd className="rounded border border-border bg-elevated px-1.5 py-0.5 font-mono text-[10px]">
                Ctrl D
              </kbd>
            </span>
          </p>
          <button
            type="button"
            onClick={dismiss}
            aria-label="Dismiss bookmark reminder"
            className="ml-1 rounded-full p-1.5 text-muted hover:text-foreground"
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
              <path d="M6 6l12 12M18 6 6 18" />
            </svg>
          </button>
        </aside>
      )}
      {thanked && (
        <div
          className="fixed bottom-4 left-4 z-[61] flex items-center gap-2 rounded-full border border-border bg-surface px-4 py-2.5 shadow-xl"
          role="status"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="text-accent" aria-hidden>
            <path d="M12 2.5l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5L12 17.3l-5.8 3.1 1.1-6.5L2.6 9.3l6.5-.9L12 2.5z" />
          </svg>
          <p className="text-xs font-medium">Bookmarked. Thanks - see you in the feed.</p>
        </div>
      )}
    </>
  );
}
