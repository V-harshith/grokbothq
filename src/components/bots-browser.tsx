"use client";

import { useMemo, useState } from "react";
import type { BotPreview } from "@/data/bots";
import { categories } from "@/data/categories";
import { BotCard } from "./bot-card";

export function BotsBrowser({ bots, initialCategory = "all" }: { bots: BotPreview[]; initialCategory?: string }) {
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(initialCategory);
  const [visible, setVisible] = useState(60);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return bots.filter((bot) => {
      const inCategory = active === "all" || bot.category === active;
      if (!inCategory) return false;
      if (!q) return true;
      return (
        bot.name.toLowerCase().includes(q) ||
        bot.tagline.toLowerCase().includes(q) ||
        bot.description.toLowerCase().includes(q) ||
        bot.builder.name.toLowerCase().includes(q) ||
        bot.builder.x.toLowerCase().includes(q)
      );
    });
  }, [bots, query, active]);

  const tabs = [{ slug: "all", name: "All" }, ...categories.map((c) => ({ slug: c.slug, name: c.name }))];

  return (
    <div>
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div role="tablist" aria-label="Filter bots by category" className="flex flex-wrap gap-1.5">
          {tabs.map((tab) => (
              <button
                key={tab.slug}
                role="tab"
                aria-selected={active === tab.slug}
                onClick={() => {
                  setActive(tab.slug);
                  setVisible(60);
                }}
              className={`rounded-[10px] px-3 py-1.5 text-xs font-semibold transition-colors ${
                active === tab.slug
                  ? "bg-accent text-accent-foreground"
                  : "border border-border text-muted hover:border-[var(--border-hov)] hover:text-foreground"
              }`}
            >
              {tab.name}
            </button>
          ))}
        </div>

        <div className="relative md:w-64">
          <svg
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted"
            width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden
          >
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>
          <input
            id="bot-search"
            type="search"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setVisible(60);
            }}
            placeholder="Search bots…"
            aria-label="Search bots"
            className="w-full rounded-lg border border-border bg-surface py-2 pl-9 pr-3 text-sm outline-none placeholder:text-muted focus:border-accent"
          />
        </div>
      </div>

      <p className="mt-4 text-xs text-muted" role="status">
        {filtered.length} bot{filtered.length === 1 ? "" : "s"}
        {active !== "all" && ` in ${tabs.find((t) => t.slug === active)?.name}`}
        {query && ` matching “${query}”`}
      </p>

      <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.slice(0, visible).map((bot) => (
          <BotCard key={bot.slug} bot={bot} />
        ))}
      </div>

      {visible < filtered.length && (
        <div className="mt-8 text-center">
          <p className="text-sm text-muted">
            Showing {Math.min(visible, filtered.length)} of {filtered.length} bots
          </p>
          <button type="button" onClick={() => setVisible((v) => v + 60)} className="btn btn-ghost mt-3">
            Show more bots
          </button>
        </div>
      )}

      {filtered.length === 0 && (
        <div className="card mt-6 p-10 text-center text-sm text-muted">
          No bots match that search - try a different term or category.
        </div>
      )}
    </div>
  );
}
