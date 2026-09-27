#!/usr/bin/env python3
"""Extra checks before adding: source-post collision vs the live directory,
near-duplicate description scan (re-share detection), and the 6 grokbots.best
candidates whose source post is not in the registry feed."""
import json
import re
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SCRATCH = "/root/.hermes/cache/scratch/"
ROOT = "/root/grokbothq"
BEST6 = ["e5UBnGbfvCyML0pahKPNw", "JOqKmRtk249knj1lWv3dl", "nXIyPDFW9mbmer2qdt4FW",
         "sy364bgoJN8Rb5vZo4Abo", "gJ3AERRL_vWOhTBgKm-2G", "Afwm3MUhTO3TxHYV_wdm6"]


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    known_src = {}
    for b in bots:
        if b.get("source"):
            known_src.setdefault(b["source"].split("?")[0].rstrip("/"), []).append(b["slug"])
    posts = [json.loads(l) for l in open(SCRATCH + "posts.jsonl")]
    scan = {json.loads(l)["bot_id"]: json.loads(l) for l in open(SCRATCH + "scan.jsonl")}
    print("=== source-post collision (feed candidates) ===")
    for p in posts:
        s = (p.get("source_post") or "").split("?")[0].rstrip("/")
        if s in known_src:
            print("  COLLISION", p["bot_id"], s, "->", known_src[s])
    print("=== near-duplicate description scan ===")
    def toks(s):
        return set(re.findall(r"[a-z]{4,}", (s or "").lower()))
    for bid, s in scan.items():
        t = toks(s.get("desc"))
        for b in bots:
            bt = toks(b.get("description"))
            if not t or not bt:
                continue
            j = len(t & bt) / len(t | bt)
            if j > 0.55:
                print(f"  BID {bid} ({s.get('name')}) ~ {b['slug']} ({b['name']}) jaccard {j:.2f}")
    print("=== grokbots.best-only candidates: post expansion ===")
    best = json.load(open(SCRATCH + "best_map.json"))
    out = open(SCRATCH + "posts2.jsonl", "w")
    for bid in BEST6:
        b = best[bid]
        rec = {"bot_id": bid, "name": b.get("name"), "best_author": b.get("author"),
               "best_source": b.get("source_url"), "sharer": None}
        su = b.get("source_url") or ""
        if "x.com/" in su:
            api = "https://api.fxtwitter.com/" + su.split("x.com/", 1)[1].split("?")[0]
            try:
                t = json.loads(get(api)).get("tweet") or {}
                rec.update({"author": (t.get("author") or {}).get("screen_name"),
                            "author_name": (t.get("author") or {}).get("name"),
                            "views": t.get("views"), "bookmarks": t.get("bookmarks"),
                            "created": t.get("created_at"),
                            "exact_id_in_text": bid in (t.get("text") or ""),
                            "text": (t.get("text") or "")[:900]})
            except Exception as exc:  # noqa: BLE001
                rec["err"] = str(exc)
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(" ", bid, rec.get("best_author"), rec.get("author"), rec.get("author_name"),
              rec.get("views"), rec.get("exact_id_in_text"), rec.get("err", ""))
    out.close()


if __name__ == "__main__":
    main()
