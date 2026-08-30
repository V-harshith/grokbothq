import { bots } from "@/data/bots";

export type Integration = { slug: string; name: string; count: number; bots: string[] };

const NAMES: Record<string, string> = {
  gmail: "Gmail",
  "google-calendar": "Google Calendar",
  "google-drive": "Google Drive",
  "google-slides": "Google Slides",
  slack: "Slack",
  notion: "Notion",
  github: "GitHub",
  youtube: "YouTube",
  reddit: "Reddit",
  linkedin: "LinkedIn",
  threads: "Threads",
  figma: "Figma",
  "claude-code": "Claude Code",
  "hacker-news": "Hacker News",
  firecrawl: "Firecrawl",
  convex: "Convex",
  x: "X",
  granola: "Granola",
};

export function integrationName(slug: string): string {
  return NAMES[slug] ?? slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/** All integrations that at least one listed bot connects to, biggest first. */
export function allIntegrations(): Integration[] {
  const map = new Map<string, string[]>();
  for (const bot of bots) {
    for (const tool of bot.integrations ?? []) {
      const list = map.get(tool) ?? [];
      list.push(bot.slug);
      map.set(tool, list);
    }
  }
  return [...map.entries()]
    .map(([slug, slugs]) => ({ slug, name: integrationName(slug), count: slugs.length, bots: slugs }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));
}

export function integrationBySlug(slug: string): Integration | undefined {
  return allIntegrations().find((i) => i.slug === slug);
}
