#!/usr/bin/env python3
"""This pass's housekeeping: fix the rotation findings, refresh candidates + reports."""
import json, collections

REPO = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"
STAMP = "2026-09-27-2010"

bots = json.load(open(REPO + "/content/bots.json"))
if isinstance(bots, dict):
    bots = bots["bots"]

fixes = []
for b in bots:
    if b["slug"] == "grok-bot-2" and b.get("status") == "published":
        b["status"] = "pending"
        fixes.append(("grok-bot-2", "status -> pending (team-only share: 200 but no public botName)"))
    if b["slug"] == "printerbot-by-federico-nPwfPZq-" and b["name"] != "printerbot":
        fixes.append((b["slug"], f"name '{b['name']}' -> 'printerbot' (live share-page name)"))
        b["name"] = "printerbot"
json.dump(bots, open(REPO + "/content/bots.json", "w"), ensure_ascii=False, indent=2)
print("fixes:", fixes)

# --- candidates bookkeeping (cap 50 newest) ---
cands = json.load(open(REPO + "/ops/scout-candidates.json"))
added = json.load(open(SCRATCH + "added_this_pass.json"))
existing = {c.get("bot_id") for c in cands}
fresh = [{
    "name": e["name"], "bot_id": e["url"].rsplit("/", 1)[-1], "url": e["url"],
    "builder_x_handle": e["builder"]["x"], "one_line_desc": e["tagline"],
    "source_post_url": e.get("source"), "found_at": "2026-09-27T20:10:00+05:30",
    "status": "listed",
} for e in added if e["url"].rsplit("/", 1)[-1] not in existing]
cands = fresh + cands
cands = cands[:50]
json.dump(cands, open(REPO + "/ops/scout-candidates.json", "w"), ensure_ascii=False, indent=1)
print("candidates:", len(cands), "| new this pass:", len(fresh))

# --- rejects / holds ---
rejects = {
    "run": f"2026-09-27 20:10 IST scout pass (cron 359022f62495)",
    "rejected": [
        {"id": "hEmSUvWxccmfAVDGri1R8", "why": "200 but empty botName (blank/unpublished template shell)"},
        {"id": "Uy2oK9854UViaiO0rQ6nC", "why": "200 but empty botName (blank/unpublished template shell)"},
        {"id": "4jtnk5wsk0UMpDSNqG4Oc", "why": "200 but empty botName (blank/unpublished template shell)"},
        {"id": "Pa8G-Ldh5jU_jozWEu2Cs", "why": "200 but empty botName (blank/unpublished template shell)"},
        {"id": "WJc0G06lrr_H9OEyQ8Ijl", "why": "Fantasy Football Manager: re-share of a bot already listed (other share id)"},
        {"id": "EQgLIMO5Q_sVk3IM9EQbZ", "why": "Full-Spectrum Law Firm OS: re-share/case-variant of an already listed share id"},
        {"id": "wOE4e95HNxhSbrzyLkSI-", "why": "Tradbot: re-share of a bot already listed"},
        {"id": "qtuoVRf5etpEVPNA29i7H", "why": "'anew': creator name 'round', one-line description 'free webpages' - no real listing"},
    ],
    "held": [
        {"ids": "57 share ids published under the creator display name 'SpaceX' (e.g. Account Health s5465ebb9e192551741f7, Account Manager sd4333bc337078a9752ac, Chief of Staff sc0a0ec3ce9c675824106, SEO / AEO Auditor sb6d579c33f7a32d0e7af, ...)",
         "why": "All 57 verified live with a real botName and description, but every one credits the creator as 'SpaceX'. Listing them would put 'by SpaceX' on the site and imply xAI endorsement, which AGENTS.md forbids. Third-party catalogs attribute the pack to a personal X handle that the x.ai page itself does not carry, so the handle rule also blocks attribution. Owner call needed: list them under a neutral creator label, or leave them out."},
        {"ids": "skVoYDfnNUPqUYIxkjXJK (Elon), QCwGPAlho0dBvBds_IOWF (Elon Musk (Algorithm & constraint)), cxUln0vqOPK7V3RccS0nm (Elongated Musketeer)",
         "why": "Personality proxies named after a public figure (Elon Musk). Verified live, but naming them on the site is a trademark/impersonation question rather than a listing task."},
        {"id": "Wj3E3oow1J4gjwK4E2vNy", "why": "Published name is a single letter 'B' (off-grid memoir publishing partner). Live and real, but the name carries no information for a directory."},
    ],
}
json.dump(rejects, open(REPO + f"/ops/scout-rejects-{STAMP}.json", "w"), ensure_ascii=False, indent=1)

rot = json.load(open(REPO + f"/ops/tools/.rotation-2026092720.json"))
report = {
    "run": "2026-09-27 20:10 IST scout pass (cron 359022f62495)",
    "branch": "ops/scout-pending",
    "push": True,
    "push_reason": "17 verified new bots (>= 3 gate met)",
    "method": ("Live fetch of every candidate x.ai/bot link with ops/tools/share_record_scan.py "
               "(HTTP 200 + share record carrying botName and a real description). Zero paid API calls: "
               "web_search + api.fxtwitter.com + urllib/curl only."),
    "counts": {"candidates_screened": 18, "live_and_verifiable": 18, "added_to_directory": 17,
               "duplicates_found": 1, "held": 4, "rejected": 8,
               "directory_after": len(bots), "published_after": sum(1 for b in bots if b.get("status") == "published")},
    "sources": {
        "grokbot.dev registry feed": "1,317 items (was 1,292 at 05:08Z). 18 items added since the last pass, all templates, all carrying a share id; 17 new, 1 already listed (Lineage Desk).",
        "grokbots.best": "1,037 records; the payload carries no x.ai share ids this time (only source X posts), so nothing additional came from it.",
        "grokbots.page": "200 records via /api/bots; 1 id not matched by bare URL, and it turned out to be a slug-suffixed duplicate of an already listed Chief of Staff.",
        "grokbotwiki.com/bots/catalog.json": "NEW SURFACE - 2,153 machine-readable rows with share ids, creators and first-seen dates. 2,084 of its ids were already in the directory (good overlap check); of the 69 unseen, 57 are the 'SpaceX'-credited pack, 4 are blank shells, and the rest are re-shares - see the rejects file.",
        "grokbot-templates.com": "DOWN this pass - /api/templates returns an empty list (was 48 static items) and the site root returns HTTP 500.",
        "x.ai/bot/marketplace": "31 Add links via web_extract; 7 not matched by id, and all 7 are already listed under other share ids (Researchy, tinkabot, Clip Bot, figma bro, Credit Card Max, Home robots, last30days).",
        "x.ai/news": "newest article is still Grok Bot for Customer Support (Sep 22); nothing to add to news.json.",
        "web_search + fxtwitter": "every search channel returned posts from Aug 29 - Sep 8; all x.ai/bot ids in them were already listed.",
    },
    "rotation": {"sampled": rot["sampled"], "live": rot["live"], "dead": 1, "renamed": 1,
                 "seed": rot["seed"], "tool": "ops/tools/rotation-2026-09-27-2010.py",
                 "findings": fixes},
    "marketing_signals": [],
    "marketing_note": "No post cleared the bar this pass (the Finance-integration signal from the 14:00 pass is unchanged and was already filed; no new >100K-view or >1K-bookmark grok-bot post surfaced in the free channels).",
    "tools": ["ops/tools/import-scout-pass-2026-09-27-2010.py", "ops/tools/rotation-2026-09-27-2010.py"],
}
json.dump(report, open(REPO + f"/ops/scout-report-{STAMP}.json", "w"), ensure_ascii=False, indent=1)
print("report written; dir", len(bots), "published", report["counts"]["published_after"])
