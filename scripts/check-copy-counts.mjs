// Guard against stale magnitudes in copy. Any "<number> bots / bot pages /
// listings / builders / categories / guides / combos" written as a literal in
// src/**, content/*.json, README.md or docs must match the directory itself.
// Run by CI on every PR: `node scripts/check-copy-counts.mjs`
//
// Why this exists: the /featured page shipped "all 700+ bot pages" and the
// README shipped "230+ Grok bots" while the directory held 1,529 — a public
// open-source repo advertising the wrong size of its own product. Prefer
// deriving the number (bots.length) over writing it down; this check is the
// backstop for the places where a literal is unavoidable.

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative, extname } from "node:path";

const root = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const read = (p) => JSON.parse(readFileSync(join(root, p), "utf8"));

const all = read("content/bots.json");
const published = all.filter((b) => b.status !== "pending");
const entities = {
  bots: published.length,
  "bot pages": published.length,
  listings: published.length,
  builders: new Set(published.map((b) => b.builder?.x).filter(Boolean)).size,
  categories: new Set(published.map((b) => b.category)).size,
  guides: read("content/guides.json").length,
  combos: read("content/combos.json").length,
};

const PATTERN = /(\d[\d,]*)\+?\s*(bots|bot pages|listings|builders|categories|guides|combos)\b/gi;
const SKIP_DIRS = new Set(["node_modules", ".git", ".next", "ops", "public"]);
const SKIP_FILES = new Set(["scripts/check-copy-counts.mjs"]);

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

const targets = [
  ...walk(join(root, "src")),
  ...readdirSync(join(root, "content")).filter((f) => extname(f) === ".json").map((f) => join(root, "content", f)),
  join(root, "README.md"),
];

const problems = [];
for (const file of targets) {
  const rel = relative(root, file);
  if (SKIP_FILES.has(rel)) continue;
  if (![".ts", ".tsx", ".json", ".md"].includes(extname(file))) continue;
  const text = readFileSync(file, "utf8");
  for (const match of text.matchAll(PATTERN)) {
    const value = Number(match[1].replace(/,/g, ""));
    const unit = match[2].toLowerCase();
    const actual = entities[unit];
    if (actual === undefined) continue;
    // Allow a lower bound (e.g. "1,500+ bots" when there are 1,529) but never a
    // number that overstates or badly understates the directory.
    if (value > actual || value < actual * 0.9) {
      const line = text.slice(0, match.index).split("\n").length;
      problems.push(`${rel}:${line} — copy says "${match[0].trim()}", directory has ${actual} ${unit}`);
    }
  }
}

if (problems.length) {
  console.error("Stale counts in copy — derive the number from content/*.json instead:\n" + problems.join("\n"));
  process.exit(1);
}
console.log(
  `counts in copy OK — ${entities.bots} bots · ${entities.builders} builders · ${entities.categories} categories · ${entities.guides} guides · ${entities.combos} combos`,
);
