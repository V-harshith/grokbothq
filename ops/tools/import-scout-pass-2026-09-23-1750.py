#!/usr/bin/env python3
"""Scout pass 2026-09-23 17:50 IST (cron 359022f62495): append the verified set
from the four upstream catalogs + grokmarket.io, refresh the candidate queue
(cap 50), and log what was looked at but not added.

Deterministic and idempotent: re-running will not double-add (dedupe on url+slug).
"""
import json
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")

SRC_CATALOG = "https://github.com/kydlikebtc/awesome-grokbot"

# bot_id -> (slug, category, source)
PLAN = {
    # --- four upstream catalogs (majiayu000/awesome-grok-bot,
    # cs68614-hash/awesome-grokbot-templates, ZeroPointRepo/GrokBotDev,
    # elie222/botdirectory.ai, aggregated by kydlikebtc/awesome-grokbot)
    "0ajHw7Ghh8oWELkrhCwxL": ("connect-multiple-grok-bot-accounts", "productivity", SRC_CATALOG),
    "B1EPNTh_TsReIL-Y5Q278": ("tera", "life", SRC_CATALOG),
    "KYM0C9BcyfXEP9uIyxlmE": ("drop-radar", "research", SRC_CATALOG),
    "UrO63RhN1LGXD3DzoMess": ("chief-cameron", "productivity", SRC_CATALOG),
    "_SuGdfXVQ06yo3woYqQVO": ("tamago", "productivity", SRC_CATALOG),
    "afzAN696RpFOIs-9uRTHo": ("norm", "productivity", SRC_CATALOG),
    "f0W4gAqrCJ0gRHJTlHOao": ("spark", "productivity", SRC_CATALOG),
    "nSNeVcwO0QZOrOdirgRAc": ("liftoff", "life", SRC_CATALOG),
    "pEUC21J4T7tQ3ORZx8w05": ("dmarc-specialist", "engineering", SRC_CATALOG),
    "z1Qf4iiLWTa8g66rXGIBC": ("roster", "productivity", SRC_CATALOG),
    # --- grokmarket.io directory (carries the creator's original post as source)
    "YkkCbN8-Ubf0FM1BE4i4S": ("research-harness", "research",
                             "https://x.com/SacredFolio/status/2100039366743568892"),
    "grZdTeKVtXFVtIYEe6g_H": ("spcx-watch", "money",
                              "https://x.com/Quidnam/status/2099887054645563412"),
    "igyfOAUWRXvTZbDj2J__S": ("buildertrend-invoice-desk", "money",
                              "https://x.com/Lhp2061004Lhp/status/2100040562497769940"),
}
VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}

# reviewed live, deliberately not listed
NOT_ADDED = [
    {"bot_id": "v-anNtCSU16DhOT6XDOpn", "name": "Carson",
     "url": "https://x.ai/bot/v-anNtCSU16DhOT6XDOpn",
     "reason": "200 but no share record (draft or team-only template) — nothing to list"},
    {"bot_id": "Xk7mQ2pR9vT4nB6cL1sD8", "name": "(unnamed)",
     "url": "https://x.ai/bot/Xk7mQ2pR9vT4nB6cL1sD8",
     "reason": "http 404 — link shared in a catalog but the template is gone"},
    {"bot_id": "-sOdLVj33yh8hh7OlHogi", "name": "Chief of Staff (daniel xu)",
     "url": "https://x.ai/bot/-sOdLVj33yh8hh7OlHogi",
     "reason": "http 404 — the four student bots shared in a post are no longer public"},
    {"bot_id": "1HFC3QdqPtcj1FIbKf8oq", "name": "the pm (daniel xu)",
     "url": "https://x.ai/bot/1HFC3QdqPtcj1FIbKf8oq",
     "reason": "http 404 — same post, template no longer public"},
]


def tagline(desc: str, limit: int = 140) -> str:
    desc = desc.strip()
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    cut = cut[:cut.rfind(" ")].rstrip(" ,;:—–-")
    return cut + "…"


def main():
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_urls = {b["url"] for b in bots}
    have_slugs = {b["slug"] for b in bots}
    rows = {}
    for path in ("/tmp/scout/verified.json", "/tmp/scout/verified2.json"):
        for line in open(path):
            r = json.loads(line)
            if r.get("ok"):
                rows[r["bot_id"]] = r
    # Norm's RSC payload ships a truncated description field; the live page's own
    # meta/body text carries the real one, so use what the page actually renders.
    norm = ("Normalize names and skills across your Grok Bots. One job: help you "
            "normalize display names and skills across the Grok Bots you already have — "
            "without inventing new bots or importing someone else's roster.")
    dir_recs = json.load(open("/tmp/scout/dir_records.json"))

    added = []
    for bid, (slug, cat, src) in PLAN.items():
        r = rows[bid]
        url = f"https://x.ai/bot/{bid}"
        assert url not in have_urls, f"{url} already listed"
        assert slug not in have_slugs, f"slug collision {slug}"
        assert cat in VALID_CATS, cat
        assert r["name"].strip(), bid
        desc = norm if bid == "afzAN696RpFOIs-9uRTHo" else r["desc"].strip()
        name = r["name"].strip()
        if bid in dir_recs and dir_recs[bid].get("summary") and len(dir_recs[bid]["summary"]) > len(desc):
            desc = dir_recs[bid]["summary"].strip()
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": r["sharer"].strip(), "x": ""},
            "tagline": tagline(desc),
            "description": desc,
            "category": cat,
            "url": url,
            "addedAt": TODAY,
            "status": "published",
            "source": src,
        }
        assert len(entry["tagline"]) <= 140, entry["tagline"]
        bots.append(entry)
        have_urls.add(url)
        have_slugs.add(slug)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w"), indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a").write("\n")

    cands = json.load(open(f"{REPO}/ops/scout-candidates.json"))
    cand_urls = {c["url"] for c in cands}
    fresh = []
    for e in added:
        if e["url"] in cand_urls:
            continue
        src = e["source"]
        fresh.append({
            "name": e["name"],
            "bot_id": e["url"].rsplit("/", 1)[-1],
            "url": e["url"],
            "builder_x_handle": "",
            "one_line_desc": e["tagline"],
            "source_post_url": src if "x.com" in src else "",
            "found_at": STAMP,
            "status": "added to directory in ops/scout-pending",
        })
    merged = fresh + cands
    json.dump(merged[:50], open(f"{REPO}/ops/scout-candidates.json", "w"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/ops/scout-candidates.json", "a").write("\n")

    exc_path = f"{REPO}/ops/scout-exclusions-2026-09-23.json"
    exc = json.load(open(exc_path))
    exc.setdefault("not_added", {})["pass_1750_checked_not_added"] = NOT_ADDED
    json.dump(exc, open(exc_path, "w"), indent=2, ensure_ascii=False)
    open(exc_path, "a").write("\n")

    print(f"added {len(added)} bots; total now {len(bots)}; "
          f"candidates {len(merged)} -> kept {min(len(merged), 50)}")
    for e in added:
        print(f"  + {e['slug']:38s} {e['name']} ({e['category']})")


if __name__ == "__main__":
    main()
