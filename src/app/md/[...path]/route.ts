import { bots, botMap } from "@/data/bots";
import { guides, guideMap } from "@/data/guides";
import { categories, categoryMap } from "@/data/categories";
import { SITE, DISCLAIMER } from "@/data/site";
import type { Bot, Guide } from "@/data/types";

// markdown variants refresh on the same cadence as the pages they mirror
export const revalidate = 300;

const base = SITE.url.replace(/\/$/, "");

const MD_HEADERS = { "Content-Type": "text/markdown; charset=utf-8" };

function footer(canonicalPath: string): string {
  const canonical = `${base}${canonicalPath}`;
  return [
    "",
    "---",
    "",
    `Part of [${SITE.name}](${base}), the independent, hand-reviewed directory of Grok bots. Canonical page: [${canonical}](${canonical}).`,
    DISCLAIMER,
    "",
  ].join("\n");
}

function botMd(bot: Bot): string {
  const lines: string[] = [];
  const handle = bot.builder.x.replace("@", "");
  const builder = handle ? `Built by ${bot.builder.name} ([@${handle}](https://x.com/${handle}))` : `Built by ${bot.builder.name}`;
  const cat = categoryMap.get(bot.category);

  lines.push(`# ${bot.name}`);
  lines.push("");
  lines.push(`> ${bot.tagline}`);
  lines.push("");
  const meta = [
    `[Open the bot](${bot.url})`,
    builder,
    cat ? `[${cat.name} bots](${base}/bots/category/${cat.slug})` : null,
  ]
    .filter(Boolean)
    .join(" - ");
  lines.push(meta);
  lines.push("");
  lines.push(bot.description);
  lines.push("");

  lines.push("## Key facts");
  lines.push("");
  lines.push(`- Added: ${bot.addedAt}`);
  if (bot.installs != null) lines.push(`- Installs: ${bot.installs} (reported by the bot's public source listing)`);
  if (bot.integrations?.length) lines.push(`- Integrations: ${bot.integrations.join(", ")}`);
  if (bot.bestFor?.length) lines.push(`- Best for: ${bot.bestFor.join(", ")}`);
  if (bot.source) lines.push(`- Source: ${bot.source}`);
  lines.push("");

  if (bot.features?.length) {
    lines.push("## Features");
    lines.push("");
    for (const f of bot.features) lines.push(`- ${f}`);
    lines.push("");
  }

  lines.push("## Open this bot");
  lines.push("");
  lines.push(`[${bot.url}](${bot.url})`);
  lines.push("");

  lines.push(footer(`/bots/${bot.slug}`));
  return lines.join("\n");
}

function guideMd(guide: Guide): string {
  const lines: string[] = [];

  lines.push(`# ${guide.title}`);
  lines.push("");
  lines.push(`> ${guide.quickAnswer}`);
  lines.push("");
  lines.push(`Updated ${guide.updatedAt} - ${guide.readingMinutes} min read - tagged: ${guide.tags.join(", ")}`);
  lines.push("");
  lines.push(guide.intro);
  lines.push("");

  for (const s of guide.sections) {
    lines.push(`## ${s.heading}`);
    lines.push("");
    if (s.body) for (const p of s.body) lines.push(p);
    if (s.list?.length) {
      lines.push("");
      for (const item of s.list) lines.push(`- ${item}`);
    }
    if (s.steps?.length) {
      lines.push("");
      s.steps.forEach((st, i) => lines.push(`${i + 1}. **${st.name}** - ${st.text}`));
    }
    lines.push("");
  }

  lines.push(footer(`/guides/${guide.slug}`));
  return lines.join("\n");
}

function guidesIndexMd(): string {
  const lines: string[] = [];

  lines.push("# Grok Bot Guides");
  lines.push("");
  lines.push(
    "How to create, write instructions for, chain, and monetize Grok bots. Every guide also has a plain-text (markdown) version: append .md to its URL."
  );
  lines.push("");
  for (const g of guides) {
    lines.push(`- [${g.title}](${base}/guides/${g.slug}): ${g.quickAnswer}`);
  }
  lines.push("");

  lines.push(footer("/guides"));
  return lines.join("\n");
}

function useCasesMd(): string {
  const lines: string[] = [];
  const sourced = bots.filter((b) => b.source);

  lines.push("# How people are using Grok bots");
  lines.push("");
  lines.push(
    "Real-world Grok bot use cases, sourced from the X posts that introduced each bot. Every example is a real, listed bot with a link you can check."
  );
  lines.push("");

  for (const cat of categories) {
    const items = sourced.filter((b) => b.category === cat.slug);
    if (items.length === 0) continue;
    lines.push(`## ${cat.name}`);
    lines.push("");
    for (const b of items) {
      lines.push(`### ${b.name}`);
      lines.push("");
      lines.push(b.tagline);
      lines.push("");
      lines.push(`- [View the X post](${b.source})`);
      lines.push(`- [Open the bot](${b.url})`);
      lines.push("");
    }
  }

  lines.push(footer("/use-cases"));
  return lines.join("\n");
}

function render(path: string[]): string | null {
  const [a, b] = path;
  if (a === "bots" && b) {
    const bot = botMap.get(b);
    return bot ? botMd(bot) : null;
  }
  if (a === "guides" && b) {
    const guide = guideMap.get(b);
    return guide ? guideMd(guide) : null;
  }
  if (a === "guides" && !b) return guidesIndexMd();
  if (a === "use-cases" && !b) return useCasesMd();
  return null;
}

export async function GET(_req: Request, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  const md = render(path);
  if (md == null) return new Response("Not found", { status: 404 });
  return new Response(md, { headers: MD_HEADERS });
}
