#!/usr/bin/env python3
"""Authoritative reader for the x.ai/bot/<id> share record.

Why this exists: the description on these pages can itself contain a
double-quoted phrase (Weekly Recap: `Answers "what did you get done this
week?" ...`). Three earlier readers each died differently on that record:

  * fetch_share_full.py - regex value branch stops at the first escaped quote
                          (read 8 chars instead of 236)
  * verify-bot-links.py  - same class of truncation at the escaped quote

The payload is a Next.js RSC flight stream: the record lives inside
self.__next_f.push([1,"<payload>"]) as an object escaped exactly once. So:
decode each push string with json.loads (level 1), then read the wanted fields
out of that payload with a scanner that counts backslash parity to tell an inner
quote (odd run) from the value terminator (even run), and json.loads the
collected raw to strip the remaining escapes.

Usage: python3 ops/tools/share_record_scan.py id1 id2 ...   (sequential, JSONL)
"""
import json
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
PUSH = re.compile(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)')
FIELDS = ("ownerType", "sharerName", "botName", "description")


def payload(html: str) -> str:
    return "".join(json.loads(m.group(1)) for m in PUSH.finditer(html))


def decode(raw: str):
    try:
        return json.loads('"' + raw + '"')
    except Exception:  # noqa: BLE001
        return raw


def token(p1: str, start: int):
    """Read an escaped string value in `p1` starting at the opening quote.

    The value's own quotes are escaped one level deeper, so the parity of a
    backslash run decides inner quote (odd) vs value terminator (even).
    """
    assert p1[start] == '"', p1[start:start + 20]
    raw = []
    i = start + 1
    while i < len(p1):
        c = p1[i]
        if c == "\\":
            run = 0
            while i + run < len(p1) and p1[i + run] == "\\":
                run += 1
            if i + run < len(p1) and p1[i + run] == '"':
                if run % 2 == 1:
                    raw.append("\\" * (run - 1) + '"')
                    i += run + 1
                    continue
                raw.append("\\" * run)
                return decode("".join(raw)), i + run + 1
            raw.append("\\" * run)
            i += run
            continue
        if c == '"':
            return decode("".join(raw)), i + 1
        raw.append(c)
        i += 1
    return None, i


def extract(html: str, bid: str):
    """Find the share record object in the decoded flight payload.

    At this level the object is ordinary JSON apart from the rest of the flight
    stream around it, so raw_decode from the record's opening brace reads the
    whole object exactly, escaped quotes and all. Fallback: the same object
    escaped one level further (a plain string scan, backslash parity).
    """
    p1 = payload(html)
    if not p1:
        return None
    dec = json.JSONDecoder()
    for pat in (f'{{"id":"{bid}","ownerType":"', f'{{\\"id\\":\\"{bid}\\",\\"ownerType\\":\\"'):
        i = p1.find(pat)
        if i < 0:
            continue
        if pat.startswith('{"'):
            try:
                obj, _ = dec.raw_decode(p1, i)
                if isinstance(obj, dict) and obj.get("id") == bid:
                    return obj
            except Exception:  # noqa: BLE001
                pass
            continue
        p2 = decode(p1[i: i + 6000]) or ""
        j = p2.find("{")
        if j < 0:
            continue
        try:
            obj, _ = dec.raw_decode(p2, j)
            if isinstance(obj, dict) and obj.get("id") == bid:
                return obj
        except Exception:  # noqa: BLE001
            pass
    return None


def fetch(bid: str):
    url = f"https://x.ai/bot/{bid}"
    rec: dict = {"bot_id": bid, "url": url}
    html = ""
    for _ in range(2):
        p = subprocess.run(["curl", "-sL", "--compressed", "--http1.1", "--max-time", "25",
                            "-w", "\n@@%{http_code}", "-A", UA, url],
                           capture_output=True, text=True, timeout=45)
        html = p.stdout
        if html and "@@" in html:
            break
    code = html.rsplit("\n@@", 1)[-1].strip() if "@@" in html else "?"
    rec["status"] = code
    if code != "200":
        rec.update({"ok": False, "reason": f"http {code}"})
        return rec
    got = extract(html, bid)
    if not got or (got.get("botName") is None and got.get("description") is None):
        rec.update({"ok": False,
                    "reason": "200 but no share record (draft/team-only/unpublished)"})
        return rec
    rec.update({"owner_type": got.get("ownerType"), "sharer": got.get("sharerName"),
                "name": got.get("botName"), "desc": got.get("description")})
    rec["ok"] = bool(rec.get("name") and rec.get("desc"))
    if not rec["ok"]:
        rec["reason"] = "empty botName" if not rec.get("name") else "empty description"
    return rec


if __name__ == "__main__":
    for bid in sys.argv[1:]:
        print(json.dumps(fetch(bid), ensure_ascii=False), flush=True)
