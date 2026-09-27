#!/usr/bin/env python3
"""Extra free surfaces for the 2026-09-27 07:50 IST pass.

- diff the grokbots.best payload links against content/bots.json
- fetch the x.ai/bot/marketplace ItemList and diff it
- fetch grokbotpulse.com and diff the x.ai/bot links it carries
One request per host.
"""
import json
import re
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    known = {b["url"] for b in bots}
    best = json.load(open(SCRATCH + "best_map.json"))
    best_ids = set(best)
    print("grokbots.best entries:", len(best))
    print("best ids already listed:", len({i for i in best_ids if f'https://x.ai/bot/{i}' in known}))
    feed = json.load(open(SCRATCH + "gbdev_feed.json"))["items"]
    feed_ids = {((i.get("share_url") or "").rsplit("/", 1)[-1]) for i in feed if i.get("share_url")}
    unseen = [i for i in best_ids if f"https://x.ai/bot/{i}" not in known and i not in feed_ids]
    print("best ids not listed and not in the registry feed:", len(unseen))
    for i in unseen[:60]:
        print("   BEST-NEW", i, best[i].get("name"), best[i].get("author"))
    open(SCRATCH + "best_unseen.json", "w").write(json.dumps(
        {i: best[i] for i in unseen}, ensure_ascii=False))

    for label, url in (("marketplace", "https://x.ai/bot/marketplace"),
                       ("grokbotpulse", "https://grokbotpulse.com")):
        try:
            html = get(url, 60)
        except Exception as exc:  # noqa: BLE001
            print(label, "ERR", exc)
            continue
        open(f"{SCRATCH}{label}.html", "w").write(html)
        ids = sorted(set(re.findall(r"x\.ai/bot/([A-Za-z0-9_\-]+)", html)))
        new = [i for i in ids if f"https://x.ai/bot/{i}" not in known]
        print(label, "links:", len(ids), "not listed:", len(new), new[:20])


if __name__ == "__main__":
    main()
