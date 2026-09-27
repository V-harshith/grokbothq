#!/usr/bin/env python3
"""Parse the Grok Bot Marketplace payload (first-party surface) from saved pages.

Each listing is a JSON object starting {"id":"<slug>","name":...,"creatorName":...,
"handle":...,"description":...,"categories":[...],"installCount":N,...,"addHref":"/bot/<ID>"}.
The payload is escaped one level, so unescape once then brace-match around each addHref.

Usage: python3 ops/tools/parse-marketplace-2026-09-28.py
"""
import glob
import json
import re

SCRATCH = "/root/.hermes/cache/scratch/"


def unesc(s: str) -> str:
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
    for path in sorted(glob.glob(SCRATCH + "surface_xai_marketplace*.txt")):
        text = unesc(open(path).read())
        got = 0
        for m in re.finditer(r'"addHref":"/bot/([A-Za-z0-9_\-]+)"', text):
            start = text.rfind("{", 0, m.start())
            chunk = object_at(text, start)
            if not chunk:
                continue
            try:
                obj = json.loads(chunk)
            except Exception:  # noqa: BLE001
                continue
            if obj.get("addHref"):
                recs.setdefault(obj.get("id") or m.group(1), obj)
                got += 1
        print(path.rsplit("/", 1)[-1], "records", got)
    print("unique marketplace bots:", len(recs))
    bots = json.load(open("/root/grokbothq/content/bots.json"))
    known = {b["url"] for b in bots}
    new = {k: v for k, v in recs.items() if f"https://x.ai/bot/{str(v.get('addHref')).rsplit('/', 1)[-1]}" not in known}
    print("not listed by share id:", len(new))
    for k, v in list(new.items())[:60]:
        print("  ", str(v.get("addHref")).rsplit("/", 1)[-1], "|", v.get("name"), "|",
              v.get("creatorName"), v.get("handle"), "|", v.get("categories"), "| installs", v.get("installCount"))
    json.dump(recs, open(SCRATCH + "marketplace_records.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
