// Full-directory audit. Verifies every published listing live and reconciles
// what we store against what the x.ai bot page says.
//
//   node scripts/audit-directory.mjs            # report only
//   node scripts/audit-directory.mjs --fix      # delist 404s, fill missing builder names
//   node scripts/audit-directory.mjs --limit 50 # sample (fast smoke test)
//
// Checks per listing:
//   1. the x.ai/bot URL still answers 200 (a dead link is the one unforgivable
//      failure in this directory — AGENTS.md hard rule 2)
//   2. `sharerName` in the page payload vs our `builder.name` — filled when we
//      have nothing. Handles are never guessed: a wrong handle is worse than a
//      missing one.
//
// Written for the daily-ops cron. No dependencies; Node 22 global fetch.

import { readFileSync, writeFileSync } from "node:fs";

const args = process.argv.slice(2);
const FIX = args.includes("--fix");
const limitArg = args.indexOf("--limit");
const LIMIT = limitArg > -1 ? Number(args[limitArg + 1]) : Infinity;

const BOTS = new URL("../content/bots.json", import.meta.url).pathname;
const all = JSON.parse(readFileSync(BOTS, "utf8"));
const published = all.filter((b) => b.status !== "pending").slice(0, LIMIT);

const UA = "Mozilla/5.0 (compatible; grokbothq-audit/1.0; +https://grokbothq.xyz)";

async function check(bot) {
  try {
    const res = await fetch(bot.url, { headers: { "user-agent": UA } });
    if (res.status !== 200) return { bot, code: res.status };
    const html = await res.text();
    const sharer = html.match(/\\"sharerName\\":\\"([^"\\]{1,80})\\"/) ?? html.match(/"sharerName":"([^"]{1,80})"/);
    return { bot, code: 200, sharer: sharer?.[1] ?? null };
  } catch (error) {
    return { bot, code: error.name };
  }
}

const results = [];
const queue = [...published];
const workers = Array.from({ length: 24 }, async () => {
  while (queue.length) {
    const bot = queue.shift();
    results.push(await check(bot));
  }
});
await Promise.all(workers);

const dead = results.filter((r) => r.code !== 200);
const named = results.filter((r) => r.code === 200 && r.sharer && !(r.bot.builder ?? {}).name);

console.log(`audited ${results.length} published listings`);
console.log(`  live 200      : ${results.length - dead.length}`);
console.log(`  failing       : ${dead.length}${dead.length ? " -> " + dead.map((d) => `${d.bot.slug} (${d.code})`).join(", ") : ""}`);
console.log(`  builder name recoverable from x.ai sharerName : ${named.length}`);

if (FIX && (dead.length || named.length)) {
  const deadSlugs = new Set(dead.map((d) => d.bot.slug));
  const byName = new Map(named.map((r) => [r.bot.slug, r.sharer]));
  let delisted = 0;
  let filled = 0;
  for (const bot of all) {
    if (deadSlugs.has(bot.slug)) {
      bot.status = "pending";
      delisted += 1;
      continue;
    }
    const sharer = byName.get(bot.slug);
    if (sharer) {
      bot.builder = { ...(bot.builder ?? {}), name: sharer };
      filled += 1;
    }
  }
  writeFileSync(BOTS, JSON.stringify(all, null, 2));
  console.log(`  --fix applied : ${delisted} delisted, ${filled} builder names filled`);
  process.exit(delisted > 0 ? 2 : 0);
}

process.exit(dead.length > 0 ? 2 : 0);
