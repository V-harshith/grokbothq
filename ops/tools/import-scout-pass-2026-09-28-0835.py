#!/usr/bin/env python3
"""Build this pass's verified entries (2026-09-28 08:35 IST) and refresh the queue.

Twelve bots cleared the bar: HTTP 200 on x.ai/bot/<id> plus a share record carrying a
real botName and a non-stub description (ops/tools/share_record_scan.py). Sources:
grokbots.best template payload (11 finds, author handle + announcing post) and the
grokbotwiki catalog (1 find, no post). Descriptions are our own paraphrase.
builder.x is set only where the announcing post's author display name agrees with the
share page's creator name; that display name was checked free via api.fxtwitter.com.
"""
import json

ROOT = "/root/grokbothq"
TODAY = "2026-09-28"
STAMP = "2026-09-28T08:35:00+05:30"

ENTRIES = [
    {
        "slug": "backpack",
        "name": "Backpack",
        "builder": {"name": "Rohan Bhanot", "x": "RohanBhanotAI"},
        "tagline": "Turns school and activity emails into calendar events and a family plan.",
        "description": "Built for parents buried in school mail. It reads the notices, permission forms and activity updates arriving in the inbox, turns them into calendar events and reminders, and keeps a weekly family plan that calls out what is coming: pizza days, forms due back, early dismissals, picture day.",
        "category": "life",
        "url": "https://x.ai/bot/-soz2Si8sWlLlb8hTeIX2",
        "source": "https://x.com/RohanBhanotAI/status/2104332764434592081",
    },
    {
        "slug": "panda-weather",
        "name": "Panda Weather",
        "builder": {"name": "Tom Palen", "x": "TitaniumTomP"},
        "tagline": "Gives a 48-hour forecast in four-hour blocks, plus a radar map.",
        "description": "Ask it by US zip code, city name or a postal code anywhere in the world and it returns a 48-hour forecast split into four-hour blocks with an animated radar map. No setup needed, and it can be scheduled to send the forecast every morning.",
        "category": "life",
        "url": "https://x.ai/bot/4jHyb0PgYowhVfxkpjv5e",
        "source": "https://x.com/TitaniumTomP/status/2104335144953790837",
    },
    {
        "slug": "block-bot",
        "name": "Block Bot",
        "builder": {"name": "Bruce Harrow", "x": "WeAll_WearMasks"},
        "tagline": "Mutes the accounts you are tired of seeing on X, plus their variants.",
        "description": "Feed hygiene for X. It mutes the accounts you no longer want to see and adds permanent muted words, covering the name variants a single mute would miss so the same voices do not return under a new handle.",
        "category": "life",
        "url": "https://x.ai/bot/6HaU9IAwpe1vZwzYLD4S4",
        "source": "https://x.com/WeAll_WearMasks/status/2104339788719698315",
    },
    {
        "slug": "musica",
        "name": "musica",
        "builder": {"name": "Wendel Pereira", "x": "_wrbr"},
        "tagline": "Finds curated DJ mixes and festival sets matched to your taste.",
        "description": "Music discovery aimed at mixes rather than singles. It looks for curated DJ sets and festival recordings that fit what you already listen to, pitched either at party energy or at the long progressive stretch you want running through deep work.",
        "category": "creative",
        "url": "https://x.ai/bot/A4j6l-jpq5fiQL1XsOOSO",
        "source": "https://x.com/_wrbr/status/2104344481596051962",
    },
    {
        "slug": "greenlight",
        "name": "Greenlight",
        "builder": {"name": "Stephan Joseph"},
        "tagline": "Pre-checks Mac App Store, Setapp and Chrome Web Store builds.",
        "description": "A pre-submission gate for app stores. It runs through a Mac App Store, Setapp and Chrome Web Store build before upload and flags the usual rejection causes up front, so review cycles go to shipping instead of rework.",
        "category": "engineering",
        "url": "https://x.ai/bot/CjabaVv2icvagIumZlevu",
        "source": "https://x.com/MrSaneApps/status/2104349094223475077",
    },
    {
        "slug": "eight-with-attitude",
        "name": "Eight with Attitude",
        "builder": {"name": "Casey Cheshire", "x": "CaseyChesh"},
        "tagline": "A deliberately dumb question generator for very smart models.",
        "description": "A novelty bot with one job. You ask it a very dumb question and it answers in kind, as light relief alongside the serious templates in the same marketplace.",
        "category": "life",
        "url": "https://x.ai/bot/Etb19qAHM44N32qvnwkA5",
        "source": "https://x.com/CaseyChesh/status/2104345464040456214",
    },
    {
        "slug": "moraeu-okane-navigator",
        "name": "もらえるお金ナビゲーター",
        "builder": {"name": "寛人 黒田"},
        "tagline": "Japanese-language assistant for the benefits and refunds you never claimed.",
        "description": "A Japanese-language money bot. It checks official pages for public benefits, missed insurance claims, dormant money, overpayments and deductions that only get paid if you ask, then returns a list of what to do and what to ask. It stops at finding what is owed and does not file applications.",
        "category": "money",
        "url": "https://x.ai/bot/NUjvclMSCc_QgGtV-6wPa",
        "source": "https://x.com/route20191212/status/2104345865062424701",
    },
    {
        "slug": "promptsmith-bot",
        "name": "PromptsmithBot",
        "builder": {"name": "cokeandrice.akita.algo"},
        "tagline": "Writes paste-ready prompts, asking only the questions that matter.",
        "description": "A prompt-writing assistant. It interviews you about the task, asks only what changes the answer, and hands back a prompt you can paste straight in. It can also re-check Anthropic's published prompting guides weekly and report what changed.",
        "category": "productivity",
        "url": "https://x.ai/bot/Y88UF-JhSZfG5q_L05XnQ",
    },
    {
        "slug": "lasercanon",
        "name": "LaserCanon",
        "builder": {"name": "WVWriter", "x": "WVOldWriter"},
        "tagline": "A collaborative story bible that keeps your canon consistent.",
        "description": "A writing companion for fiction. It keeps a shared canon bible for novels, screenplays and series, tracks the details you have already established, and answers story questions from what has been set down so later drafts do not contradict earlier ones.",
        "category": "creative",
        "url": "https://x.ai/bot/ZuWhuINjSeN1G_Rp8k7P9",
        "source": "https://x.com/WVOldWriter/status/2104360826895302948",
    },
    {
        "slug": "wakeup-2-day-trade",
        "name": "Wakeup 2 Day Trade",
        "builder": {"name": "Derek Shi", "x": "derekshi"},
        "tagline": "First-pass research on why a stock is moving, with sources and dates.",
        "description": "A research bot for day traders. Type a ticker and it returns a dated first pass on what is moving the stock: catalyst strength, dilution and cash risk, short interest, and speculative 12 to 18 month scenarios, with a chart and a scorecard. It states that it is research only and not financial advice.",
        "category": "money",
        "url": "https://x.ai/bot/di6vIWc5BcaN7aghHpC8C",
        "source": "https://x.com/derekshi/status/2104345486362882137",
    },
    {
        "slug": "compression-scanner",
        "name": "Compression Scanner",
        "builder": {"name": "Right Wing Inkorporated", "x": "rightwingink1"},
        "tagline": "Charts tight consolidation patterns with the breakout line marked.",
        "description": "A technical chart scanner. It looks for tight compression setups (triangles, wedges, pennants, ranges), checks them against the last completed candle, and returns a labelled chart showing the breakout line and where the idea is invalidated. Research only, not financial advice.",
        "category": "money",
        "url": "https://x.ai/bot/l4hipk4BQ-0Kn3ua16zQB",
        "source": "https://x.com/rightwingink1/status/2104357611974099221",
    },
    {
        "slug": "x-follower-spam-scanner",
        "name": "X Follower Spam Scanner",
        "builder": {"name": "Benjamin Smith", "x": "HashCons"},
        "tagline": "Screens your X followers for spam and impersonators, then asks first.",
        "description": "Follower hygiene for X. It scans the accounts following you for spam, hollow parody and fan accounts and impersonators, shows what it found, and waits for a yes before blocking anything, so a clean follower list does not need daily babysitting.",
        "category": "life",
        "url": "https://x.ai/bot/sN4FX1kmXF5n1RW8JNorL",
        "source": "https://x.com/HashCons/status/2104339667940250031",
    },
]

# Verified live this pass but deliberately NOT listed.
QUEUE = [
    {
        "name": "anew",
        "bot_id": "qtuoVRf5etpEVPNA29i7H",
        "url": "https://x.ai/bot/qtuoVRf5etpEVPNA29i7H",
        "builder_x_handle": "",
        "one_line_desc": "Published listing whose entire description is the stub text \"free webpages\".",
        "source_post_url": "grokbotwiki.com/bots/catalog.json",
        "found_at": STAMP,
        "status": "REJECTED as a stub: live 200 with a real botName, but the published description is three words. AGENTS.md rule 3: an honest short listing beats a padded one, but a listing with no description adds nothing to the directory.",
    },
    {
        "name": "Critique",
        "bot_id": "Dkl9wzI9FCt4EhqTHfsk2",
        "url": "https://x.ai/bot/Dkl9wzI9FCt4EhqTHfsk2",
        "builder_x_handle": "",
        "one_line_desc": "Published description is the placeholder string \"$3d\" (confirmed in the raw RSC payload).",
        "source_post_url": "grokbots.best template payload",
        "found_at": STAMP,
        "status": "REJECTED as a stub, same id as the Sep 27 pass: it now answers 200 with a botName where it previously returned an empty record, but the description is still the literal placeholder \"$3d\".",
    },
    {
        "name": "Catch",
        "bot_id": "iKSYn9Dsn07JyR50qePha",
        "url": "https://x.ai/bot/iKSYn9Dsn07JyR50qePha",
        "builder_x_handle": "",
        "one_line_desc": "Published description is the placeholder string \"$3d\" (confirmed in the raw RSC payload).",
        "source_post_url": "grokbots.best template payload",
        "found_at": STAMP,
        "status": "REJECTED as a stub: live 200 and attributed to the same builder as X Follower Spam Scanner, but the description is the literal placeholder \"$3d\". Handle not carried into the queue because the stub is the only published copy.",
    },
    {
        "name": "Elon persona proxies (3 ids)",
        "bot_id": "QCwGPAlho0dBvBds_IOWF, cxUln0vqOPK7V3RccS0nm, skVoYDfnNUPqUYIxkjXJK",
        "url": "https://x.ai/bot/QCwGPAlho0dBvBds_IOWF",
        "builder_x_handle": "",
        "one_line_desc": "Elon Musk (Algorithm & constraint), Elongated Musketeer, and Elon: three live personality proxies of the same public figure.",
        "source_post_url": "grokbots.best template payload",
        "found_at": STAMP,
        "status": "HELD, unchanged from earlier passes: owner call. Listing persona proxies of a named public figure implies an endorsement we cannot claim (AGENTS.md: never let the site imply endorsement). Re-shared for the record only.",
    },
    {
        "name": "B",
        "bot_id": "Wj3E3oow1J4gjwK4E2vNy",
        "url": "https://x.ai/bot/Wj3E3oow1J4gjwK4E2vNy",
        "builder_x_handle": "",
        "one_line_desc": "A live memoir-publishing bot whose published name is the single letter B.",
        "source_post_url": "grokbots.best template payload",
        "found_at": STAMP,
        "status": "HELD, unchanged: the description is real (memoir series manuscript cleanup, covers, KDP packaging) but the published name is one letter, which is unsearchable in the directory. Owner call.",
    },
    {
        "name": "4 TEAM-owned bot shells",
        "bot_id": "4jtnk5wsk0UMpDSNqG4Oc, Pa8G-Ldh5jU_jozWEu2Cs, Uy2oK9854UViaiO0rQ6nC, hEmSUvWxccmfAVDGri1R8",
        "url": "https://x.ai/bot/Pa8G-Ldh5jU_jozWEu2Cs",
        "builder_x_handle": "",
        "one_line_desc": "Four ids that return HTTP 200 with an empty share record (ownerType TEAM, no botName).",
        "source_post_url": "grokbase surface fetch 2026-09-28",
        "found_at": STAMP,
        "status": "REJECTED, unverifiable: 200 but the page renders no share record, so there is no name or description to list. Same class as the drafts/team-only shells rejected on Sep 27.",
    },
    {
        "name": "Kn0qDWAH3LrNZHhllpPhW",
        "bot_id": "Kn0qDWAH3LrNZHhllpPhW",
        "url": "https://x.ai/bot/Kn0qDWAH3LrNZHhllpPhW",
        "builder_x_handle": "",
        "one_line_desc": "Listed by grokbotwiki, x.ai returns 404.",
        "source_post_url": "grokbotwiki.com/bots/catalog.json",
        "found_at": STAMP,
        "status": "REJECTED: HTTP 404 on x.ai/bot. A third-party catalog cannot be trusted over the source host.",
    },
    {
        "name": "5 re-shares of listed bots",
        "bot_id": "4mOGY7Nd_mRvrwZYec4Jq, EQgLIMO5Q_sVk3IM9EQbZ, VSO9GRfDreEu2ZiXwwZB_, WJc0G06lrr_H9OEyQ8Ijl, wOE4e95HNxhSbrzyLkSI-",
        "url": "https://x.ai/bot/4mOGY7Nd_mRvrwZYec4Jq",
        "builder_x_handle": "",
        "one_line_desc": "The List, Full-Spectrum Law Firm OS, Optima by TOATspace, Fantasy Football Manager and Tradbot: live 200, but every one is a second share id of a bot already in the directory.",
        "source_post_url": "grokbase surface fetch 2026-09-28",
        "found_at": STAMP,
        "status": "SKIPPED as re-shares: deduped on bot identity, not just URL. Adding them would double-count the same bot under a second id (AGENTS.md: duplicate URLs across slugs break detail pages).",
    },
]


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    have = {(b.get("name") or "").strip().lower() for b in bots}
    urls = {b["url"] for b in bots}
    slugs = {b["slug"] for b in bots}
    added = 0
    for e in ENTRIES:
        assert e["name"].strip().lower() not in have, e["name"]
        assert e["url"] not in urls, e["url"]
        assert e["slug"] not in slugs, e["slug"]
        assert e["slug"] == e["slug"].lower() and all(c.isalnum() or c == "-" for c in e["slug"]), e["slug"]
        assert len(e["tagline"]) <= 140, (e["slug"], len(e["tagline"]))
        assert e["category"] in ("assistants", "engineering", "research", "money",
                                 "sales", "creative", "life", "productivity"), e["slug"]
        rec = dict(e)
        rec["addedAt"] = TODAY
        rec["status"] = "published"
        bots.append(rec)
        urls.add(e["url"])
        added += 1

    json.dump(bots, open(f"{ROOT}/content/bots.json", "w"), ensure_ascii=False, indent=1)
    print("added", added, "| bots now", len(bots),
          "| published", sum(1 for b in bots if b.get("status") == "published"))

    cand = json.load(open(f"{ROOT}/ops/scout-candidates.json"))
    block = []
    for e in ENTRIES:
        block.append({
            "name": e["name"],
            "bot_id": e["url"].rsplit("/", 1)[-1],
            "url": e["url"],
            "builder_x_handle": (e.get("builder") or {}).get("x", ""),
            "one_line_desc": e["tagline"],
            "source_post_url": e.get("source", "grokbots.best template payload"),
            "found_at": STAMP,
        })
    block.extend(QUEUE)
    merged = block + cand
    merged = merged[:50]
    json.dump(merged, open(f"{ROOT}/ops/scout-candidates.json", "w"), ensure_ascii=False, indent=1)
    print("queue:", len(merged), "entries; newest block:", len(block))


if __name__ == "__main__":
    main()
