#!/usr/bin/env python3
"""Parse grokmarket.io (independent Grok Bot template directory) records.

Each record: {"id","slug","name","author","authorUrl","category","summary",...
"templateUrl":"https://x.ai/bot/<ID>","sourceUrl":"https://x.com/..."}
Payload is escaped one level; unescape then brace-match around each templateUrl.

Usage: python3 ops/tools/parse-grokmarket-2026-09-28.py
"""
import glob
import json
import re

SCRATCH = "/root/.hermes/cache/scratch/"


def unesc(s):
    return s.replace('\\"', '"').replace('\\\\', '\\')


def object_at(text, start):
    depth, i, instr, esc = 0, start, False, False
    while i < len(text):
        c = text[i]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif c == '"':
            instr = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
        i += 1
    return None


def main():
    recs = {}
    for path in sorted(glob.glob(SCRATCH + "gm_*.html")):
        h = open(path).read()
        if len(h) < 5000:
            continue
        text = unesc(h)
        got = 0
        for m in re.finditer(r'"templateUrl":"https://x\.ai/bot/([A-Za-z0-9_\-]+)"', text):
            start = text.rfind("{", 0, m.start())
            chunk = object_at(text, start)
            if not chunk:
                continue
            try:
                obj = json.loads(chunk)
            except Exception:  # noqa: BLE001
                continue
            if obj.get("templateUrl"):
                recs.setdefault(obj.get("id") or m.group(1), obj)
                got += 1
        print(path.rsplit("/", 1)[-1], "records", got)
    print("unique grokmarket records:", len(recs))
    bots = json.load(open("/root/grokbothq/content/bots.json"))
    known = {b["url"] for b in bots}
    new = {k: v for k, v in recs.items() if v.get("templateUrl") not in known}
    print("not listed:", len(new))
    for k, v in new.items():
        print("  ", k, "|", v.get("name"), "|", v.get("author"), "|", v.get("category"), "|",
              (v.get("summary") or "")[:90], "|", v.get("sourceUrl"))
    json.dump(recs, open(SCRATCH + "grokmarket_records.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
