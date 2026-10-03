import type { Bot } from "./types";
import botsJson from "../../content/bots.json";
import metricsJson from "../../content/metrics.json";

export type { Bot };

type MetricsFile = { updatedAt?: string; opens?: Record<string, number>; sponsorClicks?: number; sponsors?: Record<string, number> };
const metrics = metricsJson as MetricsFile;

/** Live per-bot open counts (Open-button clicks) from the daily metrics pipeline. */
export function botOpens(slug: string): number {
  return metrics.opens?.[slug] ?? 0;
}

/** Only published bots are rendered; pending/spam entries never reach the site. */
export const bots: Bot[] = (botsJson as Bot[]).filter((b) => (b as { status?: string }).status !== "pending");

export const botMap = new Map(bots.map((b) => [b.slug, b]));

export function getBot(slug: string): Bot | undefined {
  return botMap.get(slug);
}

export function botsByCategory(categorySlug: string): Bot[] {
  return bots.filter((b) => b.category === categorySlug);
}

/**
 * Same-category neighbours as a rotating window from this bot's position, so the tail of a big
 * category still receives links. Taking the first N instead gave every page in a category the same
 * two companions (engineering: every page shared one pair) and left the rest unreachable from each
 * other.
 */
export function relatedBots(bot: Bot, count = 4): Bot[] {
  const all = botsByCategory(bot.category);
  const same = all.filter((b) => b.slug !== bot.slug);
  if (same.length <= count) return same;
  const idx = all.findIndex((b) => b.slug === bot.slug);
  const start = idx < 0 ? 0 : idx % same.length;
  return Array.from({ length: count }, (_, i) => same[(start + i) % same.length]);
}

/**
 * How many published listings share each name (case-insensitive). 77 names do: "Chief of Staff"
 * appears 53 times, built by 53 different people. They are distinct bots, not duplicates — so the
 * fix is to say which one this is, never to delist them.
 */
const nameCounts = (() => {
  const m = new Map<string, number>();
  for (const b of bots) {
    const key = b.name.trim().toLowerCase();
    m.set(key, (m.get(key) ?? 0) + 1);
  }
  return m;
})();

/** Names shared by more than one listing. */
export function nameCount(bot: Bot): number {
  return nameCounts.get(bot.name.trim().toLowerCase()) ?? 1;
}

export function nameCollides(bot: Bot): boolean {
  return nameCount(bot) > 1;
}

/** Position among this category's listings that publish install counts (null when none do). */
export function installRank(bot: Bot): { rank: number; of: number } | null {
  if (typeof bot.installs !== "number") return null;
  const peers = botsByCategory(bot.category)
    .filter((b) => typeof b.installs === "number")
    .sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0));
  const i = peers.findIndex((b) => b.slug === bot.slug);
  return i < 0 ? null : { rank: i + 1, of: peers.length };
}

export function latestBots(count = 8): Bot[] {
  return [...bots].sort((a, b) => b.addedAt.localeCompare(a.addedAt)).slice(0, count);
}

/**
 * Every listing, newest first — the full chronological series behind `/new` (the page paginates it
 * 60 at a time; server-rendering all of it was a 10 MB document).
 */
export const newBots: Bot[] = [...bots].sort((a, b) => b.addedAt.localeCompare(a.addedAt));

export function newThisWeek(count = 4): Bot[] {
  const week = 7 * 86_400_000;
  const now = Date.now();
  return bots
    .filter((b) => now - new Date(b.addedAt).getTime() < week)
    .sort((a, b) => b.addedAt.localeCompare(a.addedAt))
    .slice(0, count);
}

export type BotPreview = Pick<
  Bot,
  "slug" | "name" | "builder" | "tagline" | "description" | "category" | "url" | "addedAt" | "installs" | "hue"
>;

export function previewBots(limit?: number): BotPreview[] {
  const slice = typeof limit === "number" ? bots.slice(0, limit) : bots;
  return slice.map((b) => ({
    slug: b.slug,
    name: b.name,
    builder: b.builder,
    tagline: b.tagline,
    description: b.description,
    category: b.category,
    url: b.url,
    addedAt: b.addedAt,
    installs: b.installs,
    hue: b.hue,
  }));
}

export function topInstalledBots(count = 6): Bot[] {
  return [...bots]
    .filter((b) => typeof b.installs === "number")
    .sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0))
    .slice(0, count);
}

const today = () => new Date().toISOString().slice(0, 10);

/** Featured placements auto-expire via featuredUntil - no manual takedowns needed. */
export function featuredBots(): Bot[] {
  const now = today();
  return bots.filter((b) => b.featured && (!b.featuredUntil || b.featuredUntil >= now));
}

/**
 * Exact counts for the whole directory. The interactive browser on `/bots` holds only the newest
 * listings (sending all 2,594 to the client was a 1.5 MB React payload), so it needs the true totals
 * to label what it is showing without understating the directory.
 */
export function categoryTotals(): { all: number; byCategory: Record<string, number> } {
  const byCategory: Record<string, number> = {};
  for (const b of bots) byCategory[b.category] = (byCategory[b.category] ?? 0) + 1;
  return { all: bots.length, byCategory };
}

export const stats = {
  bots: bots.length,
  // Only listings with a known builder handle count; an empty handle is not a
  // builder and would otherwise inflate this by one.
  builders: new Set(bots.map((b) => b.builder.x).filter(Boolean)).size,
  categories: new Set(bots.map((b) => b.category)).size,
};
