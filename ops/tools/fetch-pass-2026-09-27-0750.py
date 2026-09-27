#!/usr/bin/env python3
"""Free sources for the 2026-09-27 07:50 IST scout pass.

1. Expand each grokbot.dev source post via api.fxtwitter.com (free, no auth):
   read author handle + display name + stats, and check whether the post body
   actually carries that candidate's exact share id / x.ai bot URL.
2. Pull the grokbots.best payload (one request) for author handles.

Prints JSONL to /root/.hermes/cache/scratch/posts.jsonl and
/root/.hermes/cache/scratch/best.json.
"""
import json
import re
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
FEED = "/root/.hermes/cache/scratch/gbdev_feed.json"
POSTS = "/root/.hermes/cache/scratch/posts.jsonl"
BEST = "/root/.hermes/cache/scratch/best.json"
BEST_URL = "https://grokbots.best"
IDS = open("/root/.hermes/cache/scratch/ids.txt").read().split()


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    feed = json.load(open(FEED))["items"]
    src = {}
    for it in feed:
        su = it.get("share_url") or ""
        bid = su.rsplit("/", 1)[-1]
        if bid in IDS:
            src[bid] = ((it.get("source") or {}).get("url"), it.get("headline"),
                        it.get("summary"), it.get("slug"))
    out = open(POSTS, "w")
    for bid in IDS:
        url, headline, summary, slug = src.get(bid, (None, None, None, None))
        rec = {"bot_id": bid, "headline": headline, "slug": slug, "summary": summary,
               "source_post": url}
        if url and "x.com/" in url:
            api = "https://api.fxtwitter.com/" + url.split("x.com/", 1)[1]
            try:
                d = json.loads(get(api))
                t = d.get("tweet") or {}
                rec.update({
                    "author": (t.get("author") or {}).get("screen_name"),
                    "author_name": (t.get("author") or {}).get("name"),
                    "views": t.get("views"), "likes": t.get("likes"),
                    "bookmarks": t.get("bookmarks"), "created": t.get("created_at"),
                    "text_carries_id": bid in (t.get("text") or "")
                    or ("x.ai/bot" in (t.get("text") or "")),
                    "text": (t.get("text") or "")[:1200],
                })
                ents = ((t.get("media") or {}).get("external") or {})
                if ents.get("url"):
                    rec["external_url"] = ents["url"]
            except Exception as exc:  # noqa: BLE001
                rec["err"] = str(exc)
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out.flush()
        print(rec["bot_id"], rec.get("author"), rec.get("views"), rec.get("bookmarks"),
              rec.get("text_carries_id"), rec.get("err", ""), flush=True)
    out.close()
    try:
        raw = get(BEST_URL, 45)
        open(BEST, "wb").write(raw)
        print("best:", len(raw), "bytes")
    except Exception as exc:  # noqa: BLE001
        print("best ERR", exc)


if __name__ == "__main__":
    main()
