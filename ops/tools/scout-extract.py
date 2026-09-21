#!/usr/bin/env python3
"""Scout helper: extract x.ai/bot links from an HTML/markdown blob, dedupe against
content/bots.json, verify each live (200 + bot name present in body), write results.

Usage:
  python3 ops/tools/scout-extract.py file1 file2 ...      # extract + dedupe + verify
  python3 ops/tools/scout-extract.py --url URL            # fetch then process
Outputs JSON to stdout: {found, new, verified:[...], rejected:[...]}
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, "content", "bots.json")
LINK_RE = re.compile(r"x\.ai/bot/([A-Za-z0-9_-]{8,})")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def known_urls():
    bots = json.load(open(BOTS))
    return {b["url"].rstrip("/") for b in bots}


def extract(text):
    return {"https://x.ai/bot/" + m for m in LINK_RE.findall(text)}


def fetch(url, headers=None):
    cmd = ["curl", "-sL", "--max-time", "25", "-A", UA, url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=40)
        return p.stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def verify(url):
    """Return (ok, name, note)."""
    body = fetch(url)
    if not body:
        return False, None, "empty body"
    # title format: "<name> by @handle" or "<name>"
    m = re.search(r"<title>([^<]*)</title>", body)
    title = (m.group(1).strip() if m else "")
    if len(body) < 2000:
        return False, None, f"body too small ({len(body)}b)"
    low = body.lower()
    if any(x in low for x in ("just a moment", "access denied", "attention required")):
        return False, None, "interstitial"
    # name: strip " by @x" suffix, "<name> · Grok Bot" etc.
    name = re.split(r"\s+(?:by|·|\|)\s+", title)[0].strip() if title else ""
    if not name:
        return False, None, "no title"
    # the page must mention the share/bot framing
    if "grok bot" not in low and "spacexai" not in low:
        return False, None, "no grok bot framing in body"
    return True, name, title


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    blob = ""
    if args[0] == "--url":
        blob = fetch(args[1])
    else:
        for f in args:
            try:
                blob += open(f, encoding="utf-8", errors="replace").read()
            except Exception as e:
                print(f"skip {f}: {e}", file=sys.stderr)
    found = extract(blob)
    known = known_urls()
    new = sorted(u for u in found if u.rstrip("/") not in known)
    verified, rejected = [], []
    for u in new:
        ok, name, note = verify(u)
        if ok:
            verified.append({"url": u, "name": name, "title": note})
        else:
            rejected.append({"url": u, "reason": note})
    print(json.dumps({"found": len(found), "new": len(new),
                      "verified": verified, "rejected": rejected}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
