/**
 * CI script: auto-expires featured placements past their featuredUntil date.
 * Exits 0 silently when nothing changed; prints "CHANGED" when bots were updated.
 */
import { readFileSync, writeFileSync } from "node:fs";

const FILE = "content/bots.json";
const today = new Date().toISOString().slice(0, 10);

const data = JSON.parse(readFileSync(FILE, "utf8"));
let changed = false;

for (const bot of data) {
  if (bot.featured && bot.featuredUntil && bot.featuredUntil < today) {
    bot.featured = false;
    delete bot.featuredUntil;
    changed = true;
    console.log(`expired featured: ${bot.name} (was until ${bot.featuredUntil})`);
  }
}

if (changed) {
  writeFileSync(FILE, JSON.stringify(data, null, 2) + "\n", "utf8");
  console.log("CHANGED");
} else {
  console.log("NO_CHANGES");
}
