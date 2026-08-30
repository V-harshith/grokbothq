// Route sweep: hit every sitemap URL, report anything that is not a 200.
import http from "node:http";

const BASE = process.argv[2] ?? "http://localhost:3133";

function get(url) {
  return new Promise((resolve) => {
    http
      .get(url, (r) => {
        r.resume();
        resolve(r.statusCode);
      })
      .on("error", () => resolve(0));
  });
}

function getText(path) {
  return new Promise((resolve) => {
    http
      .get(BASE + path, (r) => {
        let d = "";
        r.on("data", (c) => (d += c));
        r.on("end", () => resolve(d));
      })
      .on("error", () => resolve(""));
  });
}

const xml = await getText("/sitemap.xml");
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace("https://grokbothq.xyz", BASE));

const bad = [];
for (const u of urls) {
  const c = await get(u);
  if (c !== 200) bad.push(`${c} ${u}`);
}

console.log(`checked ${urls.length} pages`);
console.log(bad.length ? `BROKEN (${bad.length}):\n` + bad.join("\n") : "all 200 OK");
