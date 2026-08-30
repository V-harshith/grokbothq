/**
 * CI script: parses a GitHub issue created from the bot-submission template,
 * validates it, and appends the bot to content/bots.json.
 *
 * Inputs (env): ISSUE_BODY, ISSUE_NUMBER, ISSUE_TITLE
 * Outputs (GITHUB_OUTPUT): valid, reason, slug, name
 *
 * Exit code 1 = rejected (workflow closes the issue with the reason).
 */
import { readFileSync, writeFileSync, appendFileSync } from "node:fs";

const BODY = process.env.ISSUE_BODY ?? "";
const ISSUE_NUMBER = process.env.ISSUE_NUMBER ?? "?";
const FILE = "content/bots.json";

const CATEGORIES = new Set([
  "assistants", "engineering", "research", "money",
  "sales", "creative", "life", "productivity",
]);

// Naive but effective spam screen — anything pitching services/products gets rejected.
const SPAM = [
  /\b(crypto|bitcoin|nft|airdrop|token presale)\b/i,
  /\b(casino|betting|porn|nsfw|onlyfans)\b/i,
  /\b(seo services|backlinks|guest post|link building)\b/i,
  /\b(followers|subscribers|likes) (for|cheap|fast)\b/i,
  /\b(telegram|whatsapp)\s*[:+]/i,
  /https?:\/\/(?!x\.ai\/bot)/i, // no external links anywhere in the submission
];

function fail(reason) {
  console.error(`REJECTED: ${reason}`);
  const fs = process.env.GITHUB_OUTPUT;
  if (fs) appendFileSync(fs, `valid=false\nreason=${reason.replace(/\n/g, " ")}\n`);
  process.exit(1);
}

function succeed({ slug, name }) {
  const fs = process.env.GITHUB_OUTPUT;
  if (fs) {
    appendFileSync(fs, `valid=true\nslug=${slug}\nname=${name.replace(/\n/g, " ")}\n`);
  }
  console.log(`ACCEPTED: ${name} → ${slug}`);
}

/** GitHub YAML issue forms produce "### Label\n\n<value>" blocks. */
function parseField(label) {
  const re = new RegExp(`### ${label}\\s*\\n+([\\s\\S]*?)(?=\\n### |$)`, "i");
  const m = BODY.match(re);
  return m ? m[1].trim() : "";
}

function lines(text) {
  return text.split("\n").map((l) => l.replace(/^[-*]\s*/, "").trim()).filter(Boolean).slice(0, 8);
}

function slugify(name) {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "bot";
}

// ---------- parse ----------
const name = parseField("Bot name");
const url = parseField("x\\.ai/bot link") || parseField("x.ai/bot link");
const category = parseField("Category").toLowerCase().trim();
const pitch = parseField("One-sentence pitch");
const xHandle = parseField("Your X handle").replace(/^@/, "").trim();
const instructions = parseField("Core instructions(?: \\(optional\\))?");
const features = lines(parseField("Features(?: \\(optional\\))?"));
const bestFor = lines(parseField("Best for(?: \\(optional\\))?"));

// ---------- validate ----------
if (!name || name.length < 2 || name.length > 60) fail("Bot name must be 2-60 characters.");
if (!/^https:\/\/x\.ai\/bot\/\S+$/i.test(url)) fail("The bot link must look like https://x.ai/bot/<your-bot>.");
if (!CATEGORIES.has(category)) fail(`Category must be one of: ${[...CATEGORIES].join(", ")}.`);
if (pitch.length < 10 || pitch.length > 280) fail("The one-sentence pitch must be 10-280 characters.");
if (xHandle && !/^[A-Za-z0-9_]{1,15}$/.test(xHandle)) fail("X handle looks invalid (letters, numbers, underscores, max 15).");
if (instructions && instructions.length > 1200) fail("Core instructions are too long (max 1200 characters).");
for (const l of [...features, ...bestFor]) if (l.length > 100) fail("Feature/best-for lines must be under 100 characters.");

const allText = [name, pitch, instructions, ...features, ...bestFor].join("\n");
for (const rx of SPAM) if (rx.test(allText)) fail("Submission tripped the spam filter. Only x.ai/bot links and plain descriptions, please.");

// ---------- dedupe + build entry ----------
const data = JSON.parse(readFileSync(FILE, "utf8"));
if (data.some((b) => (b.url || "").toLowerCase() === url.toLowerCase())) {
  fail("This bot is already listed (or already pending review).");
}

let slug = slugify(name);
let n = 2;
while (data.some((b) => b.slug === slug)) slug = `${slugify(name)}-${n++}`;

const today = new Date().toISOString().slice(0, 10);
data.push({
  slug,
  name,
  builder: { name: xHandle || "Unknown builder", x: xHandle || "unknown" },
  tagline: pitch,
  description: pitch + " Open it directly from the listing with one click.",
  category,
  instructions: instructions || `You are ${name}. ${pitch} Follow the user's input faithfully and never request credentials or private data.`,
  features: features.length ? features : ["Single-purpose workflow — paste your input, get structured output"],
  bestFor: bestFor.length ? bestFor : ["Anyone who does this task more than once a week"],
  url,
  addedAt: today,
  status: "published",
});

writeFileSync(FILE, JSON.stringify(data, null, 2) + "\n", "utf8");
succeed({ slug, name });
