#!/usr/bin/env python3
"""Parse the x.ai/bot/marketplace page (Next.js flight payload) into structured rows.

The payload is JSON-escaped inside <script> tags and shaped like:
  "templates":[{"id":"dr-eggbot-v2","name":"dr eggbot","creatorName":"Lauren Tan",
                "handle":"poteto","description":"...","summary":"...",
                "categories":["From Grok Bot Team"],"installCount":0,
                "addHref":"/bot/_jOdbfkB16zxu7MRcmReE", ...}]
"addHref" carries the official x.ai/bot/<id> used by the marketplace Import button.

Usage: python3 ops/tools/parse-marketplace.py FILE > rows.json
"""
import json
import re
import sys


def field(chunk, key):
    m = re.search(r'"%s":"((?:[^"\\]|\\.)*)"' % key, chunk)
    if not m:
        return None
    try:
        return json.loads('"%s"' % m.group(1))
    except Exception:
        return m.group(1)


def main():
    body = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    text = body.replace('\\"', '"').replace("\\\\", "\\")
    rows = []
    for m in re.finditer(r'"addHref":"(/bot/[A-Za-z0-9_-]+)"', text):
        start = text.rfind('{"id":"', 0, m.start())
        if start == -1:
            continue
        chunk = text[start:m.start() + 200]
        bot_id = m.group(1).rsplit("/", 1)[-1]
        cats = re.search(r'"categories":\[([^\]]*)\]', chunk)
        rows.append({
            "bot_id": bot_id,
            "marketplace_slug": field(chunk, "id"),
            "name": field(chunk, "name"),
            "creator_name": field(chunk, "creatorName"),
            "handle": field(chunk, "handle"),
            "summary": field(chunk, "summary") or field(chunk, "description") or "",
            "categories": [c.strip('"') for c in cats.group(1).split(",")] if cats else [],
            "installCount": field(chunk, "installCount"),
        })
    # de-dup on bot_id, keep first
    seen, out = set(), []
    for r in rows:
        if r["bot_id"] in seen:
            continue
        seen.add(r["bot_id"])
        out.append(r)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
