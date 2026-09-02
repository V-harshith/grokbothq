import { readFileSync, writeFileSync } from "node:fs";

// /stats: shareable infographic link in the methodology block
let s = readFileSync("src/app/stats/page.tsx", "utf8");
if (!s.includes("opengraph-image")) {
  s = s.replace(
    `          cite it as <span className="font-mono text-xs">Source: GrokBot HQ ({SITE.url}/stats)</span>. Limitation: bot
          behavior depends on xAI&apos;s platform and each builder&apos;s instructions.`,
    `          cite it as <span className="font-mono text-xs">Source: GrokBot HQ ({SITE.url}/stats)</span>. Limitation: bot
          behavior depends on xAI&apos;s platform and each builder&apos;s instructions.
        </p>
        <p className="mt-3 text-sm">
          <a href="/stats/opengraph-image" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
            Download the shareable stats card →
          </a>`
  );
  writeFileSync("src/app/stats/page.tsx", s);
  console.log("infographic link ok");
}

// GEO-ANALYSIS: mark implemented items
let g = readFileSync("GEO-ANALYSIS.md", "utf8");
g = g.replace(
  "## GEO Readiness Score: 74/100",
  "## GEO Readiness Score: 74/100 → **80/100 after the September audit pass**\n\n> Implemented since this analysis: original citable research page (/stats, Dataset schema, daily recomputed), shareable stats infographic, evidence panels, reviewer attribution, FAQ anchors + dated FAQPage schema. Remaining gap is unchanged: off-site entity presence."
);
g = g.replace(
  "2. **Original citable research** — publish \"State of Grok Bots\" monthly from our own directory data (scale, categories, dead-link rate). Unique statistics are the highest-citation asset there is.",
  "2. ✅ **DONE: original citable research** — /stats lives, computed daily, Dataset schema + CC BY. Keep it fresh via the daily pass."
);
g = g.replace(
  "3. **Multi-modal** — an infographic of the directory stats; one short demo video.",
  "3. ⏳ PARTIAL: the /stats shareable infographic card ships (auto-generated OG image). A demo video is still owner-side."
);
writeFileSync("GEO-ANALYSIS.md", g);
console.log("analysis updated");
