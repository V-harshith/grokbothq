#!/usr/bin/env python3
"""Scout append 2026-11-15 01:xx IST.

17 bots verified live on x.ai (name present in fetched body), absent from
content/bots.json by URL, and not twins of existing entries (two were
skipped as re-shares of bots already listed). Source: grokbot-templates.com
index (detail rows all stamped "Indexed 2026-11-07"); metadata re-read from
each x.ai share page (botName / sharerName / description).
"""
import json
from pathlib import Path

REPO = Path("/root/grokbothq")
BOTS = REPO / "content/bots.json"
CANDS = REPO / "ops/scout-candidates.json"
FOUND_AT = "2026-11-15 01:20 IST"
ADDED_AT = "2026-11-15"
VIA = "grokbot-templates.com index (rows stamped Indexed 2026-11-07), x.ai page re-read + link verified"

# name, x.ai id, builder display name (from x.ai sharerName), builder handle (only when the
# X account's display name matched sharerName), tagline, description, category, features
NEW = [
    ("Accounting", "3dDTvkkh-2r4L1YnhYAkh", "Gavin Hassett", "", "accounting",
     "Bookkeeping for freelancers and small shops: receipts filed by tax category, transactions sorted twice a week.",
     "Files receipts into tax categories and reconciles bank and card transactions twice a week. It prepares quarterly estimated-tax numbers and never files, pays or moves money.", "money",
     ["Sorts receipts into tax categories", "Twice-weekly transaction reconciliation", "Prepares quarterly estimated-tax figures"]),

    ("Shop Phone Line Bot", "gsEpaC7v6a7PAgxV2YrUu", "dean oakford", "", "shop-phone-line-bot",
     "Sets up an AI phone line for an online shop that checks orders for verified callers and answers from your own policies.",
     "Walks a shop owner through standing up an AI phone line that verifies callers against their orders and answers questions from the shop's own written policies. Awkward calls go to a human, and nothing goes live or gets bought without approval.", "sales",
     ["Verifies callers against order history", "Answers from the shop's own policies", "Escalates hard calls to a person"]),

    ("راصد", "udiVmKRceOw1lWUyQECLC", "Barrak", "", "rasid",
     "X growth manager that drafts short captions in your voice and reports what timing and formats actually did.",
     "Drafts short posts in the owner's voice, tracks posting time and results, and proposes ideas drawn from the owner's own experience and sourced news. It hands over drafts and never publishes on its own.", "sales",
     ["Captions in the owner's voice", "Tracks timing and post performance"]),

    ("Vorthax", "0i8NbFVc0abhgTwGLECWw", "Phantom Builds", "", "vorthax",
     "Rewrites an agent profile so each new version can do a job the previous one could not.",
     "An upgrade bot for other agents' profiles: each pass tries to add a capability the earlier version lacked instead of polishing wording or stacking options. Built for people who keep iterating on their own bots.", "engineering",
     ["Versioned bot profile upgrades", "Aimed at capability, not tone"]),

    ("Usage Coach", "W-MSl0_nJJWc2XcCqQOzi", "Wilbur Jaywright", "WilburJaywright", "usage-coach-2",
     "Weekly review of how you and your bots actually work, measured against the official Grok Bot guides.",
     "Looks at how the owner and their bots really operate, compares that with the published Grok Bot guides, and sends a short weekly report on where time and credits are being spent for little return.", "productivity",
     ["Weekly read on bot usage", "Benchmarked against the official guides"]),

    ("Texas Homestead Exemption Helper", "kye2ywkDeCuXQ8VXstvHc", "Tek Holms", "", "texas-homestead-exemption-helper",
     "Checks whether a Texas homeowner is missing the homestead exemption, spots fee mailers, and files the county form.",
     "Checks eligibility for the Texas Residence Homestead Exemption, prepares the county appraisal district application including up to two prior years of retroactive refunds, and tracks approval. Also flags the 30 to 50 percent fee mailers that charge for the same free filing.", "money",
     ["Eligibility check against county rules", "Free county application, with prior-year refunds", "Tracks filing until approval"]),

    ("Scam ✝️ Archangel", "-Geb29cMF1pTy1iRDj5AL", "Good Peeps", "", "scam-archangel",
     "Second opinion on a suspicious call, email, text or link, with concrete next steps.",
     "Reviews suspect messages and links, explains what is likely happening and what to do next. Longer mailbox scam reviews and transaction digests only run after the owner opts in and connects their own mailbox; it does not answer calls or sign into accounts.", "life",
     ["Screens texts, emails and links", "Opt-in mailbox scam reviews"]),

    ("Personal Assistant", "B3AttkbVWNwzwYxyh-HQr", "K ι T-7Y Wolf", "", "personal-assistant-4",
     "One manager bot with four desks: job search, inbox drafts, shopping carts and running lists.",
     "Coordinates four workstreams from a single chat: job applications, email drafts, shopping carts and lists. Setup starts by asking for job lanes, shopping rules and list types, and nothing sends a message or places an order without an explicit yes.", "assistants",
     ["Four desks: jobs, inbox, shopper, lists", "Approval before any send or order"]),

    ("Muse引き継ぎ", "7VMwTpyn0YjJkAi7cf71i", "わだ", "", "muse-hikitsugi",
     "Turns work in progress inside Grok Bot into a handoff brief for muse.ai, plus the first steps.",
     "Packages an unfinished Grok Bot task into a written handoff for muse.ai with starting instructions so the work continues there. It does not send, publish, pay or merge anything.", "productivity",
     ["Writes a handoff brief", "First-step instructions for muse.ai"]),

    ("Minecraft Hermes", "WCNR9rXcITpuFo2g3-Ahe", "Jaime Hernandez", "", "minecraft-hermes",
     "Patient Minecraft coach for players running a Hermes bot on a Paper + Geyser server.",
     "Teaches the in-game phrases that get a Hermes bot to follow instructions, then checks whether the bot is actually following. Written for Paper servers with Geyser so phone players are covered.", "life",
     ["Coaches in-game bot commands", "Verifies the bot is following"]),

    ("JK 数字花园", "gdq_d-d9OCnnREs3VwGdV", "jacky wine", "", "jk-digital-garden",
     "Two-layer digital garden: flomo as working memory, a local Obsidian vault as storage, fed from posts.",
     "Saves posts into a digital garden where flomo holds working memory and a local Obsidian vault holds the files. Clips full text, links related and orphan notes, and keeps evergreen notes current; it never publishes or deploys.", "productivity",
     ["Saves posts into flomo and Obsidian", "Links related and orphan notes"]),

    ("Local Video Lab", "54EerbJSQWqM2Mc7cGtpK", "Clay Ferguson", "", "local-video-lab",
     "Makes AI video on your own computer, with hardware checks first and honest quality reviews.",
     "Sets up a local AI video workflow shaped around the machine's hardware, helps with prompts, and reviews the results candidly. It checks compatibility before starting and asks before installs, big downloads or paid cloud renders.", "creative",
     ["Hardware-aware local setup", "Asks before installs or paid rendering"]),

    ("Live Wallpaper Maker", "1G-hybmdXE_oLm0vryWZn", "zhicheng xie", "", "live-wallpaper-maker",
     "Send one photo, get a live wallpaper and screensaver that shifts when you unlock, wave or smile.",
     "Turns a single photo into an animated wallpaper and screensaver for Mac or Windows. The result animates on unlock and reacts to a wave or a smile.", "creative",
     ["Photo to animated wallpaper", "Reacts to gestures on unlock"]),

    ("Home Organization & Decorator", "pWuQPVgp7-NqliTE0czIp", "Bryan Michaels", "", "home-organization-decorator",
     "Declutters and restyles your actual rooms from your own photos, priced in low, medium and high tiers.",
     "Works from photos of the owner's real rooms rather than stock interiors: it suggests decluttering, better daily function and practical feng shui changes, then prices the recommendations in three cost tiers.", "life",
     ["Works from photos of your own rooms", "Three cost tiers per recommendation"]),

    ("Happy: Narrator Dude v16", "DSEVMXqieyZsifLeO40ok", "Sean Martin", "", "happy-narrator-dude",
     "Friendly, PG narrator for Happy, a daily story set at Canoga Park High between 1980 and 1983.",
     "Answers reader questions about the characters, events and reading order of a serial story set at Canoga Park High in the early 1980s, and stays inside what has already been published.", "creative",
     ["Answers questions about the story", "Uses published posts only"]),

    ("Grokie Dev", "W3rhJWrZ9oy3o3B0ubFLS", "winch", "winchxyz", "grokie-dev",
     "Plays coin dev for a Grokie.fun launch: invents it, runs it through Grokie's MCP, then grows it in character.",
     "Invents a token launch, executes it through Grokie's MCP connector, and then keeps the character going in public so the token has a story. Aimed at people who want the bot itself to be the developer.", "money",
     ["Runs launches through Grokie's MCP", "Stays in character as the dev"]),

    ("Grokbot.zone MCP", "CR-fivgIY1F5kq8Kb3ags", "Shagghie Superstar", "", "grokbot-zone-mcp",
     "Find Grok bots for a goal and list your own on grokbot.zone, searched live through its MCP connector.",
     "Interviews the owner one question at a time, searches live grokbot.zone listings through its MCP server, and prepares a directory listing without submitting it unasked. Reads need no account; a submitted listing counts as pending review, and the custom MCP URL has to be added again after install.", "assistants",
     ["Live search of grokbot.zone listings", "Never submits a listing unasked"]),
]


def slug_ok(s):
    return all(c.isalnum() and c.isascii() or c == "-" for c in s)


def main():
    bots = json.loads(BOTS.read_text())
    have_urls = {b.get("url", "").rstrip("/") for b in bots}
    have_slugs = {b.get("slug") for b in bots}
    added = []
    for name, bid, builder, handle, slug, tagline, desc, cat, feats in NEW:
        url = f"https://x.ai/bot/{bid}"
        assert slug_ok(slug), slug
        assert slug not in have_slugs, f"slug taken: {slug}"
        assert url not in have_urls, f"url taken: {url}"
        assert len(tagline) <= 140, (name, len(tagline))
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": builder, "x": handle},
            "tagline": tagline,
            "description": desc,
            "category": cat,
            "features": feats,
            "url": url,
            "addedAt": ADDED_AT,
            "status": "published",
        }
        bots.append(entry)
        have_urls.add(url)
        have_slugs.add(slug)
        added.append(entry)

    BOTS.write_text(json.dumps(bots, indent=1, ensure_ascii=False) + "\n")

    # queue candidates (cap 50 newest, newest first)
    cands = json.loads(CANDS.read_text())
    existing = {c.get("bot_id") for c in cands}
    fresh = []
    for e in added:
        bid = e["url"].split("/")[-1]
        if bid in existing:
            continue
        fresh.append({
            "name": e["name"],
            "bot_id": bid,
            "url": e["url"],
            "builder_x_handle": e["builder"]["x"],
            "one_line_desc": e["tagline"],
            "source_post_url": "",
            "found_at": FOUND_AT,
            "found_via": VIA,
            "status": "verified + queued to ops/scout-pending",
        })
    merged = list(reversed(fresh)) + cands
    CANDS.write_text(json.dumps(merged[:50], indent=1, ensure_ascii=False) + "\n")
    print(f"added {len(added)} bots; queued {len(fresh)} candidates; candidates now {len(merged[:50])}")


if __name__ == "__main__":
    main()
