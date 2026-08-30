import type { MetadataRoute } from "next";
import { SITE } from "@/data/site";
import { bots } from "@/data/bots";
import { categories } from "@/data/categories";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { comparePages } from "@/data/compare";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = SITE.url.replace(/\/$/, "");
  const now = new Date(SITE.lastUpdated);

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${base}/`, lastModified: now, changeFrequency: "daily", priority: 1 },
    { url: `${base}/bots`, lastModified: now, changeFrequency: "daily", priority: 0.9 },
    { url: `${base}/new`, lastModified: now, changeFrequency: "daily", priority: 0.8 },
    { url: `${base}/use-cases`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${base}/groups`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${base}/guides`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${base}/compare`, lastModified: now, changeFrequency: "weekly", priority: 0.8 },
    { url: `${base}/faq`, lastModified: now, changeFrequency: "monthly", priority: 0.7 },
    { url: `${base}/submit`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    { url: `${base}/featured`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
    { url: `${base}/about`, lastModified: now, changeFrequency: "monthly", priority: 0.5 },
  ];

  const botRoutes: MetadataRoute.Sitemap = bots.map((bot) => ({
    url: `${base}/bots/${bot.slug}`,
    lastModified: new Date(bot.addedAt),
    changeFrequency: "weekly",
    priority: 0.7,
  }));

  const categoryRoutes: MetadataRoute.Sitemap = categories.map((c) => ({
    url: `${base}/bots/category/${c.slug}`,
    lastModified: now,
    changeFrequency: "weekly",
    priority: 0.8,
  }));

  const comboRoutes: MetadataRoute.Sitemap = combos.map((c) => ({
    url: `${base}/groups/${c.slug}`,
    lastModified: new Date(c.addedAt),
    changeFrequency: "weekly",
    priority: 0.6,
  }));

  const guideRoutes: MetadataRoute.Sitemap = guides.map((g) => ({
    url: `${base}/guides/${g.slug}`,
    lastModified: new Date(g.updatedAt),
    changeFrequency: "monthly",
    priority: 0.7,
  }));

  const compareRoutes: MetadataRoute.Sitemap = comparePages.map((c) => ({
    url: `${base}/compare/${c.slug}`,
    lastModified: new Date(c.updatedAt),
    changeFrequency: "monthly",
    priority: 0.7,
  }));

  return [...staticRoutes, ...botRoutes, ...categoryRoutes, ...comboRoutes, ...guideRoutes, ...compareRoutes];
}
