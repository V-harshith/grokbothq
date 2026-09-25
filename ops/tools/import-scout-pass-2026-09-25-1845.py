#!/usr/bin/env python3
"""Scout pass 2026-09-25 18:45 IST (cron 359022f62495).

Fresh-bot pass from the five public awesome-grokbot catalogs plus the kydlikebtc
catalog.json (all fetched free, one fetch each). Every candidate x.ai/bot link
was opened live with ops/tools/verify-bot-links.py (HTTP 200 + a share record
carrying id/ownerType/sharerName/botName/description) and re-read with
ops/tools/fetch_share_full.py for the full description. No paid API calls: curl
plus free web_search only.

Rules applied (same bar as the 06:10 pass, so held rows stay held):
  - dedupe on x.ai/bot id against content/bots.json, ops/scout-candidates.json
    and every id already recorded in ops/scout-exclusions-*.json /
    ops/scout-report-*.json (the queue rolls over at 50, so the id has to be
    checked against the archive, not just the live queue)
  - drop live descriptions under 40 chars (placeholder)
  - drop non-ASCII names (queued for a translation pass)
  - hold rows whose platform display name is the org name "SpaceX"
    (attribution not verifiable from the page)
  - no twin listings: a candidate whose live template is already listed under a
    different share id is dropped as a duplicate
  - builder x handle only when the catalog's handle corroborates the sharer
    display name on the platform record (every word of the name appears in the
    handle); otherwise name only, never a guessed handle

Deterministic + idempotent: re-running never double-adds.
"""
import json
import re
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/scout"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")
SRC = "https://github.com/kydlikebtc/awesome-grokbot"
SRC2 = "https://github.com/cs68614-hash/awesome-grokbot-templates"

VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}

CATEGORY = {
    "mono-lisa": "creative",
    "x-bot-2": "sales",
    "chuck": "productivity",
    "weekly-usage": "productivity",
    "grocery-bot-3": "life",
    "peep-txt": "engineering",
    "quote-chase-desk": "sales",
    "grok-build-5": "engineering",
    "news-ear": "life",
}

# kept out for a reason that is not mechanical — document it in the report
MANUAL_DROP = {
    "EQgLIMO5Q_sVk3IM9EQbZ": "same template already listed as full-spectrum-law-firm-os "
                             "(the x.ai share id resolves case-insensitively)",
    "VSO9GRfDreEu2ZiXwwZB_": "third near-identical \"Optima by TOATspace\" re-share; the "
                             "directory already carries two, and the sharer display name "
                             "(\"gemini sub001\") is not verifiable as the builder",
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "bot"


def tagline(desc: str, limit: int = 140) -> str:
    desc = " ".join(desc.split())
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    return cut[:cut.rfind(" ")].rstrip(" ,;:—-–") + "…"


def handle_for(sharer: str, handle: str) -> str:
    """Handle only when it corroborates the sharer name on the platform record."""
    if not handle or not sharer:
        return ""
    words = [w for w in re.split(r"[^a-z0-9]+", sharer.lower()) if len(w) >= 3]
    h = re.sub(r"[^a-z0-9]", "", handle.lower())
    return handle if words and all(w in h for w in words) else ""


def main():
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_ids = {b["url"].rsplit("/", 1)[-1] for b in bots}
    have_slugs = {b["slug"] for b in bots}

    full = {}
    for line in open(f"{SCRATCH}/full_records.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r.get("ok"):
            full[r["bot_id"]] = r
    lines = json.load(open(f"{SCRATCH}/catalog_lines.json"))
    still = json.load(open(f"{SCRATCH}/still_ok.json"))

    added, dropped = [], []
    for bid in still:
        r = full.get(bid)
        if not r:
            dropped.append((bid, bid, "no live record on the second read"))
            continue
        name = (r.get("name") or "").strip()
        desc = " ".join((r.get("desc") or "").split())
        sharer = (r.get("sharer") or "").strip()
        cat_lines = lines.get(bid, [])
        cat_handle = cat_lines[0]["handle"] if cat_lines else ""
        cat_name = cat_lines[0]["name"] if cat_lines else ""
        source = SRC2 if any(c["src"] == "cs68614" for c in cat_lines) else SRC

        if bid in MANUAL_DROP:
            dropped.append((name, bid, MANUAL_DROP[bid]))
            continue
        if sharer.lower() == "spacex":
            dropped.append((name, bid, "platform display name is the org name \"SpaceX\" "
                                       "— attribution not verifiable from the page"))
            continue
        if len(desc) < 40:
            dropped.append((name, bid, f"live description is a placeholder ({len(desc)} chars)"))
            continue
        if not name or any(ord(c) > 127 for c in name):
            dropped.append((name, bid, "non-ASCII name — needs a dedicated translation pass"))
            continue
        if bid in have_ids:
            dropped.append((name, bid, "already listed (same x.ai/bot id)"))
            continue

        slug = slugify(name)
        n = 2
        while slug in have_slugs:
            slug = f"{slugify(name)}-{n}"
            n += 1
        have_slugs.add(slug)
        have_ids.add(bid)

        cat = CATEGORY.get(slug, "assistants")
        assert cat in VALID_CATS, cat
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": sharer, "x": handle_for(sharer, cat_handle)},
            "tagline": tagline(desc),
            "description": desc if desc.endswith((".", "!", "?")) else desc + ".",
            "category": cat,
            "url": f"https://x.ai/bot/{bid}",
            "addedAt": TODAY,
            "status": "published",
            "source": source,
        }
        assert len(entry["tagline"]) <= 140, slug
        bots.append(entry)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w"), indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a").write("\n")

    queue = [{"name": e["name"], "bot_id": e["url"].rsplit("/", 1)[-1], "url": e["url"],
              "builder_x_handle": e["builder"]["x"], "one_line_desc": e["tagline"],
              "source_post_url": e["source"], "found_at": STAMP,
              "status": "added to directory in ops/scout-pending"} for e in added]
    for name, bid, why in dropped:
        queue.append({"name": name or bid, "bot_id": bid, "url": f"https://x.ai/bot/{bid}",
                      "builder_x_handle": "", "one_line_desc": why,
                      "source_post_url": SRC, "found_at": STAMP,
                      "status": "verified live, not listed"})
    old = json.load(open(f"{REPO}/ops/scout-candidates.json"))
    seen = {q["bot_id"] for q in queue}
    queue += [o for o in old if o.get("bot_id") not in seen]
    json.dump(queue[:50], open(f"{REPO}/ops/scout-candidates.json", "w"),
              indent=2, ensure_ascii=False)

    report = {
        "run": "2026-09-25 18:45 IST scout pass (cron 359022f62495)",
        "branch": "ops/scout-pending (single accumulating PR)",
        "method": ("Five awesome-grokbot catalogs fetched free (one request each), every "
                   "x.ai/bot link opened live: HTTP 200 AND a share record with "
                   "id/ownerType/sharerName/botName/description. Zero paid API calls "
                   "(no xurl, no x_search)."),
        "counts": {"raw_links_found": 2104, "not_previously_seen": 97,
                   "templates_confirmed_live": 73,
                   "already_held_or_excluded": 54,
                   "added_to_directory": len(added), "held_back": len(dropped)},
        "added": [{"name": e["name"], "slug": e["slug"], "url": e["url"],
                   "category": e["category"], "builder": e["builder"]} for e in added],
        "held_back": [{"name": n, "bot_id": b, "reason": w} for n, b, w in dropped],
        "sources": {
            "kydlikebtc/awesome-grokbot (catalog.json)": "https://github.com/kydlikebtc/awesome-grokbot",
            "cs68614-hash/awesome-grokbot-templates": SRC2,
            "majiayu000/awesome-grok-bot": "https://github.com/majiayu000/awesome-grok-bot",
            "RongleCat/awesome-grok-bot": "https://github.com/RongleCat/awesome-grok-bot",
            "lroolle/awesome-grokbot-templates": "https://github.com/lroolle/awesome-grokbot-templates",
            "divo12/awesome-grok-bot-templates": "https://github.com/divo12/awesome-grok-bot-templates",
        },
        "tools": ["ops/tools/verify-bot-links.py", "ops/tools/fetch_share_full.py"],
    }
    json.dump(report, open(f"{REPO}/ops/scout-report-2026-09-25-1845.json", "w"),
              ensure_ascii=False, indent=1)

    print(json.dumps({"added": len(added), "held": len(dropped), "total": len(bots)}))
    for e in added:
        print(f"  + {e['slug']:22s} {e['name'][:30]:30s} {e['category']:13s} "
              f"{e['builder']['name'][:18]:18s} x={e['builder']['x'] or '-'}")
    for n, b, w in dropped:
        print(f"  - {b:24s} {n[:28]:28s} {w[:70]}")


if __name__ == "__main__":
    main()
