#!/usr/bin/env python3
"""Verify Grok bot share links live: HTTP 200 AND the page payload must carry a
real share record (id, ownerType, botName), otherwise the template is a draft or
the link is dead.

Usage: python3 ops/tools/verify-bot-links.py id1 id2 ... > /tmp/verified.json
Prints one JSON object per line on stdout, a summary to stderr.
"""
import json
import re
import subprocess
import sys
import concurrent.futures as cf

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
REC = re.compile(
    r'\\+"id\\+":\\+"(?P<bid>[A-Za-z0-9_\-]+)\\+",\\+"ownerType\\+":\\+"(?P<own>[A-Z]+)\\+",'
    r'\\+"sharerName\\+":\\+"(?P<sharer>(?:[^"\\]|\\\\.)*)\\+",'
    r'\\+"botName\\+":\\+"(?P<name>(?:[^"\\]|\\\\.)*)\\+",'
    r'\\+"description\\+":\\+"(?P<desc>(?:[^"\\]|\\\\.)*)\\+"'
)


def clean(s: str) -> str:
    s = s.replace('\\\\n', ' ').replace('\\n', ' ')
    s = s.replace('\\\\"', '"').replace('\\"', '"')
    s = s.replace("\\\\'", "'").replace("\\'", "'")
    return re.sub(r"\s+", " ", s).strip()


def fetch(bid: str):
    url = f"https://x.ai/bot/{bid}"
    try:
        p = subprocess.run(
            ["curl", "-sL", "--max-time", "30", "-w", "\n@@%{http_code}", "-A", UA, url],
            capture_output=True, text=True, timeout=45)
        body = p.stdout
        code = body.rsplit("\n@@", 1)[-1].strip()
        m = REC.search(body)
        if code != "200":
            return {"bot_id": bid, "url": url, "status": code, "ok": False,
                    "reason": f"http {code}"}
        if not m:
            return {"bot_id": bid, "url": url, "status": code, "ok": False,
                    "reason": "200 but no share record (draft/team-only/unpublished)"}
        rec = {k: clean(v) for k, v in m.groupdict().items()}
        if rec["bid"] != bid:
            return {"bot_id": bid, "url": url, "status": code, "ok": False,
                    "reason": f"payload id mismatch ({rec['bid']})"}
        if not rec["name"]:
            return {"bot_id": bid, "url": url, "status": code, "ok": False,
                    "reason": "live but unnamed template"}
        return {"bot_id": bid, "url": url, "status": code, "ok": True,
                "owner_type": rec["own"], "sharer": rec["sharer"],
                "name": rec["name"], "desc": rec["desc"]}
    except Exception as e:  # noqa: BLE001
        return {"bot_id": bid, "url": url, "ok": False, "reason": f"error {e}"}


def main():
    ids = [a for a in sys.argv[1:] if a]
    out = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(fetch, ids):
            out.append(r)
    for r in out:
        print(json.dumps(r))
    ok = [r for r in out if r.get("ok")]
    print(f"checked={len(out)} live_named={len(ok)}", file=sys.stderr)


if __name__ == "__main__":
    main()
