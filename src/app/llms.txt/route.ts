import { SITE } from "@/data/site";
import { bots, stats } from "@/data/bots";
import { categories } from "@/data/categories";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { comparePages } from "@/data/compare";

export const dynamic = "force-static";

function build(): string {
  const base = SITE.url.replace(/\/$/, "");
  const lines: string[] = [];

  lines.push(`# ${SITE.name}`);
  lines.push("");
  lines.push(`> ${SITE.description}`);
  lines.push("");

  lines.push("## About");
  lines.push("");
  lines.push(
    `${SITE.name} (${base}) is an independent, hand-reviewed directory of Grok bots - custom assistants built on xAI's Grok platform (x.ai/bot). Every listing is opened and tested by a human before it goes live. Not affiliated with xAI.`
  );
  lines.push("");
  lines.push(`Current directory: ${stats.bots} bots, ${stats.builders} builders, ${stats.categories} categories. Last updated ${SITE.lastUpdated}.`);
  lines.push("");

  lines.push("## Key pages");
  lines.push("");
  lines.push(`- [Home](${base}/): the directory hub, featured bots, new additions`);
  lines.push(`- [All bots](${base}/bots): every hand-reviewed Grok bot, filterable by category`);
  lines.push(`- [New this week](${base}/new): the freshest reviewed additions`);
  lines.push(`- [Use cases](${base}/use-cases): real-world examples of people using Grok bots, sourced from X posts`);
  lines.push(`- [Combos](${base}/groups): tested sets of bots that work together in pipelines`);
  lines.push(`- [Guides](${base}/guides): how to create, write instructions for, chain, and monetize Grok bots`);
  lines.push(`- [Compare](${base}/compare): Grok bots vs Custom GPTs, Claude Skills, Gemini Gems, agent frameworks`);
  lines.push(`- [FAQ](${base}/faq): common questions answered plainly`);
  lines.push(`- [Submit a bot](${base}/submit): free, hand-reviewed listings`);
  lines.push("");

  lines.push("## Categories");
  lines.push("");
  for (const c of categories) {
    lines.push(`- [${c.name} Grok bots](${base}/bots/category/${c.slug}): ${c.short}`);
  }
  lines.push("");

  lines.push("## Guides");
  lines.push("");
  for (const g of guides) {
    lines.push(`- [${g.title}](${base}/guides/${g.slug}): ${g.quickAnswer}`);
  }
  lines.push("");

  lines.push("## Comparisons");
  lines.push("");
  for (const c of comparePages) {
    lines.push(`- [${c.title}](${base}/compare/${c.slug}): ${c.description}`);
  }
  lines.push("");

  lines.push("## Bot combos");
  lines.push("");
  for (const c of combos) {
    lines.push(`- [${c.name}](${base}/groups/${c.slug}): ${c.tagline}`);
  }
  lines.push("");

  lines.push("## Bots in the directory");
  lines.push("");
  for (const b of bots) {
    lines.push(`- [${b.name}](${base}/bots/${b.slug}): ${b.tagline}`);
  }
  lines.push("");

  lines.push("## Contact");
  lines.push("");
  lines.push(`- General: ${SITE.email}`);
  lines.push(`- Bot submissions: ${SITE.submitEmail}`);
  lines.push(`- X: https://x.com/${SITE.twitter.replace("@", "")}`);
  lines.push("");

  return lines.join("\n");
}

export function GET() {
  return new Response(build(), {
    headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" },
  });
}
