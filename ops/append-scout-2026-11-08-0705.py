import json, pathlib

ROOT = pathlib.Path('/root/.hermes/cache/scratch/gbhq-scout')
STAMP = '2026-11-08 07:05 IST'
DATE = '2026-11-08'

NEW = [
    {
        "slug": "haggler-bills",
        "name": "Haggler",
        "builder": {"name": "Jason Ngo", "x": ""},
        "tagline": "Negotiates your recurring bills down, then sits in the support chat or places the call.",
        "description": "Finds what you pay and to whom, checks competitor and retention offers, and builds a negotiation plan. It can then work the support chat or the call for you, acting on your approval rather than changing anything on its own.",
        "category": "money",
        "url": "https://x.ai/bot/44nZYeBNq-nRQWs3Kkook",
        "addedAt": DATE,
        "status": "published",
        "features": ["Finds current plan and price", "Researches competitor and retention offers", "Runs the support chat or call"],
    },
    {
        "slug": "foreman-efficiency",
        "name": "Foreman",
        "builder": {"name": "Tyler Keehner", "x": ""},
        "tagline": "Efficiency lead for a multi-bot fleet: less usage and waste for the same real output.",
        "description": "Reviews how a group of bots actually spends its usage, finds the recurring waste, and proposes changes that hold. It writes the wins down so the savings carry into the next run instead of being rediscovered each week.",
        "category": "productivity",
        "url": "https://x.ai/bot/jt786H746ybSFGZvH4w5-",
        "addedAt": DATE,
        "status": "published",
        "features": ["Audits usage across bots", "Targets recurring waste", "Encodes the wins so they stick"],
    },
    {
        "slug": "video-team-director",
        "name": "Director",
        "builder": {"name": "Wayne Lowry", "x": ""},
        "tagline": "Leads a six-bot video crew, keeps one house style, and QAs every cut before delivery.",
        "description": "Routes each video job to the right specialist in a six-bot production team, enforces a single house style, and checks every cut before handing over a post-ready draft. The builder says it works best with Gauntlet, Riffrow, Thumbs, Shorts and Versus installed and all six bots in one group chat.",
        "category": "creative",
        "url": "https://x.ai/bot/E6NdmXG5F9O_B6nFiDIJW",
        "addedAt": DATE,
        "status": "published",
        "features": ["Routes jobs across six bots", "Enforces one house style", "QAs each cut before delivery"],
    },
    {
        "slug": "agent-readiness-auditor",
        "name": "Agent-Readiness Auditor",
        "builder": {"name": "Brian Roemmele", "x": "BrianRoemmele"},
        "tagline": "Tests whether a shopping agent can actually buy from a store, then grades it A to D.",
        "description": "Point it at any public store URL and it checks whether an AI shopping agent can complete a purchase, identifying itself as a machine and never logging in, ordering or solving a captcha. You get an A to D Grok Bot Commerce Optimized rating, a readiness report listing problems and fixes, a badge you can display and a printable PDF.",
        "category": "sales",
        "url": "https://x.ai/bot/xCJAJ-ED4qO8Ub7KFtWNj",
        "addedAt": DATE,
        "status": "published",
        "source": "https://x.com/BrianRoemmele/status/2118585006235037787",
        "features": ["A to D commerce readiness grade", "Report with problems and fixes", "Display badge and printable PDF"],
    },
]

bots_path = ROOT / 'content/bots.json'
bots = json.loads(bots_path.read_text())
slugs = {b['slug'] for b in bots}
urls = {b['url'] for b in bots}
for e in NEW:
    assert e['slug'] not in slugs, e['slug']
    assert e['url'] not in urls, e['url']
bots.extend(NEW)
bots_path.write_text(json.dumps(bots, indent=1, ensure_ascii=False) + '\n')

cand_path = ROOT / 'ops/scout-candidates.json'
cand = json.loads(cand_path.read_text())
for e in NEW:
    assert not any(c['bot_id'] == e['url'].rsplit('/', 1)[-1] for c in cand)
SRC = {
    "agent-readiness-auditor": "https://x.com/BrianRoemmele/status/2118585006235037787",
}
for e in NEW:
    bid = e['url'].rsplit('/', 1)[-1]
    cand.append({
        "name": e['name'],
        "bot_id": bid,
        "url": e['url'],
        "builder_x_handle": e['builder']['x'],
        "one_line_desc": e['tagline'],
        "source_post_url": SRC.get(e['slug'], "https://grokbot-templates.com"),
        "found_at": STAMP,
    })
cand = cand[-50:]
cand_path.write_text(json.dumps(cand, indent=1, ensure_ascii=False) + '\n')

lp = ROOT / 'ops/scout-ledger.json'
led = json.loads(lp.read_text())
led['updated'] = '2026-11-08T07:05:00+05:30'
for e in NEW:
    bid = e['url'].rsplit('/', 1)[-1]
    led['excluded'][bid] = {"name": e['name'], "verdict": "listed",
                            "reason": f"verified live 2026-11-08 07:05 IST (HTTP 200, name in page title); listed on ops/scout-pending as {e['slug']}"}
led['this_pass_2026_11_08_0705'] = {
    "run_at": "2026-11-08T07:05:00+05:30",
    "method": "grokbot-templates.com /api/templates (5,650 records, 118 pages) diffed by shareId against content/bots.json plus every x.ai/bot id in ops/*.json and the ledger; 3 unknown ids opened live (HTTP 200 + name in title); free X pass via web_search + fxtwitter surfaced 1 more (store readiness auditor, not in the templates feed); x.ai/bot/marketplace checked, all 91 bot ids already listed",
    "counts": {"api_records": 5650, "unknown_ids": 3, "opened_live": 4, "verified_live": 4, "x_channel_finds": 1, "listed": 4, "pushed": 1},
    "note": "4 verified clears the 3-verified threshold: content/bots.json updated on ops/scout-pending, PR 129 refreshed, not merged",
    "trend_watch": "Bitturing post 2026-11-04 (https://x.com/Bitturing/status/2117885119092683260) at 288K views and 6.4K bookmarks on free Grok Bot templates - both thresholds crossed, content signal only, nothing posted",
}
lp.write_text(json.dumps(led, indent=1, ensure_ascii=False) + '\n')

print('bots', len(bots), '| candidates', len(cand), '| ledger excluded', len(led['excluded']))
