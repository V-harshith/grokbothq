// Route sweep: hit every sitemap URL, report anything that is not a 200.
import http from "node:http";
import https from "node:https";

const BASE = process.argv[2] ?? "http://localhost:3133";
const mod = BASE.startsWith("https") ? https : http;
const origin = new URL(BASE).origin;

function get(url) {
  return new Promise((resolve) => {
    mod
      .get(url, (r) => {
        r.resume();
        resolve(r.statusCode);
      })
      .on("error", () => resolve(0));
  });
}

function getText(path) {
  return new Promise((resolve) => {
    mod
      .get(BASE + path, (r) => {
        let d = "";
        r.on("data", (c) => (d += c));
        r.on("end", () => resolve(d));
      })
      .on("error", () => resolve(""));
  });
}

const xml = await getText("/sitemap.xml");
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) =>
  m[1].replace("https://grokbothq.xyz", origin)
);

const bad = [];
for (const u of urls) {
  const c = await get(u);
  if (c !== 200) bad.push(`${c} ${u}`);
}

console.log(`checked ${urls.length} pages`);
console.log(bad.length ? `BROKEN (${bad.length}):\n` + bad.join("\n") : "all 200 OK");
