import { news } from "@/lib/news";
import { SITE } from "@/data/site";

export const dynamic = "force-static";

/**
 * Google News sitemap: only articles from the last 2 days (Google's rule).
 * Hermes adds news daily, so this stays populated automatically; on quiet
 * days it serves a valid but empty channel.
 */
export function GET() {
  const base = SITE.url.replace(/\/$/, "");
  const cutoff = new Date(Date.now() - 2 * 86_400_000).toISOString().slice(0, 10);

  const recent = [...news]
    .filter((n) => n.date >= cutoff)
    .sort((a, b) => b.date.localeCompare(a.date));

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">',
    ...recent.map((n) =>
      [
        "<url>",
        `<loc>${base}/news</loc>`,
        "<news:news>",
        "<news:publication>",
        `<news:name>${SITE.name}</news:name>`,
        "<news:language>en</news:language>",
        "</news:publication>",
        `<news:publication_date>${n.date}</news:publication_date>`,
        `<news:title>${n.title.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</news:title>`,
        "</news:news>",
        `</url>`,
      ].join("")
    ),
    "</urlset>",
  ].join("");

  return new Response(xml, {
    headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" },
  });
}
