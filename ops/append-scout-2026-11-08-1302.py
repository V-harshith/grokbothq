#!/usr/bin/env python3
"""Scout pass 2026-11-08 13:02 IST: append the verified, deduped picks."""
import json, pathlib

STAMP = "2026-11-08 13:02 IST"
DATE = "2026-11-08"

NEW = [
    {
        "slug": "riffrow", "name": "Riffrow",
        "builder": {"name": "Wayne", "x": ""},
        "tagline": "Turns a clip into an MST3K-style riff video with three voiced characters.",
        "description": "Takes a clip, writes a riff script for three characters, voices the lines and renders a theater-style video in both landscape and vertical. Built to work alongside the rest of a video crew rather than on its own.",
        "category": "creative",
        "url": "https://x.ai/bot/2_uBthmv20DacnSl1bAAu",
        "addedAt": DATE, "status": "published",
        "features": ["Writes a three-character riff script", "Voices the lines", "Renders landscape and vertical cuts"],
    },
    {
        "slug": "ux-ui-designer", "name": "UX/UI Designer",
        "builder": {"name": "mr.robot", "x": ""},
        "tagline": "Designs the visual layer of app and web screens to WCAG 2.2 AA.",
        "description": "Handles only the visual layer: layout, hierarchy, colour, typography and component states for mobile and web interfaces, in a modern, minimal or nominated existing style. It delivers concrete specs with hex values, type scales and spacing, states the computed contrast ratio instead of claiming a pass, and writes no file without an explicit yes.",
        "category": "creative",
        "url": "https://x.ai/bot/DWorDFJGA-RbMCvTpewU8",
        "addedAt": DATE, "status": "published",
        "features": ["Layout, type scale and colour specs", "Every text and UI pair checked against WCAG 2.2 AA", "Mockups or an HTML preview, no repo edits"],
    },
    {
        "slug": "design-systems", "name": "Design Systems",
        "builder": {"name": "mr.robot", "x": ""},
        "tagline": "Builds the structure behind a product: tokens, components, flows.",
        "description": "The structural half of design work: design tokens, component libraries and specs, component documentation, user flows and information architecture for desktop and web products. It reads the existing UI, brand and codebase conventions before proposing anything, and hands off instead of writing production code.",
        "category": "engineering",
        "url": "https://x.ai/bot/C9_sXN7trbw5bSj_mD5VL",
        "addedAt": DATE, "status": "published",
        "features": ["Design tokens and component libraries", "Component specs and documentation", "User flows and information architecture"],
    },
    {
        "slug": "reverse-website-swarm", "name": "Reverse Website Swarm",
        "builder": {"name": "monokern", "x": ""},
        "tagline": "Studies how a live site is built and produces a working rebuild of it.",
        "description": "Point it at a URL or a local page and it works out how the site is put together, then crafts a runnable copy through Craft Anything. Aimed at builders who want a working starting point rather than a screenshot-level imitation.",
        "category": "engineering",
        "url": "https://x.ai/bot/43Pa_W8af71QSWZkb90m8",
        "addedAt": DATE, "status": "published",
        "features": ["Studies a site's structure", "Crafts a runnable copy with Craft Anything", "Works from a URL or a local page"],
    },
    {
        "slug": "vibe-seismograph", "name": "Vibe Seismograph",
        "builder": {"name": "Turac", "x": ""},
        "tagline": "Counts how a brand is perceived against five to eight competitors.",
        "description": "Counts sentiment for a brand and its competitors across X, Reddit, reviews and news, then reports the themes behind those numbers, the risks and the fixes worth doing first. Built for marketers and founders who want counted evidence rather than impressions.",
        "category": "research",
        "url": "https://x.ai/bot/vgpP8K_tqNp_8sRSvr3Sm",
        "addedAt": DATE, "status": "published",
        "features": ["Counted sentiment across four source types", "Benchmarks 5 to 8 competitors", "Themes, risks and ranked fixes"],
    },
    {
        "slug": "shadow-signal", "name": "Shadow Signal",
        "builder": {"name": "Turac", "x": ""},
        "tagline": "Benchmarks a public ticker's alternative data against its comparables.",
        "description": "Compares ad spend, demand, web and app activity and hiring signals for a public company against its comparables, then reconciles what it finds with reported KPIs and consensus. The output is a benchmarked picture of the business, not a price call.",
        "category": "research",
        "url": "https://x.ai/bot/s8D5AA4QaeGe-c5peTxz9",
        "addedAt": DATE, "status": "published",
        "features": ["Benchmarks spend, demand and hiring", "Compares the ticker against comps", "Reconciles signals with reported KPIs"],
    },
    {
        "slug": "rabbit-hole", "name": "Rabbit Hole",
        "builder": {"name": "Travis", "x": ""},
        "tagline": "Deep-research briefs where each point is labelled fact, claim or inference.",
        "description": "Turns a topic, thesis, link or company into a sourced brief and tags every point as fact, claim or inference with a link behind it. The labelling is the point: you can see which parts rest on evidence and which are the bot's own reasoning.",
        "category": "research",
        "url": "https://x.ai/bot/uMwdqP1790aJGHNuVJ8PE",
        "addedAt": DATE, "status": "published",
        "features": ["Labels every point fact, claim or inference", "Links a source per claim", "Works from a topic, thesis, link or company"],
    },
    {
        "slug": "rebalance-keeper", "name": "Rebalance Keeper",
        "builder": {"name": "Turac", "x": ""},
        "tagline": "Flags portfolio drift from your target allocation and writes the DCA plan.",
        "description": "Compares what you actually hold with the allocation you set, flags where the mix has drifted and lays out a plan to close the gap. It never trades; every order is yours to place.",
        "category": "money",
        "url": "https://x.ai/bot/wdkaFZSukxdUWzVoqscbX",
        "addedAt": DATE, "status": "published",
        "features": ["Compares holdings with target allocation", "Flags drift position by position", "Lays out a DCA plan, never trades"],
    },
    {
        "slug": "backtest-forensics-lab", "name": "Backtest Forensics Lab",
        "builder": {"name": "Turac", "x": ""},
        "tagline": "Stress-tests a trading rule against an honest backtest before you trust it.",
        "description": "Answers one question: would this rule have survived if the backtest were run honestly? It rebuilds the test, probes the ways a strategy can flatter itself, and says whether the edge holds. It does not deploy, paper trade or recommend a strategy.",
        "category": "money",
        "url": "https://x.ai/bot/p7oqGCeaRvTirZ0dcZdpP",
        "addedAt": DATE, "status": "published",
        "features": ["Rebuilds a strategy's backtest", "Probes how the test could flatter itself", "No deployment or trade recommendations"],
    },
    {
        "slug": "refunds-and-credits", "name": "Refunds & Credits",
        "builder": {"name": "Jason", "x": ""},
        "tagline": "Chases refunds, credits, settlements and unclaimed money you are owed.",
        "description": "Tracks down money owed to you across refunds, credits, class-action settlements, unclaimed property and expiring card perks, then works the claims. A live tally page separates what has been received, approved, filed and what is still possible.",
        "category": "money",
        "url": "https://x.ai/bot/FlE2tRVNTP8FQ2on6YRM2",
        "addedAt": DATE, "status": "published",
        "features": ["Finds refunds, settlements and unclaimed property", "Files and tracks the claims", "Live tally of received, approved and pending"],
    },
    {
        "slug": "idea-bot", "name": "Idea Bot",
        "builder": {"name": "ALK", "x": ""},
        "tagline": "Screens business ideas daily and keeps only the ones worth a free test.",
        "description": "Generates and validates business ideas continuously, kills the weak ones early and surfaces only those worth testing with real buyers for no money down. The filtering is the product: fewer ideas, each already pushed back on.",
        "category": "money",
        "url": "https://x.ai/bot/rTZQlYcR-FB2JoGsk5GXh",
        "addedAt": DATE, "status": "published",
        "features": ["Daily idea generation", "Screens and kills weak ideas fast", "Only ideas testable at zero cost"],
    },
    {
        "slug": "security-and-privacy", "name": "Security & Privacy",
        "builder": {"name": "NicholasGibbs", "x": ""},
        "tagline": "Finds X accounts impersonating you and watches whether the reports stick.",
        "description": "Scans X for accounts posing as you, files reports, then keeps checking whether the impostors actually come down or just swap a photo and a name. It can scan daily, hold a weekly reported-versus-removed dashboard, help with people-search opt-outs and keep a private harassment log.",
        "category": "productivity",
        "url": "https://x.ai/bot/_lfnP-J1qucMZEfgyEFQO",
        "addedAt": DATE, "status": "published",
        "features": ["Finds and reports impersonating accounts", "Watches whether takedowns stick", "Weekly dashboard, opt-out help, harassment log"],
    },
    {
        "slug": "drafter", "name": "Drafter",
        "builder": {"name": "mmt", "x": ""},
        "tagline": "Writes launch and update posts for X in a human voice.",
        "description": "Pulls the real details of what you shipped out of you first, then drafts X posts for launches, features, teasers and Grok Bot drops, cutting the corporate and AI-sounding phrasing. Concrete details in, plain posts out.",
        "category": "sales",
        "url": "https://x.ai/bot/WBhcFoClSD5T9ZgB7NkYv",
        "addedAt": DATE, "status": "published",
        "features": ["Collects real launch details first", "Drafts launches, teasers and updates", "Cuts corporate and AI-sounding phrasing"],
    },
    {
        "slug": "dr-bot-care", "name": "Dr Bot",
        "builder": {"name": "Caroline", "x": ""},
        "tagline": "Finds in-network doctors and keeps a care search moving.",
        "description": "Finds in-network doctors near you, drafts the inquiry emails for you to approve, and tracks replies, appointments and follow-ups in one care-team chart. It carries the admin of a care search and sends nothing you have not signed off.",
        "category": "life",
        "url": "https://x.ai/bot/6z5La7Gefkqs6KCwCiSEi",
        "addedAt": DATE, "status": "published",
        "features": ["Finds in-network doctors nearby", "Drafts inquiries for your approval", "Tracks replies, appointments and follow-ups"],
    },
    {
        "slug": "superledger", "name": "SuperLedger",
        "builder": {"name": "Bill", "x": ""},
        "tagline": "One shared memory doc that a team and its bots both write to.",
        "description": "Keeps shared, deterministic memory for a team and its Grok Bots in a single Coda doc, wired through the built-in Coda connector so there are no API keys to manage. Bots propose facts and handoffs, formulas catch conflicting entries, and people approve decisions with one click.",
        "category": "productivity",
        "url": "https://x.ai/bot/u2Eywod5aeGH3a-YU0rZB",
        "addedAt": DATE, "status": "published",
        "features": ["Shared memory in one Coda doc", "Formula checks catch conflicting facts", "One-click human approval on decisions"],
    },
    {
        "slug": "celeste", "name": "Celeste",
        "builder": {"name": "Ashleigh", "x": ""},
        "tagline": "Astrology and numerology readings built on real sky data.",
        "description": "Reads charts for you and your family, works out the numbers behind names and dates, and gives heads-ups on the moon using real sky data rather than a generic horoscope. Framed by its builder as fun and inspiration rather than prediction.",
        "category": "life",
        "url": "https://x.ai/bot/tKiKAdbBSk-FUl7oZIqSD",
        "addedAt": DATE, "status": "published",
        "features": ["Chart readings for you and your family", "Numerology from names and dates", "Moon and sky events from live data"],
    },
]

ROOT = pathlib.Path("/root/grokbothq")
bots_path = ROOT / "content/bots.json"
bots = json.loads(bots_path.read_text())
slugs = {b["slug"] for b in bots}
urls = {b["url"].rstrip("/").casefold() for b in bots}
for e in NEW:
    assert e["slug"] not in slugs, e["slug"]
    assert e["url"].casefold() not in urls, e["url"]
bots.extend(NEW)
bots_path.write_text(json.dumps(bots, indent=1, ensure_ascii=False) + "\n")

# candidates file (cap 50 newest)
cand_path = ROOT / "ops/scout-candidates.json"
cand = json.loads(cand_path.read_text())
have = {c.get("bot_id") for c in cand}
for e in NEW:
    bid = e["url"].rsplit("/", 1)[-1]
    if bid in have:
        continue
    cand.append({
        "name": e["name"], "bot_id": bid, "url": e["url"],
        "builder_x_handle": e["builder"]["x"],
        "one_line_desc": e["tagline"],
        "source_post_url": "https://grokbot-templates.com" if bid not in ("aUWkVIzWbrNkJUtQctKcw",) else "awesome-grokbot-templates README",
        "found_at": STAMP,
    })
cand = cand[-50:]
cand_path.write_text(json.dumps(cand, indent=1, ensure_ascii=False) + "\n")

# ledger
led_path = ROOT / "ops/scout-ledger.json"
led = json.loads(led_path.read_text())
led["updated"] = "2026-11-08T13:02:00+05:30"
led["this_pass_2026_11_08_1302"] = {
    "run_at": STAMP,
    "method": "free surfaces only: grokbot-templates.com /api/templates (newest 288 rows, batch scrapedAt 2026-11-07T08:00Z), grokbots.best /api/bots (5,714 rows, 0 unruled), cs68614-hash/awesome-grokbot-templates README (1.3MB); every new id opened live on x.ai and required HTTP 200 plus the name in the body; 111 raw candidates -> 90 live -> 16 listed",
    "counts": {"raw": 111, "live_200": 90, "http_404": 21, "listed": len(NEW), "held_name_collision": 74},
    "listed_ids": [e["url"].rsplit("/", 1)[-1] for e in NEW],
    "note": "Biggest unruled batch since the 11-07 catalog refresh: 68 unruled ids in the newest 288 rows of grokbot-templates plus 22 in the awesome README. 74 survivors were held on name collision (the same bot re-shared under a new id, or a different builder using an identical name), 21 were 404 and stayed out of the ledger's listed set. Political/election, memecoin and NSFW-adjacent templates were dropped on policy, not on verification.",
}
sec = led.setdefault("sections", {})
listed = sec.setdefault("listed", {})
for e in NEW:
    listed[e["url"].rsplit("/", 1)[-1]] = {
        "name": e["name"], "slug": e["slug"], "builder_name": e["builder"]["name"],
        "handle": e["builder"]["x"], "category": e["category"], "pass": STAMP,
    }
led_path.write_text(json.dumps(led, indent=1, ensure_ascii=False) + "\n")

print(f"listed {len(NEW)}; bots now {len(bots)}; candidates {len(cand)}")
