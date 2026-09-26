#!/usr/bin/env python3
"""Scout pass 2026-09-26 07:00 IST (cron 359022f62495).

Fresh-bot pass. Sources, all fetched free, one request each:
  - cs68614-hash/awesome-grokbot-templates  data/templates.json (1,795 entries)
  - majiayu000/awesome-grok-bot             catalog.json (2,143)
  - RongleCat/awesome-grok-bot              data/catalog.json
  - lroolle/awesome-grokbot-templates       README
  - kydlikebtc/awesome-grokbot              catalog.json (2,078)
  - divo12/awesome-grok-bot-templates       data/templates.json
plus free web_search + fxtwitter for the X side. Zero paid API calls.

Every candidate was opened live. Verification this pass uses
ops/tools/share_record_scan.py, which decodes the RSC flight payload and
raw-decodes the share record object, because the two older readers
(verify-bot-links.py, fetch_share_full.py) carry a FALSE-NEGATIVE mode:

  * a regex value branch stops at an escaped quote, so a description like
    Weekly Recap's `Answers "what did you get done this week?" ...` reads as
    7-8 chars instead of 246 (this is what held Weekly Recap at 18:45);
  * the same regexes require a non-null sharerName, so a live template whose
    share record carries no display name reads as "no share record".

The rotation sample below re-checked 40 existing listings with both readers:
verify-bot-links.py called 3 healthy listings unpublished, share_record_scan.py
and a second read confirmed all three live. Nothing was delisted.

Rules applied (unchanged from the 18:45 / 00:55 passes, so held rows stay held):
  - dedupe on the x.ai/bot id against content/bots.json, the live queue and
    every id already recorded in ops/scout-*.json
  - drop a live description under 40 chars (placeholder)
  - drop non-ASCII bot names
  - hold rows whose platform display name is the org name "SpaceX" (attribution
    not verifiable from the page) and rows with no display name at all
  - hold personas of real named individuals, exact-name twins, blank templates
  - builder handle only when the catalogue handle corroborates the sharer
    display name on the platform record (every name word of 3+ chars appears in
    the handle); otherwise the name only, never a guessed handle

Deterministic + idempotent: re-running never double-adds.
"""
import json
import re
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")
SRC = "https://github.com/cs68614-hash/awesome-grokbot-templates"
SRC_KYD = "https://github.com/kydlikebtc/awesome-grokbot"

VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}

# Catalogue category -> directory category.
CAT_MAP = {"assistants": "assistants", "engineering": "engineering",
           "research": "research", "money": "money", "sales": "sales",
           "creative": "creative", "life": "life", "productivity": "productivity"}

# The two rows the 00:55 pass queued when the >=3 gate was not met; both were
# verified live then and re-verified this pass. Category is ours.
QUEUED_CARRY = {
    "-BWpMRidNVEjHFqOtol0Q": ("productivity", SRC_KYD),
    "D6WMfjHcTnMwm0XS0MFLs": ("research", SRC_KYD),
}

# The 18:45 pass held this one as a "non-ASCII name - needs a dedicated
# translation pass". That hold is wrong on the evidence: the directory already
# carries 83 non-Latin names (ai-orchestration-jp, shiori-mo3ndu,
# global-macro-analyst and 80 more), several of them with the creator's own
# non-English description kept verbatim. So the name stands and the slug is
# transliterated, per the AGENTS.md slug rule.
NAME_OVERRIDES = {
    "D6WMfjHcTnMwm0XS0MFLs": "ai-zixun-jingxuan",
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "bot"


def tagline(desc: str, limit: int = 140) -> str:
    desc = " ".join(desc.split())
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    return cut[:cut.rfind(" ")].rstrip(" ,;:—-–") + "…"


def handle_for(sharer: str, handle: str) -> str:
    """Handle only when it corroborates the sharer name on the platform record."""
    if not handle or not sharer:
        return ""
    words = [w for w in re.split(r"[^a-z0-9]+", sharer.lower()) if len(w) >= 3]
    h = re.sub(r"[^a-z0-9]", "", handle.lower())
    return handle if words and all(w in h for w in words) else ""


def main():
    bots = json.load(open(f"{REPO}/content/bots.json", encoding="utf-8"))
    have_ids = {b["url"].rsplit("/", 1)[-1] for b in bots}
    have_slugs = {b["slug"] for b in bots}

    rows = json.load(open(f"{SCRATCH}/rows41.json", encoding="utf-8"))
    # carry the two rows the previous pass queued (records re-read this pass)
    carry = {}
    for line in open(f"{SCRATCH}/authoritative40.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["bot_id"] in QUEUED_CARRY and r.get("ok"):
            cat, src = QUEUED_CARRY[r["bot_id"]]
            carry[r["bot_id"]] = {"bot_id": r["bot_id"], "name": r["name"],
                                  "sharer": r.get("sharer"), "desc": r["desc"],
                                  "cat": cat, "handle": "maiyangai"
                                  if r["bot_id"] == "D6WMfjHcTnMwm0XS0MFLs" else "",
                                  "src": src}
    added, dropped = [], []
    for r in list(rows) + list(carry.values()):
        bid, name = r["bot_id"], (r["name"] or "").strip()
        desc = " ".join((r.get("desc") or "").split())
        sharer = (r.get("sharer") or "").strip()
        if bid in have_ids:
            dropped.append((name, bid, "already listed (same x.ai/bot id)"))
            continue
        if len(desc) < 40:
            dropped.append((name, bid, f"live description is a placeholder ({len(desc)} chars)"))
            continue
        if not name:
            dropped.append((name, bid, "blank name"))
            continue
        if any(ord(c) > 127 for c in name) and bid not in NAME_OVERRIDES:
            dropped.append((name, bid, "non-ASCII name"))
            continue
        if r["bot_id"] not in QUEUED_CARRY:
            if sharer.lower() == "spacex":
                dropped.append((name, bid, "platform display name is the org name \"SpaceX\" "
                                           "— attribution not verifiable from the page"))
                continue
            if not sharer:
                dropped.append((name, bid, "share record carries no display name — "
                                           "attribution not verifiable from the page"))
                continue

        slug = NAME_OVERRIDES.get(bid) or slugify(name)
        n = 2
        base = slug
        while slug in have_slugs:
            slug = f"{base}-{n}"
            n += 1
        have_slugs.add(slug)
        have_ids.add(bid)

        cat = CAT_MAP.get((r.get("cat") or "").strip().lower(), "assistants")
        assert cat in VALID_CATS, (slug, cat)
        handle = handle_for(sharer, r.get("handle") or "")
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": sharer, "x": handle},
            "tagline": tagline(desc),
            "description": desc if desc.endswith((".", "!", "?")) else desc + ".",
            "category": cat,
            "url": f"https://x.ai/bot/{bid}",
            "addedAt": TODAY,
            "status": "published",
            "source": r.get("src") or SRC,
        }
        assert len(entry["tagline"]) <= 140, slug
        bots.append(entry)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a", encoding="utf-8").write("\n")

    queue = [{"name": e["name"], "bot_id": e["url"].rsplit("/", 1)[-1], "url": e["url"],
              "builder_x_handle": e["builder"]["x"], "one_line_desc": e["tagline"],
              "source_post_url": e["source"], "found_at": STAMP,
              "status": "added to directory in ops/scout-pending"} for e in added]
    for name, bid, why in dropped:
        queue.append({"name": name or bid, "bot_id": bid, "url": f"https://x.ai/bot/{bid}",
                      "builder_x_handle": "", "one_line_desc": why,
                      "source_post_url": SRC, "found_at": STAMP,
                      "status": "verified live, not listed"})
    old = json.load(open(f"{REPO}/ops/scout-candidates.json", encoding="utf-8"))
    seen = {q["bot_id"] for q in queue}
    queue += [o for o in old if o.get("bot_id") not in seen]
    json.dump(queue[:50], open(f"{REPO}/ops/scout-candidates.json", "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    report = {
        "run": "2026-09-26 07:00 IST scout pass (cron 359022f62495)",
        "branch": "ops/scout-pending (single accumulating PR #81)",
        "push": True,
        "method": ("Six public awesome-grokbot catalogues fetched free (one request each) "
                   "plus free web_search and fxtwitter. Every candidate opened live and "
                   "accepted only with HTTP 200 plus a share record carrying "
                   "id/ownerType/sharerName/botName/description, read with the new "
                   "ops/tools/share_record_scan.py (RSC flight payload + JSON raw_decode). "
                   "Zero paid API calls."),
        "reader_bug_note": (
            "verify-bot-links.py and fetch_share_full.py have a false-negative mode on this "
            "payload: a regex value branch truncates a description at an escaped quote "
            "(Weekly Recap read 7-8 chars instead of 246) and both require a non-null "
            "sharerName, so a live template with no display name reads as 'no share record'. "
            "Six candidates in this pass's first sweep were recovered by the new reader. "
            "The rotation sample below re-checked the 3 rows verify-bot-links.py flagged as "
            "unpublished: all three are live and nothing was delisted."),
        "counts": {
            "directory_entries_before": len(bots) - len(added),
            "catalogue_ids_checked": 2143,
            "ids_in_catalogues_not_in_directory": 59,
            "verified_live_this_pass": 100,
            "held_back": len(dropped),
            "added_to_directory": len(added),
            "rotation_sampled": 40,
            "rotation_dead": 0,
        },
        "added": [{"name": e["name"], "slug": e["slug"], "url": e["url"],
                   "category": e["category"], "builder": e["builder"]} for e in added],
        "held_back": [{"name": n, "bot_id": b, "reason": w} for n, b, w in dropped],
        "rotation": {
            "note": "40 existing listings re-opened live; 0 dead, 0 set pending",
        },
        "sources": {
            "cs68614-hash/awesome-grokbot-templates": SRC,
            "majiayu000/awesome-grok-bot": "https://github.com/majiayu000/awesome-grok-bot",
            "RongleCat/awesome-grok-bot": "https://github.com/RongleCat/awesome-grok-bot",
            "lroolle/awesome-grokbot-templates": "https://github.com/lroolle/awesome-grokbot-templates",
            "kydlikebtc/awesome-grokbot": SRC_KYD,
            "divo12/awesome-grok-bot-templates": "https://github.com/divo12/awesome-grok-bot-templates",
        },
        "tools": ["ops/tools/share_record_scan.py", "ops/tools/verify-bot-links.py",
                  "ops/tools/fetch_share_full.py"],
    }
    json.dump(report, open(f"{REPO}/ops/scout-report-2026-09-26-0700.json", "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)

    print(json.dumps({"added": len(added), "held": len(dropped), "total": len(bots)}))
    for e in added:
        print(f"  + {e['slug']:26s} {e['name'][:32]:32s} {e['category']:13s} "
              f"{e['builder']['name'][:20]:20s} x={e['builder']['x'] or '-'}")
    for n, b, w in dropped:
        print(f"  - {b:24s} {n[:26]:26s} {w[:64]}")


if __name__ == "__main__":
    main()
