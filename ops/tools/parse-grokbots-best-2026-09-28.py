#!/usr/bin/env python3
"""Parse the grokbots.best embedded payload (the other main firehose).

Records: {"id","slug","name","description","author","type","link",
"source_url","categories","integrations","published","install_count",
"created_at","updated_at"} - escaped one level.

Usage: python3 ops/tools/parse-grokbots-best-2026-09-28.py <saved.html>
"""
import json
import re
import sys

SCRATCH = "/root/.hermes/cache/scratch/"


def unesc(s):
    return s.replace('\\"', '"').replace('\\\\', '\\')


def next_object(text, start):
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
    text = unesc(open(sys.argv[1]).read())
    recs = {}
    i = text.find('{"id":"')
    while i != -1:
        chunk = next_object(text, i)
        if chunk:
            try:
                o = json.loads(chunk)
            except Exception:  # noqa: BLE001
                o = None
            if o and o.get("link") and str(o["link"]).startswith("https://x.ai/bot/"):
                recs.setdefault(str(o["link"]).rsplit("/", 1)[-1], o)
        i = text.find('{"id":"', i + 1)
    print("records:", len(recs))
    bots = json.load(open("/root/grokbothq/content/bots.json"))
    known = {b["url"] for b in bots}
    new = {k: v for k, v in recs.items() if v["link"] not in known}
    print("not listed:", len(new))
    for k, v in sorted(new.items(), key=lambda x: str(x[1].get("created_at") or "")):
        print("  ", k, "|", v.get("name"), "|", v.get("author"), "|", v.get("published"),
              "|", v.get("created_at"), "|", v.get("categories"), "|", (v.get("description") or "")[:70],
              "|", v.get("source_url"))
    json.dump(recs, open(SCRATCH + "best_records_20260928.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
