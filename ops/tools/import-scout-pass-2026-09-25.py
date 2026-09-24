#!/usr/bin/env python3
"""Scout pass 2026-09-25 (cron 359022f62495, kicked off 2026-09-24 23:59 IST): append
the verified set found in the public directories + x.ai/bot/marketplace, refresh the
candidate queue (cap 50), and log every link that was opened but not listed.

Sources this pass (all free):
  - x.ai/bot/marketplace (RSC payload carries a creatorName + handle per row)
  - grokbots.best (embedded records with author handle + the creator's own post)
  - grokbots.page, x.ai/bot, x.ai/news, api.fxtwitter.com, web_search

Deterministic and idempotent: re-running will not double-add (dedupe on url+slug).
"""
import json
import os
import re
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
OUT = "/root/.hermes/cache/scratch/scout24"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")

GBEST = "https://grokbots.best/"
MKT = "https://x.ai/bot/marketplace"

# bot_id -> (slug, category, source)
PLAN = {
    # --- x.ai/bot/marketplace rows (creatorName + handle come from the same row)
    "eFnHzlDcKdoA406SzZbNZ": ("pfp-bot", "creative", MKT),
    "c47Jj2QSSR1UXEcuBgUtQ": None,  # DUPLICATE: same creator (SawyerMerritt) already listed
    "TxB-fy1KryaYJLYWBcGtT": None,  # DUPLICATE: identical description already listed
    "i2hvaEONDg6_gEF5C9RlK": None,  # DUPLICATE: identical description already listed
    "-L1yFJ5mtwPgn3O_iYUo_": None,  # DUPLICATE: same creator (ThisWeeknAI) already listed
    "-hmCmHB0ynJGvSKxeINfS": None,  # DUPLICATE: same creator (poteto) already listed
    "0LLQmzk-yzwHi0zuiV0lC": None,  # DUPLICATE: same creator (lingxi) already listed
    "pXNvc_U2cGyZmheYrUuF_": None,  # DUPLICATE: same creator (johnbai) already listed
    "ph-u_zkF5Vui1GdGnysn9": None,  # DUPLICATE: identical description already listed
    "q4u8YgzGQqCAOUZcg0Lgt": None,  # DUPLICATE: identical description already listed
    # --- grokbots.best records (author handle + that creator's own post)
    "1fdwKWpdKjtdLYUTskkey": ("prostetnic-vogon-jeltz", "creative", GBEST),
    "4mOGY7Nd_mRvrwZYec4Jq": None,  # DUPLICATE: identical description already listed
    "6DuTZ4NrJazU1YO4Llcx0": ("food-truck-marketplace-cto", "engineering", GBEST),
    "6uqwQQpLVpsSYJPG2QIEp": ("inbox-cleaner", "productivity", GBEST),
    "7epNk1Xu5vSOdiwf9xgww": ("comfy-workflow-buddy", "creative", GBEST),
    "AfpFyeysGxUyH9bAgjvGy": ("applicoti", "productivity", GBEST),
    "CLpDye-rKhP9cFMFRet3z": ("moola", "money", GBEST),
    "EQgLIMO5Q_sVk3iM9EQbZ": ("full-spectrum-law-firm-os", "productivity", GBEST),
    "Ed-L-mUFR_9nR2BYMssNF": ("chef-chad", "life", GBEST),
    "FGFMxol1pBRT2TmjmtIod": ("aila-lead", "productivity", GBEST),
    "FwtiQchlHexgCdlDo5WkL": ("smooth-brains-bot", "money", GBEST),
    "MT6acytP70wHR526vPvM3": None,  # EXCLUDED: bot is named "Grok Bot" (product name)
    "NVpdpaSAKHtd1qH6VH9vc": ("spruce", "life", GBEST),
    "QCwGPAlho0dBvBds_IOWF": None,  # EXCLUDED: persona of a real named individual
    "RTQ5cLf2WeWJPyjD8YSWr": ("goonie", "life", GBEST),
    "Rv893FcX1cPsVnr-wJpo6": ("ranch-bot", "productivity", GBEST),
    "SR14quBvqUyS-K0DqlDL8": ("doctor-md", "life", GBEST),
    "SRFGtB_-g8py4h4ijbdF2": ("a1-charity", "life", GBEST),
    "Xg1_LIUG80iz5065crarS": ("toujianli-apply", "productivity", GBEST),
    "_6ZWfvMmBLOS1rxFFezl6": ("weather-bot", "life", GBEST),
    "i7hwU3YzCKt_27dK9aCr4": ("easy-flow", "productivity", GBEST),
    "jOOljWGDKOTQIZRtRBWCQ": ("m2q2", "engineering", GBEST),
    "nylU6e_GXKCzJvLLxN6qW": ("guanchao-market-watch", "money", GBEST),
    "qtuoVRf5etpEVPNA29i7H": None,  # EXCLUDED: creator's description is "free webpages"
    "s9EKFwbfQkmKK9jL44YoP": ("chargeright-panel-coach", "engineering", GBEST),
    "Ed-L-mUFR_9nR2BYMssNF": None,  # DUPLICATE: "Chef Chad" already listed (see below)
}
# A second share id for a bot the directory already carries. The old link is still
# live, so nothing is broken; adding these would put two identical names in the grid.
# Where the description differs, the newer template is credited in the PR body as a
# candidate for enrichment rather than silently swapped under an existing listing.
DUPES = [
    ("c47Jj2QSSR1UXEcuBgUtQ", "Home robots", "home-robots", "SawyerMerritt", "same creator"),
    ("-L1yFJ5mtwPgn3O_iYUo_", "Clip Bot", "clip-bot", "ThisWeeknAI", "same creator"),
    ("-hmCmHB0ynJGvSKxeINfS", "tinkabot", "tinkabot", "poteto", "same creator"),
    ("0LLQmzk-yzwHi0zuiV0lC", "Nightly Audit Engineer", "nightly-audit-engineer", "lingxi",
     "same creator"),
    ("pXNvc_U2cGyZmheYrUuF_", "figma bro", "figma-bro", "johnbai", "same creator"),
    ("TxB-fy1KryaYJLYWBcGtT", "last30days", "last30days", "mvanhorn", "identical description"),
    ("i2hvaEONDg6_gEF5C9RlK", "Researchy", "researchy", "farzyness", "identical description"),
    ("ph-u_zkF5Vui1GdGnysn9", "Product Idea Stress Test", "product-idea-stress-test",
     "hnshah", "identical description"),
    ("q4u8YgzGQqCAOUZcg0Lgt", "Credit Card Max", "credit-card-max", "trevin",
     "identical description"),
    ("4mOGY7Nd_mRvrwZYec4Jq", "The List", "the-list", "GrokBotGod", "identical description"),
    ("Ed-L-mUFR_9nR2BYMssNF", "Chef Chad", "chef-chad", "RRomanoly",
     "same bot name; the listed copy credits a different account (Llama Mama)"),
]
DUPE_ROWS = [
    {"bot_id": bid, "name": name, "url": f"https://x.ai/bot/{bid}",
     "duplicate_of": f"{slug} (existing x.ai/bot link still live)",
     "creator_handle": handle, "reason": reason}
    for bid, name, slug, handle, reason in DUPES
]
# reviewed live, deliberately not queued
NOT_ADDED = [
    {"bot_id": "Pa8G-Ldh5jU_jozWEu2Cs", "name": "Grok Bot (blank template)",
     "url": "https://x.ai/bot/Pa8G-Ldh5jU_jozWEu2Cs",
     "reason": "200 but no share record on the page; the record only carries the "
               "stock line \"Use this template to create a new bot\""},
    {"bot_id": "Uy2oK9854UViaiO0rQ6nC", "name": "Grok Bot (blank template)",
     "url": "https://x.ai/bot/Uy2oK9854UViaiO0rQ6nC",
     "reason": "same as above — stock boilerplate, nothing to list"},
    {"bot_id": "hEmSUvWxccmfAVDGri1R8", "name": "Grok Bot (blank template)",
     "url": "https://x.ai/bot/hEmSUvWxccmfAVDGri1R8",
     "reason": "same as above — stock boilerplate, nothing to list"},
    {"bot_id": "QCwGPAlho0dBvBds_IOWF", "name": "Elon Musk (Algorithm & constraint)",
     "url": "https://x.ai/bot/QCwGPAlho0dBvBds_IOWF",
     "reason": "persona of a real named individual — same rule that kept the earlier "
               "\"Elon Musk\" and \"Steve Jobs\" templates out"},
    {"bot_id": "MT6acytP70wHR526vPvM3", "name": "Grok Bot",
     "url": "https://x.ai/bot/MT6acytP70wHR526vPvM3",
     "reason": "third-party template named exactly \"Grok Bot\" — listing it under that "
               "name would read as an xAI/ SpaceXAI template"},
    {"bot_id": "qtuoVRf5etpEVPNA29i7H", "name": "anew",
     "url": "https://x.ai/bot/qtuoVRf5etpEVPNA29i7H",
     "reason": "creator's description is the two words \"free webpages\" — nothing "
               "factual to write a listing from"},
    {"bot_id": "v-anNtCSU16DhOT6XDOpn", "name": "Carson",
     "url": "https://x.ai/bot/v-anNtCSU16DhOT6XDOpn",
     "reason": "200 but no share record (draft or team-only template) — reviewed "
               "2026-09-23 and still not installable by link"},
]
VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}


def load_payload(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    return html.replace('\\"', '"').replace("\\n", " ")


def field(html, key):
    """First JSON-string value for key, unescaped; None when absent."""
    m = re.search(r'"%s":"((?:[^"\\]|\\.)*)"' % key, html)
    if not m:
        return None
    try:
        return json.loads('"' + m.group(1) + '"')
    except Exception:  # noqa: BLE001
        return m.group(1)


def tagline(desc: str, limit: int = 140) -> str:
    desc = " ".join(desc.split())
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    return cut[:cut.rfind(" ")].rstrip(" ,;:—–-") + "…"


MANUAL_DESC = {
    # translated from the creator's own Chinese description (see PR body)
    "Xg1_LIUG80iz5065crarS": (
        "Filters job postings on Chinese boards such as 51job against your own screening "
        "criteria and submits applications, and can also email your resume to public hiring "
        "inboxes. Each round reports how many roles were filtered, how many were applied to, "
        "why anything was skipped, and where it got stuck."),
    "nylU6e_GXKCzJvLLxN6qW": (
        "Cross-market investment research assistant: follows A-shares, Hong Kong and US "
        "equities plus macro by session, compares them against your holdings and watchlist, "
        "and logs the setups worth revisiting. Short briefs by default with the full write-up "
        "on request. Not investment advice."),
    # the marketplace payload truncates these two, so use what the page renders
    "AfpFyeysGxUyH9bAgjvGy": None,
    "i7hwU3YzCKt_27dK9aCr4": (
        "Turns pasted notes or a GitHub doc or repo path into a readable end-user flowchart, "
        "with the happy path as the default output. First run asks you to accept the tool's AI "
        "agent disclaimer, then to pick the diagram format you want by default."),
}


def main():
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_urls = {b["url"] for b in bots}
    have_slugs = {b["slug"] for b in bots}
    gbest = {r["id"]: r for r in json.load(open(f"{OUT}/gbest_new.json"))}
    mkt = {r["bot_id"]: r for r in json.load(open(f"{OUT}/mkt_records.json"))}
    extra = {r["bot_id"]: r for r in json.load(open(f"{OUT}/extra.json"))}

    added = []
    for bid, plan in PLAN.items():
        if plan is None:
            continue
        slug, cat, src = plan
        url = f"https://x.ai/bot/{bid}"
        page = f"{OUT}/pages/{bid}.html"
        assert os.path.exists(page), f"no captured page for {bid}"
        html = load_payload(page)
        name = field(html, "botName") or (gbest.get(bid) or {}).get("name")
        desc = (gbest.get(bid) or {}).get("desc") or ""
        # the page's own rendered description wins when the share payload is short/absent
        if MANUAL_DESC.get(bid):
            desc = MANUAL_DESC[bid]
        if len(desc.strip()) < 40:
            meta = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"',
                             open(page, encoding="utf-8", errors="replace").read())
            if meta:
                desc = meta.group(1)
        assert name and name.strip(), bid
        assert desc and len(desc.strip()) >= 40, f"thin description for {bid}"
        assert url not in have_urls, f"{url} already listed"
        assert slug not in have_slugs, f"slug collision {slug}"
        assert re.fullmatch(r"[a-z0-9\-]+", slug), slug
        assert cat in VALID_CATS, cat

        rec = gbest.get(bid) or {}
        if bid in mkt:  # x.ai's own marketplace row is authoritative for this listing
            entry_builder = (mkt[bid].get("creator"), mkt[bid].get("handle") or "")
            source = MKT
        elif rec:
            handle = (rec.get("author") or "").lstrip("@")
            entry_builder = (field(html, "sharerName") or handle, handle)
            source = rec.get("source_url") or src
        else:
            entry_builder = (field(html, "sharerName") or "", "")
            source = src
        bname, handle = entry_builder
        entry = {
            "slug": slug,
            "name": name.strip(),
            "builder": {"name": (bname or handle or "").strip(), "x": handle},
            "tagline": tagline(desc),
            "description": desc.strip(),
            "category": cat,
            "url": url,
            "addedAt": TODAY,
            "status": "published",
            "source": source,
        }
        assert len(entry["tagline"]) <= 140, entry["tagline"]
        bots.append(entry)
        have_urls.add(url)
        have_slugs.add(slug)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w"), indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a").write("\n")

    # ---- refresh the candidate queue (50 newest, today's finds first) -------------------
    queue = [{"name": e["name"], "bot_id": e["url"].split("/bot/")[1], "url": e["url"],
              "builder_x_handle": e["builder"]["x"], "one_line_desc": e["tagline"],
              "source_post_url": e["source"], "found_at": STAMP,
              "status": "added to directory in ops/scout-pending"} for e in added]
    for r in NOT_ADDED:
        queue.append({"name": r["name"], "bot_id": r["bot_id"], "url": r["url"],
                      "builder_x_handle": "", "one_line_desc": r["reason"],
                      "source_post_url": "", "found_at": STAMP, "status": "not added"})
    old = json.load(open(f"{REPO}/ops/scout-candidates.json"))
    seen = {q["bot_id"] for q in queue}
    queue += [o for o in old if o.get("bot_id") not in seen]
    json.dump(queue[:50], open(f"{REPO}/ops/scout-candidates.json", "w"),
              indent=2, ensure_ascii=False)

    # ---- exclusions log ----------------------------------------------------------------
    ex = {
        "run": "2026-09-25 scout pass (cron 359022f62495, started 2026-09-24 23:59 IST)",
        "branch": "ops/scout-pending (single accumulating PR)",
        "method": ("Every x.ai/bot link was opened live; a listing was written only when the "
                   "page rendered a real template (name + description) and the record was "
                   "traceable to a creator handle. Zero paid API calls."),
        "counts": {"directories_walked": 4, "links_opened": len(PLAN) + len(NOT_ADDED),
                   "added_to_directory": len(added), "duplicate_of_existing": len(DUPE_ROWS),
                   "not_added": len(NOT_ADDED)},
        "duplicate_of_existing": DUPE_ROWS,
        "not_added": NOT_ADDED,
    }
    json.dump(ex, open(f"{REPO}/ops/scout-exclusions-2026-09-25.json", "w"),
              indent=2, ensure_ascii=False)
    print(f"added {len(added)}; queue {min(len(queue), 50)}; exclusions {len(NOT_ADDED)}")
    for e in added:
        print("  +", e["slug"], "|", e["name"], "|", e["builder"]["x"] or "(no handle)")


if __name__ == "__main__":
    main()
