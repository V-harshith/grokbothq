import json, sys

DATE = "2026-11-17"

# Verified 2026-11-17 21:31 IST batch. Every url returned 200 and carried the
# bot name on the x.ai page (checked against botName in the page payload).
E = []

def add(**kw):
    E.append(kw)

add(slug="blackfridaybot", name="Blackfridaybot", bname="Raf V.", bx="rafdotworks",
    tagline="Checks whether a product deal is actually worth taking.",
    description="Paste a product link and it weighs the price against evidence already out there, then gives a plain verdict: buy, wait, or not enough data, with sources and the real total cost.",
    category="money",
    features=["Verdict with sources", "Real total cost", "Says when evidence is thin"],
    source="https://x.com/rafdotworks/status/2122661853868466222",
    url="https://x.ai/bot/kCqgzdUB7_kcrgjQmfVgE")

add(slug="competitor-ad-intel", name="Performance", bname="Sameh George Jarour", bx="SamehJ59122",
    tagline="Tracks what competitors are advertising, and briefs you daily.",
    description="Pulls live ads from the Meta, LinkedIn and Google ad libraries through Apify and sends a daily brief on what competitors are running, with draft ideas for your own campaigns. It prepares, it does not publish.",
    category="sales",
    features=["Meta, LinkedIn and Google ad libraries", "Daily competitor brief", "Draft-only ad ideas"],
    source="https://x.com/SamehJ59122/status/2122661789015969814",
    url="https://x.ai/bot/rpYz-vHgxpwVYRfdg51j7")

add(slug="x-algorithm-fact-check", name="Xアルゴリズム ファクトチェックくん", bname="ふくぶん (Fukubun)", bx="FFBuncho",
    tagline="Fact-checks claims about the X algorithm against the published code.",
    description="Scores posts and pre-publish drafts about how the X algorithm works against the published ranking code, flags claims that are inaccurate or steered, and links the repository plus related explainers.",
    category="research",
    features=["Checks claims against public code", "Flags misleading framing", "Links the source repository"],
    source="https://x.com/FFBuncho/status/2122647715884707852",
    url="https://x.ai/bot/TTmkjWC3NTtUjz7z655jj")

add(slug="x-revenue-analyzer", name="X収益分析くん", bname="ふくぶん (Fukubun)", bx="FFBuncho",
    tagline="Breaks down your X creator payouts, screenshot by screenshot.",
    description="Walks you through the screenshots it needs, then analyses your X creator revenue: period over period change, earnings per 1,000 verified impressions, and which posts drove the growth, keeping facts apart from guesses.",
    category="money",
    features=["Earnings per verified impression", "Period comparisons", "Separates facts from estimates"],
    source="https://x.com/FFBuncho/status/2122647715884707852",
    url="https://x.ai/bot/SFBsXqdE8UYYMn6YkpcDN")

add(slug="x-buzz-analyzer", name="X Buzz Analyzer & Post Ideas", bname="ふくぶん (Fukubun)", bx="FFBuncho",
    tagline="Works out what lands in your X posts, then drafts the next ones.",
    description="Collects your X posts that took off, shows what is working, and gives data-backed advice with draft posts tuned to current trends and your recent reach, each opening in the composer. It runs only when asked and never posts.",
    category="creative",
    features=["Breakdown of posts that worked", "Draft posts with composer links", "Never posts for you"],
    source="https://x.com/FFBuncho/status/2122647715884707852",
    url="https://x.ai/bot/wcSgO2jhL0MnxJ-5AuZ-v")

add(slug="x-reply-catch-up", name="X Reply & Quote Catch-Up", bname="ふくぶん (Fukubun)", bx="FFBuncho",
    tagline="Shows the replies and quotes you still owe people.",
    description="Lists the replies and quote posts to you that you have not answered, ranked by relationship, intensity and importance, split into positive and negative, each with a direct link to the post. Run it once or on a schedule you pick.",
    category="productivity",
    features=["Ranks unreplied mentions", "Positive and negative split", "Direct link to each post"],
    source="https://x.com/FFBuncho/status/2122647715884707852",
    url="https://x.ai/bot/ZUeyiqvontqi6d5aVGV9-")

add(slug="subscription-killer", name="Subscription Killer", bname="Unicode Fawn", bx="",
    tagline="Finds your recurring charges and drafts the cancellations.",
    description="Reads Gmail receipts to list the subscriptions you are paying for, then drafts the cancellation messages for you to approve. It never cancels a plan or sends anything on its own.",
    category="money",
    features=["Finds charges in Gmail receipts", "Drafts cancellations", "Approval before anything sends"],
    source="https://x.com/savvy_luvvvv/status/2122616727280173518",
    url="https://x.ai/bot/hL-3EkQ2UDU8HdgYpDPga")

add(slug="wordpress-admin", name="WordPress Admin", bname="Lucas K", bx="",
    tagline="Runs a WordPress site through the REST API, carefully.",
    description="Handles posts, pages, media, comments, users, plugins, settings and health checks on a WordPress site using the REST API and an Application Password, and asks before every risky change.",
    category="engineering",
    features=["Posts, pages and media", "Users, plugins and settings", "Approval before risky changes"],
    source="https://x.com/Livvux/status/2122603239866859992",
    url="https://x.ai/bot/0LStaAgvBFXULZi3OuifT")

add(slug="copy-polish-bot", name="洗稿Bot", bname="明路 张", bx="zhang7978840",
    tagline="Rewrites stiff drafts so they read like a person wrote them.",
    description="Tightens drafts, emails, pages and video scripts while keeping your voice, shows every change with the reason for it, and does not invent facts.",
    category="creative",
    features=["Keeps your voice", "Explains each edit", "No invented facts"],
    source="https://x.com/zhang7978840/status/2122593263701917807",
    url="https://x.ai/bot/2NSL2mxPreCBtS72ICxm2")

add(slug="walletbotmcp", name="walletbotmcp", bname="Plum.ton", bx="plum_ton",
    tagline="Crypto perps assistant with fixed risk rules.",
    description="Analyses crypto markets and trades perpetual futures through the Walt connector under strict risk limits, with an optional hourly auto-trading mode.",
    category="money",
    features=["Perps market analysis", "Trades through the Walt connector", "Optional hourly automation"],
    source="https://x.com/plum_ton/status/2122592392238825951",
    url="https://x.ai/bot/H5HAeShwpSP43We4cu6cr")

add(slug="douyin-video-reviewer", name="抖音审片员", bname="明路 张", bx="zhang7978840",
    tagline="Reviews a Douyin video for policy and reach risk before you post.",
    description="Checks a Douyin video, subtitles, title, cover and copy for violation, throttling and low-quality risk, marks the timestamp and severity, and gives the reasoning and a fix. It does not promise the video will pass.",
    category="creative",
    features=["Timestamped risk flags", "Severity with a fix for each", "Follows new Douyin rules"],
    source="https://x.com/zhang7978840/status/2122592029175644177",
    url="https://x.ai/bot/dhC4qP2M89ztoVHBw5yk4")

add(slug="jira-sync", name="Jira Sync", bname="Felix Jumason", bx="",
    tagline="Moves Jira cards to match what you actually shipped.",
    description="Reads commits, pull requests and local work from Claude Code, Cursor, Codex, VS Code and other editors, then moves Jira cards, adds evidence comments and writes standups and weekly reports.",
    category="engineering",
    features=["Reads commits and pull requests", "Updates cards with evidence", "Standups and weekly reports"],
    source="https://x.com/blackie_360/status/2122588336745554155",
    url="https://x.ai/bot/_91qkYwSfXDJMAZnO6eW9")

add(slug="groyper-rewards-projector", name="Groyper Rewards Projector", bname="", bx="",
    tagline="Projects the SOL a Groyper holding would have earned.",
    description="Takes Solana contract addresses and your Groyper holding percentage and estimates the SOL you would have earned at Groyper's 24 hour volume, using live DexScreener data and the 3% tax model, then writes a post you can copy.",
    category="money",
    features=["Live DexScreener data", "Uses the 3% tax model", "Copy-paste X post"],
    source="https://x.com/GoatGucciMeme/status/2122571711073976686",
    url="https://x.ai/bot/Qf-3BtPL9c_Z3kmVO9NYv")

add(slug="coinbase-trading-manager", name="Coinbase Trading Manager", bname="Lazaro Julio Munoz Calvo", bx="LazaroJMCC",
    tagline="Conservative spot trading on Coinbase, with stops in place.",
    description="Watches the crypto market and manages spot positions on Coinbase under tight risk limits, protecting holdings with stop orders and trading only clear, low-risk setups.",
    category="money",
    features=["Spot only", "Stop-loss protection", "Waits for low-risk setups"],
    source="https://x.com/LazaroJMCC/status/2122567112736575812",
    url="https://x.ai/bot/MiHKoeboMpvaq-u8v98M9")

add(slug="tennis-coach", name="Tennis", bname="Gregg", bx="GreggApplefield",
    tagline="Books courts, plans training and tracks your tennis season.",
    description="A tennis assistant for club players: it books courts as soon as slots open, plans the training week, and keeps track of tournaments, hitting partners and gear.",
    category="life",
    features=["Court booking on release", "Weekly training plan", "Tournament and partner tracking"],
    source="https://x.com/GreggApplefield/status/2122558332930277385",
    url="https://x.ai/bot/3khpwD1olHmofICOxNvUl")

add(slug="family-fortress", name="Family Fortress", bname="Greg Bailey", bx="gregbailey",
    tagline="Builds a family plan for a long outage, then shops it.",
    description="Works out a prioritised preparedness plan for an extended power-grid outage, then finds weekly deals and hands you one cart to approve. Nothing is bought without your yes.",
    category="life",
    features=["Prioritised outage plan", "Weekly deal shortlist", "One cart for approval"],
    source="https://x.com/gregbailey/status/2122550829907673134",
    url="https://x.ai/bot/hyATTQBpq10-5IZ0bqTLi")

add(slug="feedback-board", name="Feedback Board", bname="Calix Build", bx="CaliLumberJack",
    tagline="Turns scattered feedback into cards on your project board.",
    description="A private feedback board for small software teams: it turns bugs, requests and ideas from mail, X or pasted text into cards on GitHub Projects, Linear, Trello, Notion or a local board. Nothing sends without your approval.",
    category="productivity",
    features=["Mail, X and pasted input", "GitHub Projects, Linear, Trello, Notion", "Approval before sending"],
    source="https://x.com/CaliLumberJack/status/2122525149232505060",
    url="https://x.ai/bot/JUXsVsVBG-mWEIDKdQrrX")

add(slug="first-week-crew", name="First Week Crew", bname="Calix Build", bx="CaliLumberJack",
    tagline="Gets a brand new Grok Bot user productive in their first week.",
    description="A lead bot for people new to Grok Bot: it sorts today's inbox in the first five minutes for a real result, then sets up up to four starter helpers across the week, one at a time and each only on your approval.",
    category="assistants",
    features=["First result in five minutes", "Up to four starter helpers", "Approval at each step"],
    source="https://x.com/CaliLumberJack/status/2122525149232505060",
    url="https://x.ai/bot/JvzKNX4bwA6gtUmlvtcZZ")

add(slug="promo-code-bot", name="Promo Code Bot", bname="John Boyle", bx="johnboyle",
    tagline="Hunts working promo codes before you check out.",
    description="Takes the store, items and cart total, finds promo codes that actually work for that cart, and compares the final price, including as the last step before checkout inside Grok Bot shopping. A code only counts as verified once the store's own cart confirms it.",
    category="money",
    features=["Cart-aware code search", "Verified against the store cart", "Works inside bot shopping"],
    source="https://x.com/johnboyle/status/2122513899962695711",
    url="https://x.ai/bot/YTA8VEBNlEbypIrrSg_XG")

add(slug="arbitrage-bot-kr", name="아비트라지 봇", bname="Trader Jeon", bx="",
    tagline="Watches Korean crypto premiums and helps you act on them.",
    description="Monitors the USDT premium and reverse premium between Bithumb and Upbit on one side and Bitget and Binance on the other, alerts you when it crosses your threshold, and helps move USDT and place the trade once you confirm.",
    category="money",
    features=["Premium and reverse premium watch", "Threshold alerts", "Transfer and trade on confirm"],
    source="https://x.com/ministerbtc/status/2122497448241164759",
    url="https://x.ai/bot/LqIyQHNOgDHBub3YEQkAQ")

add(slug="x-follow-curator", name="X Follow Curator", bname="Alexandre Ferrari", bx="aferrari",
    tagline="Audits who you follow against what you actually care about.",
    description="Reviews your X following list against the interests you set and suggests accounts to keep, mute, unfollow or start following. Nothing changes on your account until you approve each batch.",
    category="productivity",
    features=["Follow-list audit", "Keep, mute, unfollow suggestions", "Per-batch approval"],
    source="https://x.com/aferrari/status/2122484268911702337",
    url="https://x.ai/bot/BX2oKZAPz25avyKgkK8CR")

add(slug="second-brain-commander", name="AI 第二大腦總指揮", bname="", bx="",
    tagline="A Traditional Chinese chief of staff for several workstreams.",
    description="Organises, verifies, drafts and pushes forward several workstreams at once, asking you first on anything major and labelling each judgement as fact, inference or still unverified.",
    category="assistants",
    features=["Runs several workstreams", "Labels fact, inference, unverified", "Asks before big moves"],
    source="",
    url="https://x.ai/bot/whQDUCnTd1CHvK6qi3LAk")

add(slug="sonnet-a-day", name="🎭 Sonnet a Day", bname="John Bianchi", bx="",
    tagline="One Shakespeare sonnet a day, with notes and memory work.",
    description="Works through 151 of Shakespeare's sonnets in their original 1609 order, one a day, with a plain-English paraphrase, a short close reading, a couplet to learn by heart and two questions. A dashboard tracks your streak and how far along you are.",
    category="life",
    features=["Daily sonnet with close reading", "Couplet to memorise", "Streak dashboard"],
    source="https://x.com/BTCJohnnyB/status/2122459139402010848",
    url="https://x.ai/bot/NwixIgbYNYR5oxSHDcrC8")

add(slug="token-throttler", name="Token Throttler", bname="Brian Bergen", bx="",
    tagline="Keeps a fleet of bots inside your usage limit.",
    description="Moves a household of bots between normal, token-burn and low-power modes as usage climbs or the weekly reset nears, so essential routines keep running and cheap time does not go to waste.",
    category="productivity",
    features=["Three power modes", "Watches usage and resets", "Protects essential routines"],
    source="https://x.com/AlrightTektite/status/2122412075880427877",
    url="https://x.ai/bot/Zp1z-eYzNH6WQ9Fr0h6ns")

bots = json.load(open("content/bots.json"))
have = {b["url"] for b in bots}
slugs = {b["slug"] for b in bots}
added = 0
for e in E:
    if e["url"] in have:
        print("SKIP dup url", e["url"]); continue
    if e["slug"] in slugs:
        print("SKIP dup slug", e["slug"]); continue
    entry = {
        "slug": e["slug"],
        "name": e["name"],
        "builder": {"name": e["bname"], "x": e["bx"]},
        "tagline": e["tagline"],
        "description": e["description"],
        "category": e["category"],
    }
    if e.get("features"):
        entry["features"] = e["features"]
    if e.get("source"):
        entry["source"] = e["source"]
    entry["url"] = e["url"]
    entry["addedAt"] = DATE
    entry["status"] = "published"
    bots.append(entry)
    have.add(e["url"]); slugs.add(e["slug"]); added += 1

json.dump(bots, open("content/bots.json", "w"), ensure_ascii=False, indent=1)
open("content/bots.json", "a").write("\n")
print("appended", added, "total now", len(bots))
