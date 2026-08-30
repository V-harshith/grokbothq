"use client";

import type { Bot } from "@/data/bots";

/**
 * The Open in Grok button. Fires a Umami event per bot when analytics are
 * active, so install interest is measurable without any backend of our own.
 */
export function OpenButton({ bot, small }: { bot: Bot; small?: boolean }) {
  function track() {
    const w = window as unknown as { umami?: { track: (name: string, data: object) => void } };
    try {
      w.umami?.track("install-click", { bot: bot.slug });
    } catch {
      /* analytics are optional */
    }
  }

  return (
    <a
      href={bot.url}
      target="_blank"
      rel="noopener noreferrer nofollow"
      onClick={track}
      className={`btn btn-accent ${small ? "!px-3 !py-1.5 !text-xs" : ""}`}
      aria-label={`Open ${bot.name} in Grok`}
    >
      Open in Grok
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
        <path d="M7 17 17 7M9 7h8v8" />
      </svg>
    </a>
  );
}
