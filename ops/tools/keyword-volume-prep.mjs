/**
 * Volume prep + proxy tiering for harvested keywords.
 *
 * 1. ops/data/keyword-planner-upload.csv - ready to upload to Google Keyword
 *    Planner ("Get search volume and forecasts") for REAL monthly volumes.
 * 2. ops/data/keywords-tiered.json - proxy demand tiers from harvest signals
 *    (NOT real volume): multi-seed hits, both-engine coverage, head length.
 *
 * Usage: node ops/tools/keyword-volume-prep.mjs [input.json]
 */
import { readFileSync, writeFileSync } from "node:fs";

const input = process.argv[2] || "ops/data/keywords-2026-09-06.json";
const data = JSON.parse(readFileSync(input, "utf8"));

// --- proxy tiering (honest: this is NOT search volume) ---
function tier(kw) {
  const words = kw.keyword.split(/\s+/).length;
  const engines = new Set();
  if (kw.engine) engines.add(kw.engine);
  let score = kw.hits * 2;
  if (words <= 3) score += 4;
  else if (words <= 4) score += 2;
  if (kw.hits >= 3) engines.add("multi-seed");
  score += engines.size === 2 ? 2 : 0;
  if (score >= 10) return "HEAD";
  if (score >= 6) return "BODY";
  return "LONG-TAIL";
}

const tiered = data.keywords.map((k) => ({ ...k, tier: tier(k) }));
const counts = tiered.reduce((a, k) => ((a[k.tier] = (a[k.tier] || 0) + 1), a), {});

writeFileSync(
  "ops/data/keywords-tiered.json",
  JSON.stringify(
    {
      note: "tier is a PROXY from autocomplete signals (hits, coverage, length) - not search volume. Upload the CSV to Google Keyword Planner for real volumes.",
      updated: new Date().toISOString().slice(0, 10),
      counts,
      keywords: tiered,
    },
    null,
    2
  ) + "\n"
);

// --- Google Keyword Planner upload CSV ---
const csv = ["Keyword", ...tiered.map((k) => k.keyword)].join("\n");
writeFileSync("ops/data/keyword-planner-upload.csv", csv + "\n");

console.log(`keywords: ${tiered.length}`);
console.log(`tiers: HEAD=${counts.HEAD || 0} BODY=${counts.BODY || 0} LONG-TAIL=${counts["LONG-TAIL"] || 0}`);
console.log("wrote: ops/data/keyword-planner-upload.csv (upload to Google Keyword Planner)");
console.log("wrote: ops/data/keywords-tiered.json");
