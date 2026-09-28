#!/usr/bin/env python3
"""Append this pass's verified bots to content/bots.json + refresh ops bookkeeping."""
import json, sys, collections

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"
STAMP = "2026-09-27-2010"

new = json.load(open(SCRATCH + "new_entries.json"))
bots = json.load(open(REPO + "/content/bots.json"))
if isinstance(bots, dict):
    bots = bots["bots"]

have_slug = {b.get("slug") for b in bots}
have_url = {b.get("url") for b in bots}
added, skipped = [], []
for e in new:
    if e["slug"] in have_slug or e["url"] in have_url:
        skipped.append(e["slug"]); continue
    added.append(e)

bots.extend(added)
json.dump(bots, open(REPO + "/content/bots.json", "w"), ensure_ascii=False, indent=2)

slugs = [b.get("slug") for b in bots]
urls = [b.get("url") for b in bots]
builders = {(b.get("builder") or {}).get("x") for b in bots}
print("added", len(added), "| skipped", len(skipped))
print("total", len(bots), "| published", sum(1 for b in bots if b.get("status") == "published"))
print("unique slugs", len(set(slugs)) == len(slugs), "| unique urls", len(set(urls)) == len(urls))
print("builders", len({x for x in builders if x}) or 0)
print("empty slugs:", sum(1 for s in slugs if not s))
print("non-ascii slugs:", [s for s in slugs if s and not s.isascii()][:5])
cats = collections.Counter(b.get("category") for b in bots)
print("categories:", len(cats), dict(cats))
json.dump(added, open(SCRATCH + "added_this_pass.json", "w"), ensure_ascii=False, indent=1)
