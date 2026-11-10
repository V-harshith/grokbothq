#!/usr/bin/env python3
"""2026-11-10 14:45 IST scout: map grokbots.best new rows -> x.ai/bot ids (free, no auth)."""
import json, re, os, sys, time, urllib.request, unicodedata

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = "/root/grokbothq"
SCR = "/root/.hermes/cache/scratch"
LINK = re.compile(r"x\.ai/bot/([A-Za-z0-9_\-]{10,30})")


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def templates_on(page):
    """Pull every embedded {name,link,author,description} record out of the page."""
    out = []
    # the page embeds JSON-in-JSON; unescape once then find records
    t = page.replace('\\"', '"')
    for m in re.finditer(r'\{[^{}]*?"link"\s*:\s*"https://x\.ai/bot/[A-Za-z0-9_\-]{10,30}"[^{}]*?\}', t):
        chunk = m.group(0)
        def f(k):
            mm = re.search(r'"%s"\s*:\s*"((?:[^"\\]|\\.)*)"' % k, chunk)
            return mm.group(1) if mm else ""
        link = f("link")
        out.append({
            "bot_id": LINK.search(link).group(1),
            "name": f("name"),
            "author": f("author"),
            "description": f("description"),
            "source_url": f("source_url") if f("source_url") != "null" else "",
        })
    # dedupe by bot_id
    seen, uniq = set(), []
    for o in out:
        if o["bot_id"] in seen:
            continue
        seen.add(o["bot_id"])
        uniq.append(o)
    return uniq


def main():
    rows = json.load(open(f"{SCR}/gb-best.json"))
    rows = [r for r in rows if str(r.get("created_at", "")) >= "2026-11-08T20:00"]
    rows.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    print(f"rows to map: {len(rows)}", file=sys.stderr)
    mapped = []
    for i, r in enumerate(rows, 1):
        url = r["url"]
        try:
            page = get(url)
        except Exception as e:
            print(f"  [{i}] FAIL {r['slug']}: {e}", file=sys.stderr)
            continue
        tpls = templates_on(page)
        if not tpls:
            print(f"  [{i}] no templates {r['slug']}", file=sys.stderr)
            continue
        want = norm(r["name"])
        pick = None
        for t in tpls:
            if norm(t["name"]) == want:
                pick = t
                break
        if pick is None:
            for t in tpls:
                if want and (want in norm(t["name"]) or norm(t["name"]) in want):
                    pick = t
                    break
        if pick is None and len(tpls) == 1:
            pick = tpls[0]
        if pick is None:
            print(f"  [{i}] ambiguous {r['slug']} ({len(tpls)} recs)", file=sys.stderr)
            continue
        pick = dict(pick)
        pick["gb_slug"] = r["slug"]
        pick["gb_name"] = r["name"]
        pick["gb_desc"] = r["description"]
        pick["gb_source"] = r.get("source_url") or ""
        pick["gb_author"] = r.get("author") or ""
        pick["created_at"] = r.get("created_at")
        mapped.append(pick)
        time.sleep(0.3)
    json.dump(mapped, open(f"{SCR}/mapped-2026-11-10-1445.json", "w"), indent=1, ensure_ascii=False)
    print(f"mapped: {len(mapped)}", file=sys.stderr)
    for m in mapped:
        print(m["bot_id"], "|", m["name"], "|", m["author"])


if __name__ == "__main__":
    main()
