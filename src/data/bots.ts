import type { Bot } from "./types";
import botsJson from "../../content/bots.json";
import metricsJson from "../../content/metrics.json";

export type { Bot };

type MetricsFile = { updatedAt?: string; opens?: Record<string, number>; sponsorClicks?: number };
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

export function relatedBots(bot: Bot, count = 4): Bot[] {
  const same = botsByCategory(bot.category).filter((b) => b.slug !== bot.slug);
  return same.slice(0, count);
}

export function latestBots(count = 8): Bot[] {
  return [...bots].sort((a, b) => b.addedAt.localeCompare(a.addedAt)).slice(0, count);
}

const today = () => new Date().toISOString().slice(0, 10);

/** Featured placements auto-expire via featuredUntil - no manual takedowns needed. */
export function featuredBots(): Bot[] {
  const now = today();
  return bots.filter((b) => b.featured && (!b.featuredUntil || b.featuredUntil >= now));
}

export const stats = {
  bots: bots.length,
  builders: new Set(bots.map((b) => b.builder.x)).size,
  categories: new Set(bots.map((b) => b.category)).size,
};
