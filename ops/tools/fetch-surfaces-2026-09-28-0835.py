#!/usr/bin/env python3
"""Free surfaces for the 2026-09-28 08:35 IST pass.

Diff every x.ai/bot/<id> link these carry against content/bots.json.
One request per host, browser UA. Zero paid calls.
"""
import json
import re
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"
LINK = re.compile(r"x\.ai/bot/([A-Za-z0-9_\-]{8,})")

SURFACES = [
    ("xai_marketplace", "https://x.ai/bot/marketplace"),
    ("xai_marketplace_team", "https://x.ai/bot/marketplace/from-grok-bot-team"),
    ("xai_marketplace_product", "https://x.ai/bot/marketplace/product"),
    ("xai_marketplace_engineering", "https://x.ai/bot/marketplace/engineering"),
    ("xai_marketplace_sales", "https://x.ai/bot/marketplace/sales"),
    ("xai_marketplace_marketing", "https://x.ai/bot/marketplace/marketing"),
    ("xai_marketplace_ops", "https://x.ai/bot/marketplace/operations"),
    ("xai_marketplace_personal", "https://x.ai/bot/marketplace/personal"),
    ("xai_marketplace_design", "https://x.ai/bot/marketplace/design"),
    ("xai_marketplace_recruiting", "https://x.ai/bot/marketplace/recruiting-people"),
    ("grokmarket", "https://grokmarket.io/templates"),
    ("awesome_gh", "https://raw.githubusercontent.com/divo12/awesome-grok-bot-templates/main/README.md"),
    ("grokbotwiki", "https://grokbotwiki.com/bots/catalog.json"),
    ("grokbotpulse", "https://grokbotpulse.com"),
    ("grokbot_templates", "https://grokbot-templates.com"),
    ("grokbots_page", "https://grokbots.page"),
    ("grokbots_best", "https://grokbots.best"),
]


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    known = {b["url"] for b in bots}
    try:
        reg = json.load(open(SCRATCH + "registry_feed.json"))
    except Exception:  # noqa: BLE001
        reg = {}
    reg_items = reg.get("items") if isinstance(reg, dict) else reg
    reg_ids = set()
    for i in (reg_items or []):
        u = (i.get("share_url") or i.get("url") or "")
        m = LINK.search(u)
        if m:
            reg_ids.add(m.group(1))
    seen = {}
    for name, url in SURFACES:
        try:
            body = get(url)
        except Exception as exc:  # noqa: BLE001
            print(f"{name:26s} ERR {exc}")
            continue
        open(f"{SCRATCH}pass0835_{name}.txt", "w").write(body)
        ids = sorted(set(LINK.findall(body)))
        fresh = [i for i in ids if f"https://x.ai/bot/{i}" not in known]
        print(f"{name:26s} links={len(ids):5d} not_listed={len(fresh):4d} {fresh[:12]}")
        for i in fresh:
            seen.setdefault(i, []).append(name)
    json.dump(seen, open(SCRATCH + "pass0835_unseen.json", "w"), indent=1)
    print("union unseen:", len(seen), "| also in registry feed:", len([i for i in seen if i in reg_ids]))


if __name__ == "__main__":
    main()
