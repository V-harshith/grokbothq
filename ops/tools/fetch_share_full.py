#!/usr/bin/env python3
"""Full share-record description for an x.ai/bot/<id> page.

The page ships the record twice inside an RSC flight payload as double-escaped
JSON: first in the react-query cache (complete), then echoed in the $L3d
children. og:/meta tags carry only a ~155-char truncation. So: collapse one
level of escaping, then read the fields that follow the id, and json.loads each
string literal to undo the remaining escapes.

Usage: python3 ops/tools/fetch_share_full.py id1 id2 ...   (sequential, JSONL out)
"""
import json
import re
import subprocess
import sys

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def collapse(body: str) -> str:
    return body.replace('\\\\"', '"').replace('\\"', '"')


def str_or_null(pattern: str, text: str):
    m = re.search(pattern, text)
    if not m:
        return None
    raw = m.group(1)
    if raw == "null":
        return None
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    try:
        return json.loads('"' + raw + '"')
    except Exception:  # noqa: BLE001
        return raw


def fetch(bid: str):
    url = f"https://x.ai/bot/{bid}"
    rec = {"bot_id": bid, "url": url}
    for _ in range(2):
        p = subprocess.run(["curl", "-sL", "--compressed", "--http1.1", "--max-time", "15", "-A", UA, url],
                           capture_output=True, text=True, timeout=30)
        if p.stdout:
            break
    body = p.stdout
    if not body:
        rec.update({"ok": False, "reason": "empty body"})
        return rec
    rec["status"] = "200" if 'rel="canonical"' in body else "?"
    if f'bot/{bid}' not in body:
        rec.update({"ok": False, "reason": "id not in page"})
        return rec
    text = collapse(body)
    head = f'"id":"{bid}","ownerType":"'
    i = text.find(head)
    if i < 0:
        rec.update({"ok": False, "reason": "no share record"})
        return rec
    seg = text[i:i + 6000]
    rec["owner_type"] = str_or_null(r'"ownerType":"([^"]*)"', seg)
    rec["sharer"] = str_or_null(r'"sharerName":("(?:[^"\\]|\\.)*"|null)', seg)
    rec["name"] = str_or_null(r'"botName":("(?:[^"\\]|\\.)*"|null)', seg)
    rec["desc"] = str_or_null(r'"description":("(?:[^"\\]|\\.)*"|null)', seg)
    rec["ok"] = bool(rec["name"] and rec["desc"])
    if not rec["ok"]:
        rec["reason"] = "empty botName" if not rec["name"] else "empty description"
    return rec


if __name__ == "__main__":
    for bid in sys.argv[1:]:
        print(json.dumps(fetch(bid), ensure_ascii=False), flush=True)
