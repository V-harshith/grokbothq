#!/usr/bin/env python3
"""Scout pass 2026-09-25 06:10 IST (cron 359022f62495): append the verified
templates found via the awesome-grokbot-templates catalog + grokbots.best.

Every candidate was opened live (ops/tools/fetch_share_full.py): HTTP 200 with a
real share record (botName + description). No paid API calls.

Rules applied (see PR body for the exclusions table):
  - dedupe on x.ai/bot id AND slug against content/bots.json
  - drop rows whose live description is a placeholder (<40 chars) or missing
  - drop non-ASCII names (queued, needs a translation pass)
  - drop personas of real named individuals, and templates named after the
    product itself ("Grok Bot")
  - builder x handle only when the platform's own record shows the handle
    exactly as the creator's display name; otherwise name only
  - hold the ~40 templates whose platform display name is the org name
    "SpaceX" for an owner call (attribution is not verifiable from the page)

Deterministic + idempotent: re-running never double-adds.
"""
import json
import re
from datetime import datetime, timezone, timedelta

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/scout"
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime.now(IST)
TODAY = NOW.strftime("%Y-%m-%d")
STAMP = NOW.strftime("%Y-%m-%dT%H:%M:%S+05:30")
AWESOME = "https://github.com/cs68614-hash/awesome-grokbot-templates"
GBEST = "https://grokbots.best/"

# --- explicit exclusions -------------------------------------------------------------
EXCLUDE = {
    "QCwGPAlho0dBvBds_IOWF": "persona of a real named individual (same rule that kept "
                             "earlier Elon/Steve Jobs templates out)",
    "MT6acytP70wHR526vPvM3": "third-party template named exactly \"Grok Bot\" — would read "
                             "as an xAI/SpaceXAI template",
    "qtuoVRf5etpEVPNA29i7H": "creator's description is \"free webpages\" — nothing factual "
                             "to list",
    "XGIep-r89FqSquTEKtd1f": "self-described Grok persona clone — implies it is the "
                             "platform's own assistant",
    "j1-ISFFzWDSzihs9xz2MA": "row carries a \"(test)\" marker in the catalog",
    "pRajEKa4qSHU5-o72V3e3": "live description is a 3-char placeholder",
    "_qeZe0Y7621Wr8y6d7KBU": "live description is a 3-char placeholder; catalog text is a "
                             "prompt fragment, not a description",
    "Nmv2fCQEcQc3EHzVXJZKN": "live description is a 3-char placeholder and the catalog "
                             "entry is truncated mid-sentence",
    "xFWEqzh1pZnYL6DiZwYYN": "live description is a 3-char placeholder; catalog text is a "
                             "prompt dump",
    "Wj3E3oow1J4gjwK4E2vNy": "the template's own name is the single letter \"B\" — nothing a "
                             "directory can list it as",
}
HOLD_SPACE = "platform display name is the org name \"SpaceX\" — attribution not verifiable"

# Live templates whose catalog name would not survive the name-freshness filter:
# the directory already lists a different bot with the same name, so they enter
# under a numeric slug (same convention as the existing chief-of-staff-2..45).
EXTRA_IDS = {
    "s8cUaz0aoomvjsIyOKANn": "Adam (Ed Tan), chief-of-staff bot — directory already lists an "
                             "unrelated 'Adam' (NRC filings), so this lands as adam-2",
}

# Category is a judgement call; these override the keyword classifier.
CATEGORY_OVERRIDE = {
    "everyone": "productivity", "newt": "life", "wirey": "research", "zenith": "assistants",
    "shop-bot": "life", "legal-advisor": "research", "fleet-qc": "productivity",
    "pit-crew": "productivity", "resource-allocation": "productivity", "vibe-check": "productivity",
    "cite-desk": "research", "texas-lawyer": "research", "x-master": "creative",
    "handel": "creative", "independent-author-hub": "productivity",
    "open-call-producer": "creative", "plan-precheck-bot": "productivity",
    "number-one": "productivity", "mediadeconstructor": "creative",
}

VALID_CATS = {"assistants", "engineering", "research", "money", "sales",
              "creative", "life", "productivity"}


def categorize(name: str, desc: str) -> str:
    text = f"{name} {desc}".lower()
    if re.search(r"\b(code|dev|build|repo|github|deploy|script|automat|api|infra|bug|test)", text):
        return "engineering"
    if re.search(r"\b(sales|lead|crm|pipeline|outbound|quota|prospect|deal)", text):
        return "sales"
    if re.search(r"\b(money|invoice|expense|budget|price|invest|trading|tax|payroll|revenue|book)", text):
        return "money"
    if re.search(r"\b(research|paper|news|monitor|watch|track|brief|intel|analyst)", text):
        return "research"
    if re.search(r"\b(design|art|image|video|music|write|writing|content|social|post|brand|creative)", text):
        return "creative"
    if re.search(r"\b(email|inbox|calendar|meeting|notes|task|slack|notion|workflow|ops|assistant|schedul)", text):
        return "productivity"
    if re.search(r"\b(meal|recipe|fitness|travel|habit|health|family|home|pet|garden|surf|sleep)", text):
        return "life"
    return "assistants"


def slugify(name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "bot"
    return base


def tagline(desc: str, limit: int = 140) -> str:
    desc = " ".join(desc.split())
    if len(desc) <= limit:
        return desc
    cut = desc[:limit]
    return cut[:cut.rfind(" ")].rstrip(" ,;:—–-") + "…"


def main():
    bots = json.load(open(f"{REPO}/content/bots.json"))
    have_ids = {b["url"].rsplit("/", 1)[-1] for b in bots}
    have_slugs = {b["slug"] for b in bots}

    screen = json.load(open(f"{SCRATCH}/screen.json"))
    full = {json.loads(l)["bot_id"]: json.loads(l) for l in open(f"{SCRATCH}/full_records.jsonl")}
    meta = {json.loads(l)["bot_id"]: json.loads(l) for l in open(f"{SCRATCH}/meta_seq.jsonl")}
    awe = {r["bot_id"]: r for r in json.load(open(f"{SCRATCH}/awesome_parsed.json"))["all"]}
    gbest = json.load(open(f"{SCRATCH}/diff.json"))["union"]

    added, dropped, queued = [], [], []
    cands = list(screen["keep"])
    for bid, why in EXTRA_IDS.items():
        fr = full.get(bid, {})
        cands.append({"bot_id": bid, "name": (fr.get("name") or "").strip(),
                      "sharer": (fr.get("sharer") or "").strip(), "handle": "",
                      "desc": (fr.get("desc") or "").strip(), "forced": True,
                      "note": why})
    for cand in cands:
        bid = cand["bot_id"]
        name = (cand["name"] or "").strip()
        fr, mt, aw = full.get(bid, {}), meta.get(bid, {}), awe.get(bid, {})
        # description: the page's own payload text, falling back to the longer og: meta text
        d1 = (fr.get("desc") or "").strip()
        d2 = (mt.get("desc") or "").strip()
        desc = d1 if len(d1) >= len(d2) else d2
        desc = " ".join(desc.split())
        sharer = (fr.get("sharer") or mt.get("sharer") or "").strip()
        handle = (aw.get("handle") or "").strip()

        if bid in EXCLUDE:
            dropped.append((name, bid, EXCLUDE[bid]))
            continue
        if sharer.lower() == "spacex":
            dropped.append((name, bid, HOLD_SPACE))
            continue
        if bid in have_ids:
            dropped.append((name, bid, "already listed under another name (same x.ai/bot id)"))
            continue
        if len(desc) < 40:
            dropped.append((name, bid, f"live description is a placeholder ({len(desc)} chars)"))
            continue
        if not name or any(ord(c) > 127 for c in name):
            dropped.append((name, bid, "non-ASCII name — needs a dedicated translation pass"))
            continue
        if name.endswith("…"):
            alt = (aw.get("name") or "").strip()
            if alt and not any(ord(c) > 127 for c in alt):
                name = alt

        slug = slugify(name)
        n = 2
        while slug in have_slugs:
            slug = f"{slugify(name)}-{n}"
            n += 1
        have_slugs.add(slug)
        have_ids.add(bid)

        cat = CATEGORY_OVERRIDE.get(slug, categorize(name, desc))
        assert cat in VALID_CATS, cat
        # grokbots.best pairs the creator with their own post — prefer that source
        g = gbest.get(bid, {})
        if g.get("source_url"):
            source = g["source_url"]
        else:
            source = AWESOME
        builder_x = handle if handle and handle.lower() == sharer.lower() else ""
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": sharer or handle or "", "x": builder_x},
            "tagline": tagline(desc),
            "description": desc if desc.endswith(".") else desc + ".",
            "category": cat,
            "url": f"https://x.ai/bot/{bid}",
            "addedAt": TODAY,
            "status": "published",
            "source": source,
        }
        assert len(entry["tagline"]) <= 140
        assert entry["builder"]["name"] or entry["builder"]["x"], bid
        bots.append(entry)
        added.append(entry)

    json.dump(bots, open(f"{REPO}/content/bots.json", "w"), indent=2, ensure_ascii=False)
    open(f"{REPO}/content/bots.json", "a").write("\n")

    # ---- candidate queue (50 newest) -------------------------------------------------
    queue = [{"name": e["name"], "bot_id": e["url"].rsplit("/", 1)[-1], "url": e["url"],
              "builder_x_handle": e["builder"]["x"], "one_line_desc": e["tagline"],
              "source_post_url": e["source"], "found_at": STAMP,
              "status": "added to directory in ops/scout-pending"} for e in added]
    # verified-live rows held back this pass, so the next pass starts where this one stopped
    for name, bid, why in dropped:
        queue.append({"name": name, "bot_id": bid, "url": f"https://x.ai/bot/{bid}",
                      "builder_x_handle": "", "one_line_desc": why,
                      "source_post_url": AWESOME, "found_at": STAMP,
                      "status": "verified live, not listed" if "placeholder" not in why else "not added"})
    old = json.load(open(f"{REPO}/ops/scout-candidates.json"))
    seen = {q["bot_id"] for q in queue}
    queue += [o for o in old if o.get("bot_id") not in seen]
    json.dump(queue[:50], open(f"{REPO}/ops/scout-candidates.json", "w"), indent=2, ensure_ascii=False)

    report = {
        "run": "2026-09-25 06:10 IST scout pass (cron 359022f62495)",
        "branch": "ops/scout-pending",
        "method": ("Live fetch of every candidate x.ai/bot link (HTTP 200 + share record with "
                   "botName and description). Zero paid API calls: web_search + api.fxtwitter.com "
                   "+ curl only."),
        "counts": {"candidates_screened": len(screen["keep"]), "live_templates": len(full),
                   "added_to_directory": len(added), "held_or_dropped": len(dropped)},
        "added": [{"name": e["name"], "slug": e["slug"], "url": e["url"],
                   "category": e["category"], "builder": e["builder"]} for e in added],
        "held_back": [{"name": n, "bot_id": b, "reason": w} for n, b, w in dropped],
        "sources": {"awesome_catalog": AWESOME, "grokbots_best": GBEST,
                    "verifier": "ops/tools/fetch_share_full.py"},
    }
    json.dump(report, open(f"{REPO}/ops/scout-report-2026-09-25-0610.json", "w"),
              ensure_ascii=False, indent=1)
    print(json.dumps({"added": len(added), "dropped": len(dropped), "total": len(bots)}, indent=1))
    for e in added:
        print(f"  + {e['slug']:34s} {e['name'][:32]:34s} {e['category']:13s} {e['builder']['name'][:18]:18s} x={e['builder']['x'] or '-'}")


if __name__ == "__main__":
    main()
