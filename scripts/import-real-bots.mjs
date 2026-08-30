/**
 * One-off importer: extracts the real Grok bot dataset embedded in a saved
 * grokbots.best HTML page and converts it into content/bots.json.
 *
 * Usage:
 *   node scripts/import-real-bots.mjs /tmp/grokbots_best.html --analyze   (inspect tags)
 *   node scripts/import-real-bots.mjs /tmp/grokbots_best.html --write     (write content)
 *
 * The source page embeds records like (inside escaped JSON strings):
 *   {"slug":"be-happier","name":"Be Happier","description":"...",
 *    "author":"@lennysan","type":"template","link":"https://x.ai/bot/<ID>",
 *    "source_url":"https://x.com/<user>/status/<id>","tags":[],
 *    "integrations":["gmail"],"published":true,"install_count":5,...}
 */
import { readFileSync, writeFileSync } from "node:fs";

const [, , htmlPath, mode] = process.argv;
if (!htmlPath) {
  console.error("usage: node scripts/import-real-bots.mjs <saved.html> --analyze|--write");
  process.exit(1);
}

const html = readFileSync(htmlPath, "utf8");

// The payload is embedded with escaped quotes (\"slug\":\"...\"). Unescape, then
// brace-match every object that carries a x.ai/bot link and JSON.parse it.
const unescaped = html
  .replace(/\\"/g, '"')
  .replace(/\\\\/g, "\\");

const records = [];
const needle = '{"id":';
let i = unescaped.indexOf(needle);
while (i !== -1) {
  let depth = 0;
  let end = -1;
  for (let j = i; j < unescaped.length; j++) {
    const ch = unescaped[j];
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        end = j + 1;
        break;
      }
    }
  }
  if (end !== -1) {
    try {
      const obj = JSON.parse(unescaped.slice(i, end));
      if (obj.link && String(obj.link).startsWith("https://x.ai/bot/")) records.push(obj);
    } catch {
      /* not a record */
    }
  }
  i = unescaped.indexOf(needle, i + needle.length);
}

// dedupe by bot link, keep published only
const seen = new Set();
const clean = records.filter((r) => {
  if (!r.published || seen.has(r.link)) return false;
  seen.add(r.link);
  return true;
});

const tags = new Map();
const integrations = new Map();
for (const r of clean) {
  for (const t of r.tags ?? []) tags.set(t, (tags.get(t) ?? 0) + 1);
  for (const t of r.integrations ?? []) integrations.set(t, (integrations.get(t) ?? 0) + 1);
}

console.log(`records: ${records.length}, published+unique: ${clean.length}`);
console.log("authors:", new Set(clean.map((r) => r.author)).size);
console.log("tags:", [...tags.entries()].sort((a, b) => b[1] - a[1]).map(([t, n]) => `${t}(${n})`).join(", "));
console.log("integrations:", [...integrations.entries()].sort((a, b) => b[1] - a[1]).map(([t, n]) => `${t}(${n})`).slice(0, 20).join(", "));

const CATEGORY_RULES = [
  [/\b(code|coding|developer|github|repo|pr\b|deploy|debug|refactor|app|stack|agent loop|build)/i, "engineering"],
  [/\b(email|inbox|calendar|schedule|meeting|standup|notes?|productiv|task|todo|slack|notion|crm|workflow|automat)/i, "productivity"],
  [/\b(research|paper|arxiv|analy[sz]e|market|competitor|trend|diligence|fact|news|summar|brief)/i, "research"],
  [/\b(money|invoice|expense|budget|price|refund|invest|stock|crypto|finance|subscription|tax)/i, "money"],
  [/\b(sales|lead|outreach|cold email|prospect|customer|pitch|seo|marketing|content|newsletter|social|post|tweet|growth|brand)/i, "sales"],
  [/\b(meme|image|design|logo|write|story|creative|name|idea|hook|caption|video|clip|podcast|youtube)/i, "creative"],
  [/\b(meal|recipe|fitness|workout|health|sleep|travel|trip|habit|happier|journal|mood|life)/i, "life"],
];

function categorize(r) {
  const text = `${r.name} ${r.description} ${(r.tags ?? []).join(" ")}`;
  for (const [rx, cat] of CATEGORY_RULES) if (rx.test(text)) return cat;
  return "assistants";
}

function toBot(r) {
  const rawAuthor = String(r.author ?? "").trim();
  const handle = /^@[\w]{1,15}$/.test(rawAuthor) ? rawAuthor.slice(1) : "";
  const desc = String(r.description ?? "").trim();
  const sentences = desc.split(/(?<=[.!?])\s+/);
  const tagline = (sentences[0] ?? desc).slice(0, 140);
  const integrationNames = (r.integrations ?? [])
    .map((s) => String(s).replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()))
    .slice(0, 4);
  const features = [];
  if (integrationNames.length) features.push(`Connects with ${integrationNames.join(", ")}`);
  if (r.prompt) features.push("Ships with a ready-to-run prompt template");
  features.push("One-click open in Grok, no setup required");

  return {
    slug: r.slug,
    name: r.name,
    builder: { name: handle, x: handle },
    tagline,
    description: desc + (desc.endsWith(".") ? "" : ".") + " Open it directly from the listing with one click.",
    category: categorize(r),
    instructions: `You are ${r.name}. ${tagline} Follow the user's input faithfully, keep outputs structured, and never request credentials or private data.`,
    features,
    bestFor: (r.tags ?? []).slice(0, 3).length ? (r.tags ?? []).slice(0, 3) : ["Anyone who does this task more than once a week"],
    ...(typeof r.install_count === "number" && r.install_count > 0 ? { installs: r.install_count } : {}),
    url: r.link,
    addedAt: String(r.created_at ?? "").slice(0, 10) || new Date().toISOString().slice(0, 10),
    status: "published",
    ...(r.source_url ? { source: String(r.source_url) } : {}),
  };
}

const bots = clean.map(toBot).sort((a, b) => b.addedAt.localeCompare(a.addedAt) || a.name.localeCompare(b.name));

if (mode === "--write") {
  writeFileSync("content/bots.json", JSON.stringify(bots, null, 2) + "\n", "utf8");
  console.log(`WROTE content/bots.json with ${bots.length} real bots`);
} else {
  console.log("--- sample record ---");
  console.log(JSON.stringify(bots[0], null, 1));
  console.log("--- categories ---");
  const cats = {};
  for (const b of bots) cats[b.category] = (cats[b.category] ?? 0) + 1;
  console.log(JSON.stringify(cats));
}
