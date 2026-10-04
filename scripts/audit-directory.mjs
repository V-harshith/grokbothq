// Full-directory audit. Verifies every published listing live and reconciles
// what we store against what the x.ai bot page says.
//
//   node scripts/audit-directory.mjs            # verify only (read-only)
//   node scripts/audit-directory.mjs --fix      # delist 404s, fill missing builder names
//   node scripts/audit-directory.mjs --stamp    # also stamp lastVerifiedAt on every 200
//   node scripts/audit-directory.mjs --limit 50 # sample (fast smoke test)
//
// Checks per listing:
//   1. the x.ai/bot URL still answers 200 (a dead link is the one unforgivable
//      failure in this directory — AGENTS.md hard rule 2)
//   2. `sharerName` in the page payload vs our `builder.name` — filled when we
//      have nothing. Handles are never guessed: a wrong handle is worse than a
//      missing one.
//
// A non-200 is never taken at face value: the 24-worker burst makes x.ai answer
// 500 for a single listing now and then, and delisting a live bot over one bad
// fetch is a silent data loss (it happened: chained-oblivion-loekv1, 2026-09-25).
// Every failure is re-fetched alone, twice, before it counts as dead — so the
// URL has to be unreachable three times in a row to leave the directory.
//
// Written for the daily-ops cron. No dependencies; Node 22 global fetch.

import { readFileSync, writeFileSync } from "node:fs";

const args = process.argv.slice(2);
const FIX = args.includes("--fix");
const limitArg = args.indexOf("--limit");
const LIMIT = limitArg > -1 ? Number(args[limitArg + 1]) : Infinity;
// `lastVerifiedAt` is stamped only on an explicit --stamp run. Default-off is
// deliberate: the date lives on every entry, so stamping rewrites the whole data
// file daily, and that full-file diff collides with the scout branch that appends
// to the same file several times a day. Verify/delist by default; stamp when a
// quiet window is wanted.
const STAMP = args.includes("--stamp");
const today = new Date().toISOString().slice(0, 10);

const BOTS = new URL("../content/bots.json", import.meta.url).pathname;
const all = JSON.parse(readFileSync(BOTS, "utf8"));
const published = all.filter((b) => b.status !== "pending").slice(0, LIMIT);

const UA = "Mozilla/5.0 (compatible; grokbothq-audit/1.0; +https://grokbothq.xyz)";
const RETRIES = 2; // extra lone attempts before a non-200 counts as dead
const RETRY_DELAY_MS = 2500;

// A share record does not always carry a usable creator name. x.ai pages have
// rendered the literal junk `null x2`, and a one-character value is not an
// attribution. A blank builder name beats a wrong one (see AGENTS.md: a wrong
// handle is worse than a missing one), so those never auto-fill.
const junkName = (s) => {
  const t = (s ?? "").trim();
  return t.length < 2 || /\bnull\b|undefined/i.test(t);
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchOnce(bot) {
  const res = await fetch(bot.url, { headers: { "user-agent": UA } });
  if (res.status !== 200) return { bot, code: res.status };
  const html = await res.text();
  const sharer = html.match(/\\"sharerName\\":\\"([^"\\]{1,80})\\"/) ?? html.match(/"sharerName":"([^"]{1,80})"/);
  return { bot, code: 200, sharer: sharer?.[1] ?? null };
}

async function check(bot) {
  let last = null;
  for (let attempt = 0; attempt <= RETRIES; attempt += 1) {
    if (attempt > 0) await sleep(RETRY_DELAY_MS * attempt);
    try {
      last = { ...(await fetchOnce(bot)), attempts: attempt + 1 };
    } catch (error) {
      last = { bot, code: error.name, attempts: attempt + 1 };
    }
    if (last.code === 200) return last;
  }
  return last;
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
const named = results.filter((r) => r.code === 200 && r.sharer && !junkName(r.sharer) && !(r.bot.builder ?? {}).name);
const retried = results.filter((r) => (r.attempts ?? 1) > 1);
const recovered = retried.filter((r) => r.code === 200);

console.log(`audited ${results.length} published listings`);
console.log(`  live 200      : ${results.length - dead.length}`);
console.log(
  `  failing       : ${dead.length}${dead.length ? " -> " + dead.map((d) => `${d.bot.slug} (${d.code} x${d.attempts ?? 1})`).join(", ") : ""}`
);
console.log(`  retried after a non-200 : ${retried.length}${retried.length ? ` -> ${recovered.length} recovered, ${retried.length - recovered.length} confirmed dead` : ""}`);
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
  writeFileSync(BOTS, JSON.stringify(all, null, 1) + "\n");
  console.log(`  --fix applied : ${delisted} delisted, ${filled} builder names filled`);
}

/**
 * Stamp `lastVerifiedAt` on every listing this run reached.
 *
 * A verification date that is not stored anywhere cannot be audited: the site shows "Verified
 * <date>" per listing, and a future reader can tell which listings have gone a long time without a
 * check. Stamping runs by default (a full pass covers the whole directory daily); `--no-stamp` keeps
 * a run read-only. The file is only rewritten when a date actually changes, so re-running the same
 * day is a no-op and the ops commit stays meaningful.
 */
// Only listings that actually answered 200 are stamped: a bot delisted this run
// was checked and found dead, so it must not carry today's "verified" date.
const lookedAt = new Set(results.filter((r) => r.code === 200).map((r) => r.bot.slug));
let stamped = 0;
if (STAMP) {
  for (const bot of all) {
    if (!lookedAt.has(bot.slug)) continue;
    if (bot.lastVerifiedAt !== today) {
      bot.lastVerifiedAt = today;
      stamped += 1;
    }
  }
}
if (stamped > 0) {
  writeFileSync(BOTS, JSON.stringify(all, null, 1) + "\n");
  console.log(`  verified dates: ${stamped} updated to ${today}`);
} else if (STAMP) {
  console.log(`  verified dates: all ${lookedAt.size} checked listings already dated ${today}`);
}

process.exit(dead.length > 0 ? 2 : 0);
