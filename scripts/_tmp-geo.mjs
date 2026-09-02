import { readFileSync, writeFileSync } from "node:fs";

// 1) seo.ts: Person schema builder + richer Organization sameAs
let s = readFileSync("src/lib/seo.ts", "utf8");
if (!s.includes("personJsonLd")) {
  s = s.replace(
    "export function botListJsonLd(",
    `/** The operator entity - entity linking for AI engines (sameAs across platforms). */
export function personJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Person",
    name: "Harshith Rao",
    alternateName: "harshithOG",
    url: "https://x.com/harshithOG",
    sameAs: ["https://x.com/harshithOG", "https://github.com/V-harshith"],
    worksFor: { "@type": "Organization", name: SITE.name, url: absUrl("/") },
  };
}

export function botListJsonLd(`
  );
  s = s.replace(
    '    sameAs: [`https://x.com/${SITE.twitter.replace("@", "")}`],',
    '    sameAs: [`https://x.com/${SITE.twitter.replace("@", "")}`, "https://github.com/V-harshith/grokbothq"],'
  );
  writeFileSync("src/lib/seo.ts", s);
  console.log("seo.ts ok");
}

// 2) guides: mount Person schema + set Article author to the Person
let g = readFileSync("src/app/guides/[slug]/page.tsx", "utf8");
if (!g.includes("personJsonLd")) {
  g = g.replace('import { pageMetadata, breadcrumbsJsonLd, articleJsonLd } from "@/lib/seo";', 'import { pageMetadata, breadcrumbsJsonLd, articleJsonLd, personJsonLd } from "@/lib/seo";');
  g = g.replace("          articleJsonLd({", "          personJsonLd(),\n          articleJsonLd({");
  g = g.replace('author: SITE.name,', 'author: "Harshith Rao (@harshithOG)",');
  writeFileSync("src/app/guides/[slug]/page.tsx", g);
  console.log("guides ok");
}

// 3) llms.txt: Key facts section (citability)
let l = readFileSync("src/app/llms.txt/route.ts", "utf8");
if (!l.includes("## Key facts")) {
  l = l.replace("## Key pages", `## Key facts
- GrokBot HQ lists ${stats.bots} hand-reviewed Grok bots from ${stats.builders} builders across ${stats.categories} categories.
- Every listing is opened and tested by a human before publication; dead links are removed.
- Install counts shown on listings are reported by each bot's public source listing.
- The directory is independent and unaffiliated with xAI. Grok is a trademark of xAI.
- Content license: CC BY 4.0 with attribution (link to the site). Code is source-available and restricted.
- Operator: Harshith Rao (@harshithOG on X). Contact: ${SITE.email}
- Machine index: ${base}/api/v1/index.json - the full directory as JSON. RSS: ${base}/rss.xml

## Key pages`);
  writeFileSync("src/app/llms.txt/route.ts", l);
  console.log("llms ok");
}
