import { SITE, DISCLAIMER } from "@/data/site";
import { bots } from "@/data/bots";
import { categories } from "@/data/categories";
import { combos, comboBots } from "@/data/combos";
import { guides } from "@/data/guides";
import { comparePages } from "@/data/compare";
import { faqs } from "@/data/faqs";

export const dynamic = "force-static";

function build(): string {
  const base = SITE.url.replace(/\/$/, "");
  const lines: string[] = [];

  lines.push(`# ${SITE.name} - full content feed`);
  lines.push("");
  lines.push(`> ${SITE.description}`);
  lines.push("");
  lines.push(DISCLAIMER);
  lines.push("");

  lines.push("## FAQ");
  lines.push("");
  for (const f of faqs) {
    lines.push(`### ${f.q}`);
    lines.push("");
    lines.push(f.a);
    lines.push("");
  }

  lines.push("## Guides (full text)");
  lines.push("");
  for (const g of guides) {
    lines.push(`### ${g.title}`);
    lines.push(`URL: ${base}/guides/${g.slug}`);
    lines.push("");
    lines.push(`Quick answer: ${g.quickAnswer}`);
    lines.push("");
    lines.push(g.intro);
    lines.push("");
    for (const s of g.sections) {
      lines.push(`#### ${s.heading}`);
      lines.push("");
      for (const p of s.body ?? []) lines.push(p);
      if (s.list) for (const item of s.list) lines.push(`- ${item}`);
      if (s.steps) {
        s.steps.forEach((step, i) => lines.push(`${i + 1}. **${step.name}** - ${step.text}`));
      }
      lines.push("");
    }
  }

  lines.push("## Comparisons (full text)");
  lines.push("");
  for (const c of comparePages) {
    lines.push(`### ${c.title}`);
    lines.push(`URL: ${base}/compare/${c.slug}`);
    lines.push("");
    lines.push(`Verdict: ${c.verdict.summary}`);
    lines.push("");
    lines.push("Choose Grok bots if:");
    for (const item of c.verdict.chooseGrokBots) lines.push(`- ${item}`);
    lines.push(`Choose ${c.other} if:`);
    for (const item of c.verdict.chooseOther) lines.push(`- ${item}`);
    lines.push("");
    lines.push("Comparison table:");
    lines.push("");
    lines.push("| Aspect | Grok Bots | " + c.other + " |");
    lines.push("|---|---|---|");
    for (const r of c.rows) lines.push(`| ${r.aspect} | ${r.grok} | ${r.other} |`);
    lines.push("");
  }

  lines.push("## Bot combos (workflows)");
  lines.push("");
  for (const c of combos) {
    lines.push(`### ${c.name}`);
    lines.push(`URL: ${base}/groups/${c.slug}`);
    lines.push("");
    lines.push(c.description);
    lines.push("");
    c.steps.forEach((s, i) => lines.push(`${i + 1}. **${s.name}**: ${s.text}`));
    lines.push(`Bots: ${comboBots(c).map((b) => b.name).join(", ")}`);
    lines.push("");
  }

  lines.push("## Categories");
  lines.push("");
  for (const c of categories) {
    lines.push(`### ${c.name}`);
    lines.push(`URL: ${base}/bots/category/${c.slug}`);
    lines.push("");
    lines.push(c.intro);
    lines.push("");
  }

  lines.push("## Bot directory");
  lines.push("");
  for (const b of bots) {
    lines.push(`### ${b.name} (by @${b.builder.x})`);
    lines.push(`URL: ${base}/bots/${b.slug} · Open: ${b.url}`);
    lines.push(`Category: ${b.category}`);
    lines.push("");
    lines.push(b.tagline);
    lines.push("");
    lines.push(b.description);
    lines.push("");
    if (b.features?.length) lines.push(`Features: ${b.features.join("; ")}`);
    if (b.bestFor?.length) lines.push(`Best for: ${b.bestFor.join("; ")}`);
    if (b.source) lines.push(`Source post: ${b.source}`);
    lines.push(`Open button URL: ${b.url}`);
    lines.push("");
  }

  return lines.join("\n");
}

export function GET() {
  return new Response(build(), {
    headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" },
  });
}
