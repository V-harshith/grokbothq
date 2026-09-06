/**
 * Keyword Harvester - zero-budget keyword research.
 *
 * Mines Google + DuckDuckGo autocomplete (the same suggestions real searchers
 * see) using the alphabet-soup technique: seed queries expanded with letters
 * and intent prefixes, harvested from both engines, deduped and scored.
 *
 * Usage:  node ops/tools/keyword-harvester.mjs [--locale=en-IN] [--out=ops/data]
 * Output: ops/data/keywords-<date>.json + ops/data/keywords-top.md
 */
import { writeFileSync, mkdirSync } from "node:fs";

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v] = a.replace(/^--/, "").split("=");
    return [k, v === undefined ? true : v];
  })
);
const LOCALE = args.locale || "en-IN";
const OUT_DIR = args.out || "ops/data";

const SEEDS = [
  "grok bot",
  "grok bots",
  "best grok bots",
  "grok bot for",
  "grok bot that",
  "how to create a grok bot",
  "how to make a grok bot",
  "grok bot vs",
  "grok bot directory",
  "grok bot integrations",
  "grok bot news",
  "grok bot tutorial",
  "grok bot examples",
  "grok bot free",
];

const SUFFIXES = [
  ..."abcdefghijklmnopqrstuvwxyz".split(""),
  "best", "free", "how to", "vs", "for business", "for students", "for email",
  "for coding", "reddit", "review", "list", "new", "top 10", "without",
];

const queries = [];
for (const seed of SEEDS) {
  queries.push(seed);
  for (const sfx of SUFFIXES) queries.push(`${seed} ${sfx}`.trim());
}
const unique = [...new Set(queries)].slice(0, 168);

const all = new Map();
let done = 0;

async function googleSuggest(q) {
  const url = `https://suggestqueries.google.com/complete/search?client=firefox&hl=${LOCALE}&gl=in&q=${encodeURIComponent(q)}`;
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (keyword research)" } });
  if (!res.ok) return [];
  const data = await res.json();
  return (data && data[1] ? data[1] : []).filter((s) => typeof s === "string");
}

async function ddgSuggest(q) {
  const url = `https://duckduckgo.com/ac/?q=${encodeURIComponent(q)}&type=list`;
  const res = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 (keyword research)" } });
  if (!res.ok) return [];
  const data = await res.json();
  return (data && data[1] ? data[1] : []).filter((s) => typeof s === "string");
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (const q of unique) {
  try {
    const [g, d] = await Promise.all([googleSuggest(q), ddgSuggest(q)]);
    for (const kw of [...g, ...d]) {
      const key = kw.toLowerCase().trim();
      if (!key.includes("grok")) continue;
      const cur = all.get(key);
      if (cur) cur.hits += 1;
      else all.set(key, { keyword: kw.trim(), engine: g.length >= d.length ? "google" : "ddg", seed: q, hits: 1 });
    }
  } catch {
    /* engine hiccup - skip this query */
  }
  done++;
  if (done % 25 === 0) console.log(`${done}/${unique.length} queries, ${all.size} unique keywords`);
  await sleep(120);
}

const keywords = [...all.values()].sort((a, b) => b.hits - a.hits || a.keyword.localeCompare(b.keyword));

mkdirSync(OUT_DIR, { recursive: true });
const date = new Date().toISOString().slice(0, 10);
writeFileSync(`${OUT_DIR}/keywords-${date}.json`, JSON.stringify({ locale: LOCALE, queriesRun: unique.length, harvested: keywords.length, keywords }, null, 2) + "\n");

const top = keywords
  .slice(0, 60)
  .map((k, i) => `${String(i + 1).padStart(2, "0")}. ${k.keyword}  (hits: ${k.hits}, from: "${k.seed}")`)
  .join("\n");
writeFileSync(`${OUT_DIR}/keywords-top.md`, `# Autocomplete harvest ${date} (${LOCALE})\n\n${unique.length} queries -> ${keywords.length} unique keywords\n\n${top}\n`);

console.log(`DONE: ${unique.length} queries -> ${keywords.length} unique keywords -> ${OUT_DIR}/keywords-${date}.json`);
