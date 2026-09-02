/**
 * CI script: pulls per-bot install-click counts from Umami's API and writes
 * content/metrics.json, which the site uses to display live interest numbers.
 * Requires three repo secrets; exits 0 quietly when they are not configured.
 *
 *   UMAMI_URL      e.g. https://umami.example.com   (no trailing slash)
 *   UMAMI_TOKEN    read-only API token from Umami settings
 *   UMAMI_SITE_ID  the website id for this site
 *
 * Umami event shape produced by the Open button: name "install-click",
 * property bot = slug. We query website events for the last 30 days and
 * aggregate counts per bot slug.
 */
import { writeFileSync, readFileSync } from "node:fs";

const base = (process.env.UMAMI_URL ?? "").replace(/\/$/, "");
const token = process.env.UMAMI_TOKEN ?? "";
const siteId = process.env.UMAMI_SITE_ID ?? "";

if (!base || !token || !siteId) {
  console.log("Umami not configured (UMAMI_URL / UMAMI_TOKEN / UMAMI_SITE_ID) - skipping metrics pull.");
  process.exit(0);
}

const start = new Date(Date.now() - 30 * 86_400_000).toISOString().slice(0, 10);
const end = new Date().toISOString().slice(0, 10);

async function api(path) {
  const res = await fetch(`${base}${path}`, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error(`Umami API ${res.status} on ${path}`);
  return res.json();
}

// Umami (v3) endpoint: /api/websites/:id/metrics?startAt&endAt&type=event
// Entry shape: { x: event name, y: count, ... } with property breakdowns.
const events = await api(`/api/websites/${siteId}/metrics?startAt=${Date.parse(start)}&endAt=${Date.parse(end)}&type=event`);
const counts = {};
let sponsorClicks30d = 0;
for (const e of events) {
  if (e.x === "sponsor-click") { sponsorClicks30d += e.y ?? e.count ?? 1; continue; }
  if (e.x !== "install-click") continue;
  // Umami groups by event property; entries carry the bot slug in `p`/`pv` fields
  const slug = e.p ?? e.bot ?? e.property;
  if (typeof slug === "string" && slug) counts[slug] = (counts[slug] ?? 0) + (e.y ?? e.count ?? 1);
}

const prev = (() => {
  try {
    return JSON.parse(readFileSync("content/metrics.json", "utf8"));
  } catch {
    return {};
  }
})();

const sponsorClicks = (prev.sponsorClicks ?? 0) + sponsorClicks30d;
const merged = { updatedAt: new Date().toISOString().slice(0, 10), opens: { ...prev.opens, ...counts }, sponsorClicks };
writeFileSync("content/metrics.json", JSON.stringify(merged, null, 2) + "\n", "utf8");
const total = Object.values(merged.opens).reduce((a, b) => a + b, 0);
console.log(`CHANGED: metrics.json updated, ${Object.keys(counts).length} bots with clicks, ${total} total in last 30d`);
