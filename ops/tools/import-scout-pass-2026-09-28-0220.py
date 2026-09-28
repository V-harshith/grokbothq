#!/usr/bin/env python3
"""Append this pass's verified bots to content/bots.json + refresh ops bookkeeping.

Usage: python3 ops/tools/import-scout-pass-2026-09-28-0220.py
"""
import collections
import json

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"
STAMP = "2026-09-28-0220"
FOUND_AT = "2026-09-28T02:20:00+05:30"

new = json.load(open(SCRATCH + "new_entries.json"))
bots = json.load(open(REPO + "/content/bots.json"))
if isinstance(bots, dict):
    bots = bots["bots"]

have_slug = {b.get("slug") for b in bots}
have_url = {b.get("url") for b in bots}
added, skipped = [], []
for e in new:
    if e["slug"] in have_slug or e["url"] in have_url:
        skipped.append(e["slug"])
        continue
    added.append(e)

bots.extend(added)
json.dump(bots, open(REPO + "/content/bots.json", "w"), ensure_ascii=False, indent=2)

slugs = [b.get("slug") for b in bots]
urls = [b.get("url") for b in bots]
builders = {(b.get("builder") or {}).get("x") for b in bots}
print("added", len(added), "| skipped", len(skipped))
print("total", len(bots), "| published", sum(1 for b in bots if b.get("status") == "published"))
print("unique slugs", len(set(slugs)) == len(slugs), "| unique urls", len(set(urls)) == len(urls))
print("builders", len({x for x in builders if x}))
print("empty slugs:", sum(1 for s in slugs if not s))
print("non-ascii slugs:", [s for s in slugs if s and not s.isascii()][:5])
print("categories:", dict(collections.Counter(b.get("category") for b in bots)))
json.dump(added, open(SCRATCH + "added_this_pass.json", "w"), ensure_ascii=False, indent=1)

# ---- candidates queue: cap 50, newest first ----
cand = json.load(open(REPO + "/ops/scout-candidates.json"))
seen_ids = {(c.get("bot_id") or c.get("url", "").rsplit("/", 1)[-1]) for c in cand}
fresh = []
for e in added:
    bid = e["url"].rsplit("/", 1)[-1]
    if bid in seen_ids:
        continue
    fresh.append({
        "name": e["name"],
        "bot_id": bid,
        "url": e["url"],
        "builder_x_handle": (e.get("builder") or {}).get("x") or "",
        "one_line_desc": e["tagline"],
        "source_post_url": e.get("source") or "",
        "found_at": FOUND_AT,
    })
cand = fresh + cand
cand = cand[:50]
json.dump(cand, open(REPO + "/ops/scout-candidates.json", "w"), ensure_ascii=False, indent=1)
print("candidates queue:", len(cand), "(+%d this pass)" % len(fresh))
