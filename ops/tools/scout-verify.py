#!/usr/bin/env python3
"""Scout verify: extract x.ai/bot/<id> links from files/urls, dedupe vs content/bots.json,
then verify each live share page.

A REAL bot share page (checked 2026-09-21):
  HTTP 200
  body contains: "This AI bot was created by a third-party user, not by SpaceXAI"
  <title> and og:title = "<Name> by <Builder>"
  og:description = the bot's one-line description

DEAD / expired share link:
  HTTP 404 + ~76KB Next.js error page that still carries the site <title>
  body contains: "The share link may have expired or been deleted."
This is exactly the fake-success trap: status code and body size alone are NOT enough.

Usage:
  python3 ops/tools/scout-verify.py --url URL [--url URL ...]
  python3 ops/tools/scout-verify.py FILE [FILE ...]
  python3 ops/tools/scout-verify.py --ids-file FILE   # one bot id per line
Output: JSON {found, new, verified[], rejected[]} to stdout.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, "content", "bots.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ID_RE = re.compile(r"x\.ai/bot/([A-Za-z0-9_-]{15,})")
NON_BOT = {"marketplace", "guides", "docs", "news", "pricing", "download", "api"}
GOOD = "by a third-party user, not by SpaceXAI"
EXPIRED = "share link may have expired"


def known_urls():
    return {b["url"].rstrip("/") for b in json.load(open(BOTS))}


def curl(url):
    cmd = ["curl", "-sL", "--max-time", "25", "-A", UA,
           "-w", "\n@@STATUS@@%{http_code}", url]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=40).stdout.decode("utf-8", "replace")
    except Exception:
        return 0, ""
    m = re.search(r"@@STATUS@@(\d+)$", out)
    status = int(m.group(1)) if m else 0
    return status, out[:m.start()] if m else out


def meta(body, prop):
    m = re.search(r'<meta property="%s" content="([^"]*)"' % prop, body)
    return m.group(1).strip() if m else ""


def verify(url):
    status, body = curl(url)
    if status != 200:
        return False, None, f"HTTP {status}"
    if GOOD not in body:
        return False, None, ("share link expired/deleted" if EXPIRED in body
                             else "no share-page marker in body")
    title = meta(body, "og:title") or ""
    desc = meta(body, "og:description") or ""
    if not title:
        return False, None, "no og:title"
    name = re.split(r"\s+by\s+", title)[0].strip()
    builder = ""
    mm = re.search(r"\s+by\s+(.+)$", title)
    if mm:
        builder = mm.group(1).strip()
    return True, {"url": url, "name": name, "builder_raw": builder,
                  "title": title, "desc": desc[:400]}, ""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    ids, blob = [], ""
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--url":
            _, blob = curl(args[i + 1])
            i += 2
        elif a == "--ids-file":
            ids += [l.strip() for l in open(args[i + 1]) if l.strip()]
            i += 2
        else:
            blob += open(a, encoding="utf-8", errors="replace").read()
            i += 1
    found = {m for m in ID_RE.findall(blob) if m not in NON_BOT}
    found |= set(ids)
    known = {u.rsplit("/", 1)[1] for u in known_urls()}
    new = sorted(x for x in found if x not in known)
    verified, rejected = [], []
    for botid in new:
        ok, data, note = verify("https://x.ai/bot/" + botid)
        if ok:
            verified.append(data)
        else:
            rejected.append({"bot_id": botid, "reason": note})
    print(json.dumps({"found": len(found), "new": len(new),
                      "verified": verified, "rejected": rejected}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
