#!/usr/bin/env python3
"""Extract bot records (id, name, creatorName, handle, description, addHref) from
x.ai/bot/marketplace* HTML payloads, then diff against content/bots.json urls.

Usage: python3 ops/tools/extract-marketplace.py <html> [<html> ...]
"""
import glob
import json
import re
import sys

REPO = "/root/grokbothq"
INNER = re.compile(
    r'"name":"(?P<name>(?:[^"\\]|\\.)*)","creatorName":"(?P<creator>(?:[^"\\]|\\.)*)"'
    r',"handle":"(?P<handle>(?:[^"\\]|\\.)*)","description":"(?P<desc>(?:[^"\\]|\\.)*)"'
    r'.*?"addHref":"/bot/(?P<bid>[A-Za-z0-9_\-]+)"',
    re.S,
)


def unescape_payload(html: str) -> str:
    """Marketplace payload is JSON nested inside the RSC stream (escaped twice)."""
    return (
        html.replace('\\\\"', '"')
        .replace('\\"', '"')
        .replace("\\\\n", " ")
        .replace("\\n", " ")
        .replace("\\/", "/")
    )


def records(path: str):
    html = open(path, encoding="utf-8", errors="replace").read()
    payload = unescape_payload(html)
    out = {}
    for m in INNER.finditer(payload):
        bid = m.group("bid")
        rec = {
            "bot_id": bid,
            "url": f"https://x.ai/bot/{bid}",
            "name": m.group("name").strip(),
            "creator": m.group("creator").strip(),
            "handle": m.group("handle").strip(),
            "desc": m.group("desc").strip(),
            "src": path,
        }
        out[bid] = rec  # later pages overwrite; refs are equal across pages
    return out


def main():
    files = []
    for a in sys.argv[1:]:
        files.extend(glob.glob(a))
    recs = {}
    for f in files:
        r = records(f)
        print(f"{f}: {len(r)} records", file=sys.stderr)
        recs.update(r)
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_urls = {b.get("url", "") for b in bots}
    have_names = {(b.get("name") or "").strip().lower() for b in bots}
    try:
        aliases = set(json.load(open(f"{REPO}/ops/marketplace-alias-map.json"))["aliases"])
    except Exception:
        aliases = set()
    new = []
    for bid, r in recs.items():
        if r["url"] in have_urls:
            continue
        if bid in aliases:
            continue
        r["dupe_name"] = r["name"].lower() in have_names
        new.append(r)
    print(json.dumps(
        {"total_records": len(recs), "already_listed": len(recs) - len(new), "new": new},
        indent=1,
    ))


if __name__ == "__main__":
    main()
