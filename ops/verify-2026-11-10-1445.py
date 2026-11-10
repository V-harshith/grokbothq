#!/usr/bin/env python3
"""Verify mapped candidates live on x.ai: 200 + name present in body. Free GETs only."""
import json, re, glob, sys, time, urllib.request, html as ihtml

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = "/root/grokbothq"
SCR = "/root/.hermes/cache/scratch"
LINK = re.compile(r"x\.ai/bot/([A-Za-z0-9_\-]{10,30})")


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.getcode(), r.read().decode("utf-8", "replace")


def known_ids():
    known = set()

    def add(v):
        if isinstance(v, str):
            m = LINK.search(v)
            if m:
                known.add(m.group(1).lower())

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                add(k)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for b in json.load(open(f"{ROOT}/content/bots.json")):
        add(b.get("url", ""))
    for f in glob.glob(f"{ROOT}/ops/*.json"):
        try:
            walk(json.load(open(f)))
        except Exception:
            pass
    return known


def main():
    mapped = json.load(open(f"{SCR}/mapped-2026-11-10-1445.json"))
    known = known_ids()
    seen = set()
    cands = []
    for m in mapped:
        bid = m["bot_id"]
        if bid.lower() in known or bid.lower() in seen:
            continue
        seen.add(bid.lower())
        cands.append(m)
    print(f"mapped={len(mapped)} dedup_new={len(cands)}", file=sys.stderr)

    ok, bad = [], []
    for m in cands:
        url = f"https://x.ai/bot/{m['bot_id']}"
        try:
            code, body = get(url)
        except Exception as e:
            bad.append({**m, "reason": f"fetch error {e}"})
            continue
        if code != 200:
            bad.append({**m, "reason": f"http {code}"})
            continue
        txt = ihtml.unescape(re.sub(r"<[^>]+>", " ", body))
        name = m["name"] or ""
        # accept the name as-is, or its first meaningful token set (titles carry suffixes)
        probe = name.split(" · ")[0].split("|")[0].strip()
        probe = re.sub(r"\s+", " ", probe)
        if probe and probe.lower() in txt.lower():
            m["page_status"] = 200
            ok.append(m)
        elif len(probe) >= 4:
            # second chance: any 2+ word chunk
            words = [w for w in re.findall(r"[A-Za-z0-9']{4,}", probe)][:2]
            if words and all(w.lower() in txt.lower() for w in words):
                m["page_status"] = 200
                ok.append(m)
            else:
                bad.append({**m, "reason": "name not in body"})
        else:
            bad.append({**m, "reason": "name too short to confirm"})
        if len(ok) + len(bad) % 25 == 0:
            time.sleep(0.2)

    json.dump(ok, open(f"{SCR}/verified-2026-11-10-1445.json", "w"), indent=1, ensure_ascii=False)
    json.dump(bad, open(f"{SCR}/rejected-2026-11-10-1445.json", "w"), indent=1, ensure_ascii=False)
    print(f"verified={len(ok)} rejected={len(bad)}", file=sys.stderr)
    for o in ok:
        print(f"OK   {o['bot_id']} | {o['name']} | {o['author']} | {o['gb_slug']}")
    for b in bad:
        print(f"BAD  {b['bot_id']} | {b['name']} | {b['reason']}")


if __name__ == "__main__":
    main()
