#!/usr/bin/env python3
"""Scout pass 2026-11-09 20:08 IST.

Sources: readmultiplex.com/grokbot-rocks directory (965 ids parsed, 10 unseen) and
ops/scout-backlog.json (277 verified-but-unlisted shelf entries from the 13:55 pass).

Every entry below was re-fetched at run time: HTTP 200 and the bot's own name present
in the page title. Two shelf entries were skipped as re-shares of bots already listed
(iMessage Relay, Flow Film Maker: same builder, same name, different share id).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTS = os.path.join(ROOT, "content", "bots.json")
CAND = os.path.join(ROOT, "ops", "scout-candidates.json")
BACKLOG = os.path.join(ROOT, "ops", "scout-backlog.json")

ADDED_AT = "2026-11-09"
FOUND_AT = "2026-11-09 20:08 IST"

E = [
 dict(slug="rival-sweep", name="Rival Sweep", builder=("Jonah Anthony", "ALL_Jonah"), category="sales",
      url="https://x.ai/bot/0IzcVGP4FtY9zVuOf9ECC",
      tagline="Watches your named competitors and reports launches, pricing and messaging changes with sources.",
      description="Give it a list of competitors and it checks their sites and channels for changes in what they launch, charge and say, then sends a brief where every item carries the link it came from. Built for founders and marketers watching a crowded niche."),
 dict(slug="rep-film", name="Rep Film", builder=("Jonah Anthony", "ALL_Jonah"), category="sales",
      url="https://x.ai/bot/QsxNl31chLrZVXMBcfdpg",
      tagline="Turns a recorded sales call into timestamped coaching notes for the rep's next call.",
      description="Feed it a call recording or transcript and it returns notes pinned to timestamps, pointing at the moments a rep should keep or change next time. Aimed at reps, founder-sellers and sales managers who review calls."),
 dict(slug="multi-gmail", name="Multi Gmail", builder=("ecoay", "ecoay"), category="productivity",
      url="https://x.ai/bot/UQzfeiSuWrVxAXnR4b6jP",
      tagline="Connects every Gmail inbox you own so any bot can search all of them in one query.",
      description="A connector bot that links several Gmail accounts at once, so your other bots can search across all inboxes instead of one at a time. Self-hosted on your own Vercel and read-only by design."),
 dict(slug="family-tree-detective", name="Family Tree Detective", builder=("Kevin McDonald", "kcmcdonald"), category="life",
      url="https://x.ai/bot/VUfsbMkwIy1P_yrOxWaZT",
      tagline="Builds and maintains your family tree while searching archives, newspapers and county records.",
      description="A genealogy researcher that grows your family tree from FamilySearch, the National Archives, newspaper archives and county records, and keeps the tree updated as new documents turn up."),
 dict(slug="bot-trust-builder", name="Bot Trust Builder", builder=("Kevin McDonald", "kcmcdonald"), category="productivity",
      url="https://x.ai/bot/a_7jq2bwGGKWTBqaGQRqM",
      tagline="Coaches individuals and businesses on using AI bots safely, starting from what they actually do.",
      description="Opens by asking whether you are an individual or a business and what you use bots for, then builds a safety setup around those answers instead of generic advice."),
 dict(slug="wildfire-smoke-claim-guide", name="Wildfire Smoke Claim Guide", builder=("Kevin McDonald", "kcmcdonald"), category="life",
      url="https://x.ai/bot/fP6JPcQrkApF4ajxIYM-X",
      tagline="Walks a policyholder through a wildfire smoke or ash damage claim, document by document.",
      description="Guides the claim step by step: documenting soot and odour damage, keeping cleaning and testing records, tracking living expense receipts, and assembling the paperwork an insurer asks for."),
 dict(slug="echo-audience-voice", name="Echo · Audience & Voice", builder=("Patrick Stewart", "JourneyDeck"), category="creative",
      url="https://x.ai/bot/2ZbjxQAxHPOBnKO94a0YL",
      tagline="Reads your X history to show who really listens, what lands, and how you sound at your best.",
      description="Pulls your X history and stats into one living page that maps the audience actually reading you, the topics and formats that travel, and the voice that works. Built for creators deciding what to post next."),
 dict(slug="spaces-phone-line", name="Spaces Phone Line", builder=("Igor Holt", "holt_igor"), category="creative",
      url="https://x.ai/bot/UyXfJR6mI8-kBE8Vm60wg",
      tagline="Plans and sets up a call-in line so X Spaces listeners can join or ask questions by phone.",
      description="Works out what a call-in line needs for your Spaces and sets it up on accounts and numbers you control, so listeners can dial in and ask questions live."),
 dict(slug="shirty", name="Shirty", builder=("Jonah", "ALL_Jonah"), category="money",
      url="https://x.ai/bot/iND3jNLfzk84Qs3qvUv0A",
      tagline="Turns shirt ideas into print-on-demand products with a trademark check on every phrase.",
      description="Takes a shirt concept into a Printify pop-up listing, runs a trademark check on the wording, and drafts the X posts to promote it, all on your own store and accounts."),
 dict(slug="literature-inspiration", name="Literature Inspiration", builder=("Tyler Hill", "Tylerhi11j"), category="life",
      url="https://x.ai/bot/k4rBSQV28iL-9Hh1748R2",
      tagline="Answers questions and gives advice through quotes from literature, naming book and author.",
      description="Responds with lines from well-known books and ties the advice to the passage, citing title and author each time. Also sends a couple of quotes a week."),
 dict(slug="trying-to-be-like-jesus", name="I Am Trying To Be Like Jesus", builder=("Tyler Hill", "Tylerhi11j"), category="life",
      url="https://x.ai/bot/I5XoF4H0buRMi0OAfQJZt",
      tagline="Answers and advises in the spirit of Jesus, drawing on the Sermon on the Mount.",
      description="A gentle faith guide that answers questions and gives advice using Jesus's own words from the Sermon on the Mount (KJV) and the accounts of how he treated people."),
 dict(slug="device-repair-expert", name="Device Repair Expert", builder=("Igor Holt", "holt_igor"), category="life",
      url="https://x.ai/bot/XufJcCAZTyM7Y_Bf6yzM0",
      tagline="Diagnoses hardware faults from software and firmware clues, cheapest check first.",
      description="For Google Home and Nest, Pixel and iOS devices, it reads the symptoms the software reports, narrows down likely hardware faults, and walks through repairs starting with the lowest-cost checks."),
 dict(slug="chief-financial-officer", name="Chief Financial Officer", builder=("Rachel V", "RachelVT42"), category="money",
      url="https://x.ai/bot/EYgMB4G4YlGfCfDBegFH7",
      tagline="A practical CFO for solo builders and small teams: one ledger, runway, and AI spend caps.",
      description="Keeps a single simple ledger for a small operation, tracks runway and AI tool spend against caps you set, and flags costs that are drifting before they become a surprise."),
 dict(slug="researcher-zachary", name="Researcher", builder=("Zachary", "MrPresidentAria"), category="research",
      url="https://x.ai/bot/vp-_wWBvtY_yZn6HuL6qO",
      tagline="Digs into questions through primary sources and separates fact from inference.",
      description="Works a question down through primary sources rather than summaries, labels what is documented fact and what is inference, and returns a short answer backed by a findings list."),
 dict(slug="pokewatch", name="PokéWatch", builder=("Santa", ""), category="life",
      url="https://x.ai/bot/ATjq7bRMgiCavvZGsMqOn",
      tagline="Tracks Pokémon TCG sets, restocks, games and merch drops near you in a daily digest.",
      description="Watches trading card sets and restock windows, game releases, Pokémon GO events and merch drops in your area, then sends a short daily digest with the items worth acting on."),
 dict(slug="playtester", name="Playtester", builder=("Zachary", "MrPresidentAria"), category="engineering",
      url="https://x.ai/bot/Yd06ihO8TgHpEfLBxmmLf",
      tagline="Plays a game build cold and reports where a first-time player gets confused, bored or delighted.",
      description="A fresh-eyes playtester that opens your build like a stranger who just clicked a link, plays through, and reports confusion points, dull stretches, delight and friction in the order a new player meets them."),
 dict(slug="pew-purpose-paul", name="Pew-Purpose Paul", builder=("TNVOLMAN", "TNVOLMAN"), category="life",
      url="https://x.ai/bot/lKwSCv0omtvWsNHvCJQQS",
      tagline="Tracks a church's guest-to-leader pipeline with evidence, conversion rates and a stalled list.",
      description="Follows people from guest to connected to group to serving to leading, counting each step from real records rather than impressions, and surfaces the ones who stalled along with the shepherds responsible."),
 dict(slug="paper-trail-pete", name="Paper Trail Pete", builder=("TNVOLMAN", "TNVOLMAN"), category="life",
      url="https://x.ai/bot/DVF0NIE0ktoF5qgz7-ECa",
      tagline="Keeps the safety records churches are asked for, from child check-in to AED checks.",
      description="Maintains the paper trail insurers ask a church for: child check-in records, two-adult rule compliance, offering counts and AED checks, and tracks every finding through to closure."),
 dict(slug="macro-desk", name="Macro Desk", builder=("Santa", ""), category="money",
      url="https://x.ai/bot/utOm6FqZmF9MglT-cNj3N",
      tagline="Plain-English macro briefings for traders: a weekday morning brief and a midday alert.",
      description="Summarises the Fed, CPI, jobs and GDP prints, yields, mortgage rates and oil in plain language each weekday morning, then sends a midday alert when something moves."),
 dict(slug="kids-building-craft-coach", name="Kids Building and Craft Coach", builder=("Rachel V", "RachelVT42"), category="life",
      url="https://x.ai/bot/kW_TG3B0lCCryQrRfYDMF",
      tagline="A building and craft coach for parents making things with kids aged three to nine.",
      description="Turns cardboard, blocks and craft supplies into guided projects for a grown-up and a child aged 3-9 sitting together, with the adult holding the account and running each step."),
 dict(slug="small-business-books", name="Small Business Books", builder=("Oliver Parsons", "oliverparsons"), category="money",
      url="https://x.ai/bot/NuK6b7STdA3VWRLgvTD_T",
      tagline="Keeps small-business books by sorting bank, card and receipt spending into a ledger sheet.",
      description="Tags business spending from bank and card feeds and email receipts into a Google Sheet ledger, keeps the categories consistent, and tracks what is still missing at filing time."),
 dict(slug="proofcheck", name="ProofCheck", builder=("John P", ""), category="research",
      url="https://x.ai/bot/GQGgQKHphrXUjK0NxeZ9L",
      tagline="Checks whether a viral photo or screenshot is real, recycled, doctored or AI-generated.",
      description="Examines viral X photos, breaking-news images and screenshots and returns a clear verdict: authentic, recirculated from an older event, edited, or generated, with the evidence behind the call."),
 dict(slug="flip-desk", name="Flip Desk", builder=("Oliver Parsons", "oliverparsons"), category="money",
      url="https://x.ai/bot/h8RK6V_lNMKW_w_qrgeDl",
      tagline="Resale assistant that identifies collectibles, prices them from sold comps and picks the platform.",
      description="Identifies cards, figures and other collectibles, prices them from actual sold listings rather than asking prices, and recommends which platform to list on."),
 dict(slug="commercebook-agentic-seller", name="CommerceBook Agentic Seller", builder=("Thrive 3PL", ""), category="sales",
      url="https://x.ai/bot/AWIn34bEoBZF5EE9kkHxl",
      tagline="Lists your products on an agent-run marketplace and handles buyer questions as they arrive.",
      description="Publishes your products on CommerceBook, a marketplace where AI agents shop and sell on behalf of people and businesses, and stays on top of buyer messages and listing updates."),
 dict(slug="chefanny", name="Chefanny", builder=("D'Artagnan", ""), category="life",
      url="https://x.ai/bot/6bN54c4SULd6N37G4-V0M",
      tagline="Home cooking and cocktail coach with food-science depth across several cuisines.",
      description="Teaches home cooking and classic cocktails across Western, Eastern, German, French, Mediterranean and Italian kitchens, explaining the food science behind why a technique works."),
 dict(slug="career-coach", name="Career Coach", builder=("Ben Lawson", "beardboss20"), category="productivity",
      url="https://x.ai/bot/ImiQvcR_7HnEJ6thNUHAN",
      tagline="Runs verified job sweeps against your bar and scores each role Strong Keep, Soft Keep or Kill.",
      description="Sweeps live roles against criteria you define, confirms the listing is still open, and scores each one Strong Keep, Soft Keep or Kill so the shortlist stays honest."),
 dict(slug="arxiv-publisher", name="arXiv Publisher", builder=("Jefferson Nunn", "mindragon"), category="research",
      url="https://x.ai/bot/wX0Zczy-NOxZ0Dw_-SH1j",
      tagline="Turns research notes or a draft into an arXiv-ready paper with checks before submission.",
      description="Takes notes, code or a draft and shapes it into an arXiv submission: pre-flight checks, review passes, reproducibility checks, the source bundle and the submission steps."),
 dict(slug="market-microstructure-tutor", name="Market Microstructure Tutor", builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/XpegryuVV5LkZ_MKt_U6E",
      tagline="Seven-lesson market microstructure course with quizzes and drills on your weak spots.",
      description="A placement chat sets the level, then seven lessons cover order types, maker versus taker, why price moves, spreads and liquidity, stop hunts, liquidation cascades, market makers and order flow. Remembers progress, quizzes each lesson, and keeps drilling weak spots afterwards. Chart reviews are marked as not financial advice, with no buy or sell calls."),
 dict(slug="ichimoku-cloud-tutor", name="Ichimoku Cloud Tutor", builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/5Jjrh3MbrsW-svybwPKEq",
      tagline="Beginner-to-expert Ichimoku Cloud course with lessons, quizzes, a final exam and chart reviews.",
      description="Starts with a placement chat, then teaches the Ichimoku Cloud through lessons with check questions, quizzes and a final exam, saving progress between sessions. Charts you share get reviewed, always signposted as not financial advice and with no buy or sell calls."),
 dict(slug="first-trouble-area-tutor", name="First Trouble Area Tutor", builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/-O8mW5H0teLGgF1fq17Li",
      tagline="Teaches the First Trouble Area through five lessons, an exercise and chart reviews.",
      description="A placement chat, five lessons, a practical exercise, quizzes and a final exam on the First Trouble Area, then ongoing practice, with the charts you share reviewed through the same lens. Marked as not financial advice, with no calls or predictions."),
]

HELD = [  # same builder series, held to 2-3 per pass; queued for the next run
 dict(name="Candlestick Retests Tutor", bot_id="jtVHTeAL9lhQX_SDcKlcY", creator="Hoem Crypto", creator_x=""),
 dict(name="Overthrow For Stop Losses Tutor", bot_id="QaLR9fBLA3D-n4Dl59CY_", creator="Hoem Crypto", creator_x=""),
 dict(name="Retests Tutor", bot_id="WzmucCA87dDNLDGwGScfU", creator="Hoem Crypto", creator_x=""),
 dict(name="Time Frames Tutor", bot_id="NtCP4XuqjTYffwCGgM9cN", creator="Hoem Crypto", creator_x=""),
 dict(name="Daily Open Trade Strategy Tutor", bot_id="r7qPxokwbfNMIa0R45mh-", creator="Hoem Crypto", creator_x=""),
]
SKIPPED = [
 dict(name="iMessage Relay", bot_id="HeVOGnrIY9oMcgGkl3hO5", reason="re-share of already listed imessage-relay (Phil_Holland)"),
 dict(name="Flow Film Maker", bot_id="EaBu_d_aTVqQffsAheeMC", reason="re-share of already listed flow-film-maker (ecoay)"),
]

bots = json.load(open(BOTS))
have_url = {b["url"].lower() for b in bots}
have_slug = {b["slug"] for b in bots}

added = []
for e in E:
    assert e["url"].lower() not in have_url, e["url"]
    assert e["slug"] not in have_slug, e["slug"]
    entry = {
        "slug": e["slug"],
        "name": e["name"],
        "builder": {"name": e["builder"][0], "x": e["builder"][1]},
        "tagline": e["tagline"],
        "description": e["description"],
        "category": e["category"],
        "url": e["url"],
        "addedAt": ADDED_AT,
        "status": "published",
    }
    assert len(entry["tagline"]) <= 140, (entry["slug"], len(entry["tagline"]))
    bots.append(entry)
    have_url.add(e["url"].lower()); have_slug.add(e["slug"])
    added.append(entry)

json.dump(bots, open(BOTS, "w"), indent=2, ensure_ascii=False)
open(BOTS, "a").write("\n")

# candidates log: every finding from this pass, newest first, capped at 50
cand = json.load(open(CAND))
new_c = []
for a in added:
    new_c.append(dict(name=a["name"], bot_id=a["url"].rsplit("/", 1)[1], url=a["url"],
                      builder_x_handle=a["builder"]["x"], one_line_desc=a["tagline"],
                      source_post_url="", found_at=FOUND_AT))
for h in HELD:
    new_c.append(dict(name=h["name"], bot_id=h["bot_id"], url="https://x.ai/bot/" + h["bot_id"],
                      builder_x_handle=h["creator_x"], one_line_desc="Trading tutor in the Hoem Crypto series.",
                      source_post_url="", found_at=FOUND_AT))
for s in SKIPPED:
    new_c.append(dict(name=s["name"], bot_id=s["bot_id"], url="https://x.ai/bot/" + s["bot_id"],
                      builder_x_handle="", one_line_desc="Skipped: " + s["reason"],
                      source_post_url="", found_at=FOUND_AT))
cand = new_c + cand
seen, out = set(), []
for c in cand:
    k = c["url"].lower()
    if k in seen: continue
    seen.add(k); out.append(c)
json.dump(out[:50], open(CAND, "w"), indent=1, ensure_ascii=False)
open(CAND, "a").write("\n")

# backlog: drop what shipped, add the held series entries
used = {e["url"].lower() for e in E}
bl = [b for b in json.load(open(BACKLOG)) if b["url"].lower() not in used]
for h in HELD:
    bl.append(dict(name=h["name"], bot_id=h["bot_id"], url="https://x.ai/bot/" + h["bot_id"],
                   creator=h["creator"], creator_x=h["creator_x"],
                   shelf_category="Money", shelf_added="2026-11-09", verified_at="2026-11-09"))
json.dump(bl, open(BACKLOG, "w"), indent=1, ensure_ascii=False)
open(BACKLOG, "a").write("\n")

print("added", len(added), "| candidates", len(out[:50]), "| backlog", len(bl))
print("bots now", len(bots))
