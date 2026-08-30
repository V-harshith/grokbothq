/**
 * Merges grokbots.page listings into content/bots.json (deduped by x.ai/bot
 * link). Source page embeds each bot as:
 *
 * <li class="listing" style="--bot-hue:95">
 *   <span class="listing-kicker">Creative</span>
 *   <a class="listing-open" href="https://x.ai/bot/<ID>">
 *   <span class="listing-name">...</span>
 *   <span class="listing-desc">...</span>
 *   <a class="listing-owner" href="/owners/handle">...@handle</a>
 *
 * Usage: node scripts/import-gpage.mjs <saved.html>
 */
import { readFileSync, writeFileSync } from "node:fs";

const [, , htmlPath] = process.argv;
if (!htmlPath) {
  console.error("usage: node scripts/import-gpage.mjs <saved.html>");
  process.exit(1);
}

const html = readFileSync(htmlPath, "utf8");

function pick(block, re) {
  const m = block.match(re);
  return m ? decode(m[1]) : "";
}

function decode(s) {
  return s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&nbsp;/g, " ")
    .trim();
}

const CATEGORY_MAP = {
  assistants: "assistants",
  engineering: "engineering",
  research: "research",
  money: "money",
  sales: "sales",
  creative: "creative",
  life: "life",
  productivity: "productivity",
};

function categorize(kicker, name, desc) {
  const k = kicker.toLowerCase().trim();
  if (CATEGORY_MAP[k]) return CATEGORY_MAP[k];
  const text = `${name} ${desc}`.toLowerCase();
  if (/\b(code|dev|build|repo|github|deploy|script|automat)/.test(text)) return "engineering";
  if (/\b(email|inbox|calendar|meeting|notes|task|slack|notion|workflow)/.test(text)) return "productivity";
  if (/\b(research|paper|news|monitor|watch|track|market)/.test(text)) return "research";
  if (/\b(money|price|deal|budget|refund|invest)/.test(text)) return "money";
  if (/\b(sales|lead|seo|marketing|content|post|newsletter|growth|brand)/.test(text)) return "sales";
  if (/\b(meme|image|design|write|video|clip|podcast|hook)/.test(text)) return "creative";
  if (/\b(meal|recipe|fitness|travel|habit|health|surf)/.test(text)) return "life";
  return "assistants";
}

const items = [];
const liRe = /<li class="listing"[^>]*>([\s\S]*?)<\/li>/g;
let m;
while ((m = liRe.exec(html))) {
  const block = m[1];
  const link = pick(block, /class="listing-open" href="([^"]+)"/);
  if (!link.startsWith("https://x.ai/bot/")) continue;
  items.push({
    link,
    categoryKicker: pick(block, /listing-kicker"[\s\S]*?<\/span>([\s\S]*?)<\/span>/) || pick(block, /listing-dot" aria-hidden="true"><\/span>([\s\S]*?)<\/span>/),
    name: pick(block, /class="listing-name">([^<]*)</),
    desc: pick(block, /class="listing-desc">([\s\S]*?)<\/span>/),
    handle: (pick(block, /class="listing-owner"[\s\S]*?@([A-Za-z0-9_]{1,15})/)),
    hue: (block.match(/--bot-hue:(\d+)/) ?? [])[1] ?? "",
  });
}

const existing = JSON.parse(readFileSync("content/bots.json", "utf8"));
const seenUrls = new Set(existing.map((b) => (b.url || "").toLowerCase()));
const seenSlugs = new Set(existing.map((b) => b.slug));

function slugify(name) {
  const base =
    name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "")
      .slice(0, 60) || "bot";
  let slug = base;
  let n = 2;
  while (seenSlugs.has(slug)) slug = `${base}-${n++}`;
  seenSlugs.add(slug);
  return slug;
}

const today = new Date().toISOString().slice(0, 10);
let added = 0;

for (const item of items) {
  if (seenUrls.has(item.link.toLowerCase())) continue;
  seenUrls.add(item.link.toLowerCase());
  if (!item.name) continue;

  existing.push({
    slug: slugify(item.name),
    name: item.name,
    builder: { name: item.handle, x: item.handle },
    tagline: item.desc.slice(0, 140),
    description: item.desc.endsWith(".") ? item.desc : item.desc + ".",
    category: categorize(item.categoryKicker, item.name, item.desc),
    ...(typeof item.hue === "string" && item.hue !== "" ? { hue: Number(item.hue) % 360 } : {}),
    url: item.link,
    addedAt: today,
    status: "published",
  });
  added++;
}

writeFileSync("content/bots.json", JSON.stringify(existing, null, 2) + "\n", "utf8");
console.log(`source items: ${items.length}, new bots added: ${added}, total: ${existing.length}`);
