import { SITE } from "@/data/site";
import { bots } from "@/data/bots";
import { categories } from "@/data/categories";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { comparePages } from "@/data/compare";
import { allIntegrations } from "@/lib/integrations";

export const dynamic = "force-dynamic";

/**
 * /sitemap.xml as an explicit route handler.
 *
 * This replaced app/sitemap.ts (Next's MetadataRoute generator) because Search
 * Console reported "Sitemap could not be read" for it while reading
 * /news-sitemap.xml without complaint. The two differed only in how they were
 * produced: the generator served `Content-Type: application/xml` plus
 * `Content-Disposition: inline; filename="sitemap.xml"`, whereas this site's
 * hand-written news sitemap serves `application/xml; charset=utf-8` with no
 * Content-Disposition - and that one is reported as Success.
 *
 * The URL set is deliberately unchanged, so switching generators cannot drop or
 * add a page. What changes is only the response headers.
 */

type Entry = {
  url: string;
  lastmod: string;
  changefreq: "daily" | "weekly" | "monthly" | "yearly";
  priority: number;
};

const esc = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

export function GET() {
  const base = SITE.url.replace(/\/$/, "");
  // date-only strings (YYYY-MM-DD) - the format Google's sitemap docs use and
  // unambiguously valid for Search Console, unlike full ISO timestamps
  const now = SITE.lastUpdated;

  const staticRoutes: Entry[] = [
    { url: `${base}/`, lastmod: now, changefreq: "daily", priority: 1 },
    { url: `${base}/bots`, lastmod: now, changefreq: "daily", priority: 0.9 },
    { url: `${base}/new`, lastmod: now, changefreq: "daily", priority: 0.8 },
    { url: `${base}/use-cases`, lastmod: now, changefreq: "weekly", priority: 0.8 },
    { url: `${base}/agent`, lastmod: now, changefreq: "monthly", priority: 0.7 },
    { url: `${base}/integrations`, lastmod: now, changefreq: "weekly", priority: 0.7 },
    { url: `${base}/stats`, lastmod: now, changefreq: "daily", priority: 0.7 },
    { url: `${base}/news`, lastmod: now, changefreq: "daily", priority: 0.7 },
    { url: `${base}/privacy`, lastmod: now, changefreq: "yearly", priority: 0.3 },
    { url: `${base}/terms`, lastmod: now, changefreq: "yearly", priority: 0.3 },
    { url: `${base}/groups`, lastmod: now, changefreq: "weekly", priority: 0.8 },
    { url: `${base}/guides`, lastmod: now, changefreq: "weekly", priority: 0.8 },
    { url: `${base}/compare`, lastmod: now, changefreq: "weekly", priority: 0.8 },
    { url: `${base}/faq`, lastmod: now, changefreq: "monthly", priority: 0.7 },
    { url: `${base}/submit`, lastmod: now, changefreq: "monthly", priority: 0.6 },
    { url: `${base}/featured`, lastmod: now, changefreq: "monthly", priority: 0.5 },
    { url: `${base}/about`, lastmod: now, changefreq: "monthly", priority: 0.5 },
  ];

  const botRoutes: Entry[] = bots.map((bot) => ({
    url: `${base}/bots/${bot.slug}`,
    lastmod: bot.addedAt,
    changefreq: "weekly",
    priority: 0.7,
  }));

  const categoryRoutes: Entry[] = categories.map((c) => ({
    url: `${base}/bots/category/${c.slug}`,
    lastmod: now,
    changefreq: "weekly",
    priority: 0.8,
  }));

  const comboRoutes: Entry[] = combos.map((c) => ({
    url: `${base}/groups/${c.slug}`,
    lastmod: c.addedAt,
    changefreq: "weekly",
    priority: 0.6,
  }));

  const guideRoutes: Entry[] = guides.map((g) => ({
    url: `${base}/guides/${g.slug}`,
    lastmod: g.updatedAt,
    changefreq: "monthly",
    priority: 0.7,
  }));

  const integrationRoutes: Entry[] = allIntegrations().map((i) => ({
    url: `${base}/integrations/${i.slug}`,
    lastmod: now,
    changefreq: "weekly",
    priority: 0.6,
  }));

  const compareRoutes: Entry[] = comparePages.map((c) => ({
    url: `${base}/compare/${c.slug}`,
    lastmod: c.updatedAt,
    changefreq: "monthly",
    priority: 0.7,
  }));

  const entries = [
    ...staticRoutes,
    ...botRoutes,
    ...categoryRoutes,
    ...comboRoutes,
    ...guideRoutes,
    ...compareRoutes,
    ...integrationRoutes,
  ];

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...entries.flatMap((e) => [
      "<url>",
      `<loc>${esc(e.url)}</loc>`,
      `<lastmod>${e.lastmod}</lastmod>`,
      `<changefreq>${e.changefreq}</changefreq>`,
      `<priority>${e.priority}</priority>`,
      "</url>",
    ]),
    "</urlset>",
  ].join("\n");

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
