import { bots } from "@/data/bots";
import { news } from "@/lib/news";
import { SITE } from "@/data/site";

export const dynamic = "force-static";

function esc(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/** RSS 2.0 feed: curated news + the freshest listings, newest first. */
export function GET() {
  const base = SITE.url.replace(/\/$/, "");
  const now = new Date().toUTCString();

  const newsItems = [...news]
    .sort((a, b) => b.date.localeCompare(a.date))
    .slice(0, 15)
    .map((n) => ({
      title: n.title,
      link: n.url,
      guid: n.url,
      date: n.date,
      description: `${n.summary} (via ${n.source})`,
    }));

  const botItems = [...bots]
    .sort((a, b) => b.addedAt.localeCompare(a.addedAt))
    .slice(0, 30)
    .map((b) => ({
      title: `New Grok bot: ${b.name}`,
      link: `${base}/bots/${b.slug}`,
      guid: `${base}/bots/${b.slug}`,
      date: b.addedAt,
      description: b.tagline,
    }));

  const items = [...newsItems, ...botItems].sort((a, b) => b.date.localeCompare(a.date));

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss version="2.0">',
    "<channel>",
    `<title>${esc(SITE.name)}</title>`,
    `<link>${base}</link>`,
    `<description>${esc(SITE.description)}</description>`,
    "<language>en</language>",
    `<lastBuildDate>${now}</lastBuildDate>`,
    ...items.flatMap((i) => [
      "<item>",
      `<title>${esc(i.title)}</title>`,
      `<link>${esc(i.link)}</link>`,
      `<guid>${esc(i.guid)}</guid>`,
      `<pubDate>${new Date(i.date).toUTCString()}</pubDate>`,
      `<description>${esc(i.description)}</description>`,
      "</item>",
    ]),
    "</channel>",
    "</rss>",
  ].join("\n");

  return new Response(xml, {
    headers: { "Content-Type": "application/rss+xml; charset=utf-8", "Cache-Control": "public, max-age=3600" },
  });
}
