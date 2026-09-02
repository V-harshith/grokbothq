import { bots, stats } from "@/data/bots";
import { allIntegrations } from "@/lib/integrations";
import { SITE } from "@/data/site";

/**
 * "State of Grok Bots" - original citable statistics computed from the
 * directory itself. Regenerated at build time; every number traces back to
 * content/bots.json.
 */
export function siteStats() {
  const perCategory = new Map<string, number>();
  for (const b of bots) perCategory.set(b.category, (perCategory.get(b.category) ?? 0) + 1);

  const integrations = allIntegrations().slice(0, 8);

  const installsTotal = bots.reduce((a, b) => a + (b.installs ?? 0), 0);
  const topInstalled = [...bots]
    .filter((b) => typeof b.installs === "number" && b.installs > 0)
    .sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0))
    .slice(0, 5);

  // weekly additions, last 8 weeks (oldest first)
  const now = Date.now();
  const weeks = Array.from({ length: 8 }, (_, i) => {
    const start = now - (8 - i) * 7 * 86_400_000;
    const end = start + 7 * 86_400_000;
    const count = bots.filter((b) => {
      const t = new Date(b.addedAt).getTime();
      return t >= start && t < end;
    }).length;
    return { label: `W-${8 - i}`, count };
  });

  const last7 = bots.filter((b) => now - new Date(b.addedAt).getTime() < 7 * 86_400_000).length;
  const last30 = bots.filter((b) => now - new Date(b.addedAt).getTime() < 30 * 86_400_000).length;

  return {
    updated: SITE.lastUpdated,
    totals: { bots: stats.bots, builders: stats.builders, categories: stats.categories, installs: installsTotal, last7, last30 },
    perCategory: [...perCategory.entries()]
      .map(([slug, count]) => ({ slug, count }))
      .sort((a, b) => b.count - a.count),
    integrations,
    topInstalled: topInstalled.map((b) => ({ slug: b.slug, name: b.name, installs: b.installs as number })),
    weeks,
  };
}
