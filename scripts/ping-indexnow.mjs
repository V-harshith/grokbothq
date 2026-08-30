/**
 * CI script: pings IndexNow with all sitemap URLs so search engines re-crawl
 * fresh content quickly. Requires the INDEXNOW_KEY secret; exits 0 quietly
 * when it's not configured (non-fatal).
 *
 * One-time setup for the human:
 *   1. Generate any 32-char hex key (or any string), put it in repo secret INDEXNOW_KEY
 *   2. Put the same string in a file at https://<domain>/<key>.txt (public)
 */
const key = process.env.INDEXNOW_KEY ?? "";
const site = (process.env.SITE_URL ?? "https://grokbothub.xyz").replace(/\/$/, "");

if (!key) {
  console.log("INDEXNOW_KEY not set — skipping IndexNow ping.");
  process.exit(0);
}

const res = await fetch(`${site}/sitemap.xml`);
if (!res.ok) {
  console.error(`Could not fetch sitemap (${res.status}) — skipping.`);
  process.exit(0);
}
const xml = await res.text();
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
console.log(`Pinging IndexNow with ${urls.length} URLs…`);

const payload = {
  host: site.replace(/^https?:\/\//, ""),
  key,
  keyLocation: `${site}/${key}.txt`,
  urlList: urls,
};

const ping = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body: JSON.stringify(payload),
});
console.log(`IndexNow responded ${ping.status}`);
process.exit(0); // never fail the workflow on ping errors
