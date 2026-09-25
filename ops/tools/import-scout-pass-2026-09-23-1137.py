#!/usr/bin/env python3
"""This run's scout import: append the verified pass set to content/bots.json,
refresh ops/scout-candidates.json (cap 50 newest) and log the skip.

Deterministic, idempotent: re-running will not double-add (dedupe on url + slug).
"""
import json
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")
SRC_GITHUB = "https://github.com/cs68614-hash/awesome-grokbot-templates"

# bot_id -> (slug, category)
PLAN = {
    "-HSQcnXiifDMwXqkgMix9": ("grok-build-independentdocx", "engineering"),
    "DwV395eKDJOWYtjcqVbAb": ("onboard-bot", "productivity"),
    "Eny_bgU-fpZdifOm_QN-C": ("demo-builder", "engineering"),
    "GD3ihBmx3ZbfEH0GzNqOT": ("house-cleaner", "productivity"),
    "Gx0HlW1t8lTnW2pVn0nKF": ("ramp-bot", "money"),
    "IWfeUN5d0Ad8vwfhxQycG": ("engineering-loop-pm", "engineering"),
    "KaC99w7qlJ0QTtrKwxqFm": ("kilo", "productivity"),
    "LtgFNOt7Y-bmSnixM1yAj": ("astro-jerry", "research"),
    "NgVzsPCqf9_qdNWLs9NAQ": ("uk-healthops", "life"),
    "O-7W0uf0-_raG54kvXQcV": ("soulsie-riff", "creative"),
    "OXHJeOy_Iwk5dMCcjdO1v": ("kids-activity-scheduler", "life"),
    "OuHK7dyYD8C6Joqw80yfJ": ("ai-health", "life"),
    "TtbtDOEfnPntO9DWANx3P": ("linkedin-agent", "sales"),
    "VpXAZQg8JIr4YbrgwwqCf": ("restauranthero", "life"),
    "WMLSz9eCswzYR8nPmmxsJ": ("chief-of-staff-amine", "productivity"),
    "Y8YOrZBsPE8U-jyTI7Qtk": ("garden-retail-research-specialist", "research"),
    "aUHkBXXwCzljCcTJSzBYw": ("codex", "engineering"),
    "bLjgwE9D7HtZ17fVQc53o": ("sharenow-bot", "creative"),
    "buqKPC6jkQxBPdY93HL-w": ("business-loop-pm", "money"),
    "cgaQkN_5O5NtWep6-c0Ll": ("flip", "money"),
    "eb1UwzjTfdNsYRfUh599j": ("product-loop-pm", "productivity"),
    "jYajAanyKBO7aTMQ3zxUL": ("ime-chart-review", "research"),
    "py3cDcRaSgRj_ixBOK3XN": ("xgas-superchain-dapp-supercycle", "engineering"),
    "qG_ZROllzSSRGKx_iIbsQ": ("media-manager", "creative"),
    "sX5M7dv2lxhG7V_utytG7": ("scroll", "research"),
    "tes3TMV3WjinLazIM9N_n": ("routines", "productivity"),
}
VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}

# verified live but deliberately NOT added: same bot, re-shared (alias)
SKIPPED = [{
    "bot_id": "fY1xwWCLzDDGVe3GwH78j",
    "name": "Lingxi's Engineer Bot",
    "sharer": "Lingxi Li",
    "url": "https://x.ai/bot/fY1xwWCLzDDGVe3GwH78j",
    "reason": "duplicate of listed lingxis-engineer-bot (same builder, near-identical "
              "description; already carried at https://x.ai/bot/SxqbG1NT5qEw7ggmHqQu_)",
}]


def tagline(desc: str, limit: int = 140) -> str:
    desc = desc.strip()
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    cut = cut[:cut.rfind(" ")].rstrip(" ,;:—-")
    return cut + "…"


def main():
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_urls = {b["url"] for b in bots}
    have_slugs = {b["slug"] for b in bots}
    rows = {r["bot_id"]: r for r in
            (json.loads(l) for l in open("/tmp/verified.json")) if r.get("ok")}

    added = []
    for bid, (slug, cat) in PLAN.items():
        r = rows[bid]
        url = f"https://x.ai/bot/{bid}"
        assert url not in have_urls, f"{url} already listed"
        assert slug not in have_slugs, f"slug collision {slug}"
        assert cat in VALID_CATS, cat
        assert r["name"].strip(), bid
        desc = r["desc"].strip()
        entry = {
            "slug": slug,
            "name": r["name"].strip(),
            "builder": {"name": r["sharer"].strip(), "x": ""},
            "tagline": tagline(desc),
            "description": desc,
            "category": cat,
            "url": url,
            "addedAt": TODAY,
            "status": "published",
            "source": SRC_GITHUB,
        }
        assert len(entry["tagline"]) <= 140, entry["tagline"]
        # em-dashes are kept verbatim: the tagline is the creator's own summary
        # text, and 220 existing taglines in the directory carry them.
        bots.append(entry)
        have_urls.add(url)
        have_slugs.add(slug)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w"), indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a").write("\n")

    # candidates queue: this pass's finds first, cap 50 newest
    cands = json.load(open(f"{REPO}/ops/scout-candidates.json"))
    cand_urls = {c["url"] for c in cands}
    fresh = []
    for e in added:
        if e["url"] in cand_urls:
            continue
        fresh.append({
            "name": e["name"],
            "bot_id": e["url"].rsplit("/", 1)[-1],
            "url": e["url"],
            "builder_x_handle": "",
            "one_line_desc": e["tagline"],
            "source_post_url": SRC_GITHUB,
            "found_at": STAMP,
            "status": "added to directory in ops/scout-pending",
        })
    merged = fresh + cands
    json.dump(merged[:50], open(f"{REPO}/ops/scout-candidates.json", "w"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/ops/scout-candidates.json", "a").write("\n")

    exc_path = f"{REPO}/ops/scout-exclusions-2026-09-23.json"
    exc = json.load(open(exc_path))
    exc.setdefault("not_added", {})["pass_1137_verified_but_skipped"] = SKIPPED
    json.dump(exc, open(exc_path, "w"), indent=2, ensure_ascii=False)
    open(exc_path, "a").write("\n")

    print(f"added {len(added)} bots; total now {len(bots)}; "
          f"candidates {len(merged)} -> kept {min(len(merged), 50)}")
    for e in added:
        print(f"  + {e['slug']:42s} {e['name']} ({e['category']})")


if __name__ == "__main__":
    main()
