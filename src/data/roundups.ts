import type { Bot } from "./types";
import { bots, botsByCategory, latestBots } from "./bots";
import { categoryMap } from "./categories";
import roundupsJson from "../../content/roundups.json";

/**
 * Category roundups: comparison pages that answer "which of these should I open?" for the categories
 * where there is enough real data to answer it.
 *
 * The authored prose in content/roundups.json states structure (what the category is, what the
 * listings contain, how to judge one) and deliberately avoids counts, because counts drift. Every
 * number rendered on the page is computed here from the current data.
 */

export type Roundup = {
  slug: string;
  /** category slug this roundup covers */
  category: string;
  title: string;
  seoTitle: string;
  description: string;
  updatedAt: string;
  intro: string;
  howWePicked: string[];
  sections: { heading: string; body: string[] }[];
  faqs: { q: string; a: string }[];
};

export const roundups = roundupsJson as Roundup[];
export const roundupMap = new Map(roundups.map((r) => [r.slug, r]));
export const roundupByCategory = new Map(roundups.map((r) => [r.category, r]));

export type RoundupFacts = {
  categoryName: string;
  total: number;
  builders: number;
  /** listings whose source listing publishes install counts */
  withInstalls: number;
  withIntegrations: number;
  withFeatures: number;
  withSource: number;
  addedLast7: number;
  topIntegrations: { slug: string; count: number }[];
  ranked: Bot[];
  newest: Bot[];
};

export function roundupFacts(categorySlug: string): RoundupFacts {
  const items = botsByCategory(categorySlug);
  const builders = new Set(items.map((b) => b.builder.x || b.builder.name).filter(Boolean));
  const integrationCounts = new Map<string, number>();
  for (const b of items) {
    for (const slug of b.integrations ?? []) {
      integrationCounts.set(slug, (integrationCounts.get(slug) ?? 0) + 1);
    }
  }
  const weekAgo = new Date(Date.now() - 7 * 86_400_000).toISOString().slice(0, 10);
  return {
    categoryName: categoryMap.get(categorySlug)?.name ?? categorySlug,
    total: items.length,
    builders: builders.size,
    withInstalls: items.filter((b) => typeof b.installs === "number").length,
    withIntegrations: items.filter((b) => (b.integrations ?? []).length > 0).length,
    withFeatures: items.filter((b) => (b.features ?? []).length > 0).length,
    withSource: items.filter((b) => Boolean(b.source)).length,
    addedLast7: items.filter((b) => b.addedAt >= weekAgo).length,
    topIntegrations: [...integrationCounts.entries()]
      .map(([slug, count]) => ({ slug, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 6),
    ranked: [...items].filter((b) => typeof b.installs === "number").sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0)).slice(0, 10),
    newest: [...items].sort((a, b) => b.addedAt.localeCompare(a.addedAt)).slice(0, 6),
  };
}

/** How many listings in the whole directory the given category represents, for an honest context line. */
export function categoryShare(categorySlug: string): number {
  return Math.round((botsByCategory(categorySlug).length / Math.max(bots.length, 1)) * 100);
}

export { latestBots };
