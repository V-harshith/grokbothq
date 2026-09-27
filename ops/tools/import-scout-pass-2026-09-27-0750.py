#!/usr/bin/env python3
"""Scout pass 2026-09-27 07:50 IST (cron 359022f62495). Adds this pass's
verified bots to content/bots.json.

Sources, all free, one request each:
  - grokbot.dev community registry feed (1,291 items, fresh again: newest
    added_at 2026-09-26T23:56:52Z, generated_at 2026-09-27T00:34:24Z) via
    ops/tools/fetch-registry-feed.py. 35 items added since the 01:45 pass's
    snapshot; 4 were already listed.
  - grokbots.best payload (1,018 entries, author handle per bot) - 14 of the
    feed candidates appear there too, which is the second source that lets a
    handle be written.
  - grokbotpulse.com (10 links, none new).
  - x.ai/bot/marketplace (link-harvested; nothing new).
  - free web_search + api.fxtwitter.com for the X side (one expansion per
    candidate's source post: the post body was read to carry that candidate's
    exact share id).

Verification is ops/tools/share_record_scan.py (authoritative reader: HTTP 200
AND a share record carrying a botName AND a real description). 37 ids opened
this pass, 36 passed. Zero paid API calls.

Handle rule: written only where the post carrying that exact share link is
authored by that handle AND a second source agrees (the platform share record's
sharerName matches that account, or grokbots.best names the same handle).

Deterministic + idempotent: re-running never double-adds.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, 'content', 'bots.json')
ADDED_AT = '2026-09-27'
BEST = 'https://grokbots.best'

NEW = [
    {
        'slug': '3-day-notice-validator',
        'name': '3-Day Notice Validator',
        'builder': {'name': 'Real Estate Lawyer', 'x': 'SinaiLawFirm'},
        'tagline': 'Checks a California three-day pay-or-quit notice field by field before you serve it.',
        'description': 'A checker for California three-day notices to pay rent or quit, built around City of Los Angeles residential notices. Upload a filled notice or a blank template and it returns a rule-by-rule checklist, a verdict and a list of fixes to make. Not legal advice.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/opCFOq0FKZ41PBIiBeuVO',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/SinaiLawFirm/status/2103997263009980625',
    },
    {
        'slug': 'it-department-lead',
        'name': 'IT Department Lead',
        'builder': {'name': 'DCOL Admin', 'x': 'braytron'},
        'tagline': 'Runs a fleet of IT sibling bots and takes on the cross-cutting asks.',
        'description': 'A coordinating lead for a team of specialised IT bots. It imports with design-a-bot, handles secret intake and fleet healthchecks, and carries portable Windows triage skills so the desk keeps working when one bot is down.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/28cjt6-FRq2D69vUX5F9L',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/braytron/status/2103994716685791345',
    },
    {
        'slug': 'calendar-liftoff',
        'name': 'Calendar Liftoff',
        'builder': {'name': 'Grokx Fan', 'x': 'tdsfixer'},
        'tagline': 'Turns a theme, a subject or a year into a print-ready 12x12 photo wall calendar.',
        'description': 'Give it a theme, a subject or a year and it builds a print-ready 12x12 photo wall calendar PDF, one full-bleed photo and a clean date grid for every month. It then finds a printer and walks you through ordering a single copy.',
        'category': 'creative',
        'url': 'https://x.ai/bot/nJ7hHZsPczXvJIi0wv8c-',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/tdsfixer/status/2103993998675448184',
    },
    {
        'slug': 'quill',
        'name': 'Quill',
        'builder': {'name': 'John Koisch', 'x': 'the_simonjester'},
        'tagline': 'Craft pass for Obsidian notes: voice punch-up, continuity or a depth read.',
        'description': 'A writing craft pass for Obsidian notes. Point it at a note and pick the job: voice punch-up, continuity check or a depth read on the writing you point it at. Part of the Obsidian Vault Kit alongside Porter for intake and Groundskeeper for hygiene.',
        'category': 'creative',
        'url': 'https://x.ai/bot/tHo33t3IaAhpxds5IpNbD',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/the_simonjester/status/2103992041734811919',
    },
    {
        'slug': 'scriptsprint',
        'name': 'ScriptSprint',
        'builder': {'name': 'John Koisch', 'x': 'the_simonjester'},
        'tagline': 'Turns voice, meeting and rant transcripts into speakers, action items and library atoms.',
        'description': 'Converts voice memos, meeting recordings and rant transcripts into a speaker breakdown, a summary and a list of action items, plus candidates for a notes library. It never overwrites the raw transcript.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/YV5xOs96YaWLN39PbkPwk',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/the_simonjester/status/2103991653375824068',
    },
    {
        'slug': 'solopreneur-chief-of-staff',
        'name': 'Solopreneur Chief of Staff',
        'builder': {'name': 'Mainly Digital', 'x': 'c0rtex1100X'},
        'tagline': 'Chief of staff for solopreneurs: short scoreboards and hard approval gates.',
        'description': 'A chief of staff for one-person businesses. It keeps short scoreboards, enforces hard approval gates before anything leaves your desk, and proposes same-cycle fixes when a workstream goes flat.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/NsCDfZMFctaP1WIp_48k4',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/c0rtex1100X/status/2103990572000378881',
    },
    {
        'slug': 'mamboitalianobot',
        'name': 'MamboItalianoBot',
        'builder': {'name': 'Mambo Italiano', 'x': 'mamboitaliano__'},
        'tagline': 'Travel assistant that builds realistic itineraries without inventing hours or prices.',
        'description': 'A travel assistant for planning a trip: realistic itineraries, transport and lodging options with pros and cons, checklists and a plan B. It is explicit about not inventing opening hours or prices.',
        'category': 'life',
        'url': 'https://x.ai/bot/F0ZQruHL4AsmoLxWWLvUG',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/mamboitaliano__/status/2103990336242761964',
    },
    {
        'slug': 'shawn',
        'name': 'Shawn',
        'builder': {'name': 'Badger Bets', 'x': 'BadgersBet'},
        'tagline': 'Paper-first sports betting research desk that tracks closing-line value.',
        'description': 'A paper-first research desk for sports betting. It hunts closing-line value and juice-aware expected value, drafts an auditable daily card and keeps a ticket ledger. It never places bets.',
        'category': 'money',
        'url': 'https://x.ai/bot/gEEv8k6WgJyU8es3eaXi7',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/BadgersBet/status/2103989579980108154',
    },
    {
        'slug': 'handyman',
        'name': 'Handyman',
        'builder': {'name': 'Dylan Mitchell', 'x': 'dkmitc'},
        'tagline': 'Household maintenance tracker that remembers your filter sizes and due dates.',
        'description': 'A household maintenance tracker. It remembers your filter size, logs when each task was last done, and reminds you about filter changes, water heater flushes, seasonal HVAC tune-ups and seasonal cleaning.',
        'category': 'life',
        'url': 'https://x.ai/bot/rQvB9sFrdQU7Ef43jOxgI',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/dkmitc/status/2103988834253820025',
    },
    {
        'slug': 'pal',
        'name': 'Pal',
        'builder': {'name': 'Badger Bets', 'x': 'BadgersBet'},
        'tagline': 'MLB matchup scout that surfaces hitter and pitcher spots from projections.',
        'description': 'An MLB matchup scout for a single owner. It surfaces the day\'s best hitter pass spots and pitcher strikeout spots from BallparkPal projections, arsenal checks and soft batter-versus-pitcher history. Short boards only, and it never places bets.',
        'category': 'money',
        'url': 'https://x.ai/bot/9Zvz4Qe0dxRjo4H984gOI',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/BadgersBet/status/2103988405558513795',
    },
    {
        'slug': 'brew-what-you-got',
        'name': 'Brew What You Got',
        'builder': {'name': 'Vitality Ebatez', 'x': 'Ebatez_'},
        'tagline': 'Cafe-style drink recipes built from the machine, beans and syrups you already own.',
        'description': 'Tell it your coffee machine, beans, milk, syrups and spices and it returns cafe-style drink recipes you can make right now from what is already in the kitchen.',
        'category': 'life',
        'url': 'https://x.ai/bot/YlzTbxg6wPAKYJutJ00rG',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Ebatez_/status/2103988316190433499',
    },
    {
        'slug': 'phone-use-bot',
        'name': 'Phone Use Bot',
        'builder': {'name': 'Harsh Manoj Jain', 'x': 'harshmanojjain'},
        'tagline': 'Remotely drives your Android phone over Tailscale and wireless debugging.',
        'description': 'A bot that controls your Android phone remotely: it mirrors the screen over Tailscale and wireless debugging, then taps through apps and settings for you. Built for anyone who wants an assistant that can actually use their phone.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/SjBZH94wJlen_fuVsoYaO',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/harshmanojjain/status/2103987874077307067',
    },
    {
        'slug': 'opus-motion',
        'name': 'Opus Motion',
        'builder': {'name': 'Matt Rice', 'x': 'bossriceshark'},
        'tagline': 'Short motion-graphics product and brand videos, drafted as MP4 files.',
        'description': 'Produces short motion-graphics product and brand videos as MP4 drafts. Paste a product link to start and it works through the danny.md motion-ad skill. Draft files only, so you publish.',
        'category': 'creative',
        'url': 'https://x.ai/bot/-ozpDFk78Euk4sbbfmRn4',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/bossriceshark/status/2103987844394160149',
    },
    {
        'slug': 'the-box-of-names',
        'name': 'The Box of Names',
        'builder': {'name': 'jack', 'x': 'BLDG_390'},
        'tagline': 'Traces how any word, place, god or object travelled across civilizations.',
        'description': 'An Atlas Obscura for names. Give it any word, place, god or object and it traces how the name travelled between civilizations, tagging every link as real or as a possible false echo.',
        'category': 'research',
        'url': 'https://x.ai/bot/M0ZZw7AT7MzGjvYe1jLBb',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/BLDG_390/status/2103987768196211108',
    },
    {
        'slug': 'x-growth-assistant',
        'name': 'X Growth Assistant',
        'builder': {'name': 'Donald Moore', 'x': 'DonaldMoor91672'},
        'tagline': 'Cleans up and grows an X account: unfollows non-followers, clears bots.',
        'description': 'Keeps an X account clean and growing. It unfollows accounts that do not follow back, clears out bots and dead accounts, follows people in your niche, and can run the cleanups on a slow autopilot.',
        'category': 'sales',
        'url': 'https://x.ai/bot/B4ro8N0_j3XGF5ras3iW0',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/DonaldMoor91672/status/2103987428528882072',
    },
    {
        'slug': 'superfan',
        'name': 'Superfan',
        'builder': {'name': 'Samuel Dickinson', 'x': 'SamuelD2022'},
        'tagline': 'Daily brief on your favourite teams: next game, last result, season record.',
        'description': 'A sports fan daily brief. Pick your favourite teams and a delivery time and it sends the next game, the last result and the season record every day, with optional news headlines.',
        'category': 'life',
        'url': 'https://x.ai/bot/l5MDTh-AZS2Frx4b2TYy_',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/SamuelD2022/status/2103987020964241870',
    },
    {
        'slug': 'ai-security-advisor',
        'name': 'AI Security Advisor',
        'builder': {'name': 'zeus', 'x': 'zeuss_000'},
        'tagline': 'Defensive advisor that hardens AI apps against prompt injection and leaks.',
        'description': 'A defensive security advisor for teams building with AI. It covers hardening against prompt injection, tool abuse and data leakage, plus the surrounding governance. It does not provide offensive playbooks.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/rrKp1eA9QnW8P5QAGKaKS',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/zeuss_000/status/2103984574061842850',
    },
    {
        'slug': 'webb-knox',
        'name': 'Webb Knox',
        'builder': {'name': 'Rardo', 'x': 'gerardocasta711'},
        'tagline': 'Lead specialist that finds scored, verified leads and drafts honest outreach.',
        'description': 'A lead specialist for anyone who sells. Tell it what you are after and it finds verified leads with the reason each one needs you now, drafts outreach and follow-ups in plain language, and sends a weekly pipeline recap.',
        'category': 'sales',
        'url': 'https://x.ai/bot/7veO5EEAD-LxgkOGy4sjk',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/gerardocasta711/status/2103983798622806061',
    },
    {
        'slug': 'elon-ecosystem-desk',
        'name': 'Elon Ecosystem Desk',
        'builder': {'name': 'CHRISV', 'x': 'cvey15'},
        'tagline': 'Sourced news desk for X, Tesla, SpaceX, xAI, Neuralink and The Boring Company.',
        'description': 'A news desk covering X, Tesla, SpaceX and Starlink, xAI and Grok, Neuralink and The Boring Company. It separates rumour from confirmed reporting and can run a daily brief.',
        'category': 'research',
        'url': 'https://x.ai/bot/j8Znml_qB4leZhOgihZ-p',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/cvey15/status/2103982737207996649',
    },
    {
        'slug': 'bookmark-miner',
        'name': 'Bookmark Miner',
        'builder': {'name': 'Reuben H', 'x': 'therookiehacker'},
        'tagline': 'Reads your X bookmarks and returns a short ranked list of things worth doing.',
        'description': 'Reads your X bookmarks and turns them into a short, ranked list of things worth acting on: skills to write, projects to build, features for what you already run, ways to earn and changes to your AI setup. Read-only on X.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/2KoI66uCOtx0PSf3do4tK',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/therookiehacker/status/2103980722189197456',
    },
    {
        'slug': 'market-sentiment-bot',
        'name': 'Market Sentiment Bot',
        'builder': {'name': 'itachi data', 'x': 'Itachidata'},
        'tagline': 'Scores US risk assets from 1.0 to 10.0 with a market card and ticker cards.',
        'description': 'Scores US risk assets from 1.0 to 10.0 and returns a market-wide card plus optional cards for tickers you choose. It works from public web data and states that it does not invent prints.',
        'category': 'money',
        'url': 'https://x.ai/bot/dpEIOmZE65XCVEnPJUp_-',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Itachidata/status/2103974697834598748',
    },
    {
        'slug': 'connection-mapper',
        'name': 'Connection Mapper',
        'builder': {'name': 'Michael A.M.E.', 'x': 'MindandEmotion7'},
        'tagline': 'Maps the links between two people, groups or companies, with sources.',
        'description': 'Give it two people, groups or companies and it maps every direct and one-step-removed link between them: investments, board seats and ownership chains, hiring, political donations, shared societies and photos, and X. Results land in sourced Obsidian notes, and you can suggest intermediaries to test.',
        'category': 'research',
        'url': 'https://x.ai/bot/9zEVJ7Eya66BLQ11xhPlD',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MindandEmotion7/status/2103945021863129514',
    },
    {
        'slug': 'video-editor',
        'name': 'Video Editor',
        'builder': {'name': 'Ross', 'x': 'ross_zeiger'},
        'tagline': 'Turns a desk talking-head recording into a clean branded YouTube cut.',
        'description': 'Drop in a desk talking-head recording and get a clean, branded cut for YouTube. It also guides first-run installs and helps you assemble your own motion brand kit.',
        'category': 'creative',
        'url': 'https://x.ai/bot/Oo4vOtwAggO933EwCmKrc',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/ross_zeiger/status/2103941921983107481',
    },
    {
        'slug': 'grok-workhorse',
        'name': 'Grok Workhorse',
        'builder': {'name': 'ali mahmoudnia', 'x': 'Mahmoudnia95'},
        'tagline': 'Coding supervisor that hands bounded tasks to sandboxed agents and reviews the diffs.',
        'description': 'A coding supervisor. It breaks work into bounded tasks, hands them to sandboxed coding agents on its own computer, then reviews the diff and the test results before anything reaches you. Works with any OpenAI-compatible model.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/MTQNKdLtJX0pplFm8CRvO',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Mahmoudnia95/status/2103931914918801592',
    },
    {
        'slug': 'github-pr-desk',
        'name': 'GitHub PR Desk',
        'builder': {'name': 'Michael', 'x': 'MichaelGannotti'},
        'tagline': 'Weekday digest of the pull requests and issues on the repos you choose, with verdicts.',
        'description': 'A morning desk for GitHub. Every weekday it sweeps the repos you choose for new pull requests, issues and comments, sends one short digest, and gives each PR a merge, request changes or close verdict. It never merges without your yes and drafts every public comment for approval.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/Ih9HEfCaYjMKbEZqSfbic',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MichaelGannotti/status/2103929935337595076',
    },
    {
        'slug': 'master-chief-2',
        'name': 'Master Chief',
        'builder': {'name': 'Peter Sinke', 'x': 'psinke'},
        'tagline': 'Personal chief of staff for inbox and calendar that never auto-sends.',
        'description': 'A personal chief of staff for email and calendar. It triages the inbox, drafts replies in your voice, preps meetings and sends a weekday morning brief. Nothing goes out without you.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/F8vp6AGwCX3DYuTJ_aahF',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/psinke/status/2103929339263770887',
    },
    {
        'slug': 'first-week-coach',
        'name': 'First-Week Coach',
        'builder': {'name': 'Michael', 'x': 'MichaelGannotti'},
        'tagline': 'Seven-day, ten-minutes-a-day starter course for people new to Grok Bot.',
        'description': 'A starter course for people new to Grok Bot: one 10-minute lesson a day for seven days. It learns your work, picks three bots worth adding, teaches routines, approvals and safe connections, then runs a weekly check-up. An unofficial guide, unaffiliated with the platform.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/kOQ7mWg9DLWq2-UpGKf67',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MichaelGannotti/status/2103927818216411541',
    },
    {
        'slug': 'ssh-to-grok-bot-via-tailscale',
        'name': 'SSH to Grok Bot via Tailscale',
        'builder': {'name': 'Altman Sam', 'x': ''},
        'tagline': 'Gets you SSH access into the bot\'s own computer over your tailnet.',
        'description': 'Installs Tailscale on the bot\'s own computer so you can SSH in over your tailnet, either from a local client or the Tailscale web console. On the first run it sets up Tailscale SSH and boot autostart, and it warns you not to update the computer image.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/BrViAOWzDSiAjBLqUnBgA',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/app_sail/status/2103886508264653232',
    },
    {
        'slug': 'seishin-mental-advisor',
        'name': '精神メンタル・アドバイザー',
        'builder': {'name': 'Shimpei Araki', 'x': ''},
        'tagline': 'Sorts past notes into fact, interpretation and unconfirmed, then offers a next move.',
        'description': 'A self-observation bot for daily life. It sorts earlier notes into fact, interpretation and unconfirmed, applies a metacognition pass, then offers one to three next moves. It does not diagnose and does not post on your behalf.',
        'category': 'life',
        'url': 'https://x.ai/bot/ZCm7Z2hxDPeGPmMIpjCId',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/shin_chan_ai/status/2103859145774702907',
    },
    {
        'slug': 'x-ops-advisor-ja',
        'name': 'X運用アドバイザー',
        'builder': {'name': 'Shimpei Araki', 'x': ''},
        'tagline': 'Weekly consulting-style report built from your own X account data.',
        'description': 'Reads your own X account data and builds a consulting-style weekly report with supporting material. Posting, following and DMs stay behind a human gate. Aimed at creators and social media operators.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/lQyIEp3Wqbm8X78tLTa-8',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/shin_chan_ai/status/2103858945542717895',
    },
    {
        'slug': 'the-morning-paper',
        'name': 'The Morning Paper',
        'builder': {'name': 'Raildragon', 'x': ''},
        'tagline': 'A sourced local morning paper for one US ZIP code, weekdays and weekends.',
        'description': 'A daily morning paper for a US ZIP code: live weather, local news, national and world headlines and nearby jobs, all sourced. It prints a weekday edition Monday to Friday and a weekend edition on Saturday and Sunday, inside your chat.',
        'category': 'life',
        'url': 'https://x.ai/bot/e5UBnGbfvCyML0pahKPNw',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MAGAmechanic60/status/2103999477761896621',
    },
    {
        'slug': 'tripscout',
        'name': 'TripScout',
        'builder': {'name': 'Haim Bahari', 'x': 'HaimBahari'},
        'tagline': 'Travel agent that researches destinations, flights, hotels and campsites.',
        'description': 'A travel agent that researches destinations, flights, hotels and campsites, builds day-by-day itineraries and hands back verified options with direct booking links. It never books or charges anything itself.',
        'category': 'life',
        'url': 'https://x.ai/bot/JOqKmRtk249knj1lWv3dl',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/HaimBahari/status/2103999986639995214',
    },
    {
        'slug': 'baitcheck',
        'name': 'BaitCheck',
        'builder': {'name': 'Renee Rudczynski', 'x': 'reneerud'},
        'tagline': 'Paste a cold DM, ad or video card and get a safe, suspicious or scam verdict.',
        'description': 'A checker for cold outreach. Paste the bait, whether that is a DM, an ad or a video card, and it returns one verdict: safe, suspicious or likely scam. Live for X today, with other platforms planned.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/nXIyPDFW9mbmer2qdt4FW',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/reneerud/status/2104000131590988152',
    },
    {
        'slug': 'porter-2',
        'name': 'Porter',
        'builder': {'name': 'John Koisch', 'x': 'the_simonjester'},
        'tagline': 'Files dumps and inbox notes into your Obsidian vault with frontmatter.',
        'description': 'Files dumps and inbox notes into an Obsidian vault, choosing the door, the frontmatter and the path. Part of the Obsidian Vault Kit with Groundskeeper for hygiene and Quill for craft.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/sy364bgoJN8Rb5vZo4Abo',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/the_simonjester/status/2103992665268441124',
    },
    {
        'slug': 'inbox-first-pass',
        'name': 'Inbox First Pass',
        'builder': {'name': 'Mike Mosley', 'x': ''},
        'tagline': 'Weekday morning mail triage with one-line draft replies, quiet when calm.',
        'description': 'A weekday morning pass over your mail: it flags urgent and reply-needed threads with one-line draft replies, and stays quiet when nothing needs you. It never sends without your yes.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/gJ3AERRL_vWOhTBgKm-2G',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': BEST,
    },
    {
        'slug': 'chief-of-staff-worldwidevibes',
        'name': 'Chief of Staff',
        'builder': {'name': 'WorldWideVibes', 'x': 'W0rldwid3vib3s'},
        'tagline': 'Keeps your top priorities moving and drafts everything for your OK.',
        'description': 'A chief of staff for solo creators and small teams. It keeps your one to three top priorities moving, protects your time and drafts everything for your approval. It never sends or posts without your say-so.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/Afwm3MUhTO3TxHYV_wdm6',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/W0rldwid3vib3s/status/2103988528581648524',
    },
]


def main():
    bots = json.load(open(BOTS, encoding='utf-8'))
    slugs = {b['slug'] for b in bots}
    urls = {b['url'] for b in bots}
    names = {b['name'] for b in bots}
    added, skipped, name_clash = [], [], []
    for bot in NEW:
        if bot['slug'] in slugs or bot['url'] in urls:
            skipped.append(bot['slug'])
            continue
        if bot['name'] in names and not bot['slug'].endswith('-2'):
            name_clash.append((bot['slug'], bot['name']))
        if len(bot['tagline']) > 140:
            raise SystemExit(f"tagline too long: {bot['slug']} ({len(bot['tagline'])})")
        bots.append(bot)
        slugs.add(bot['slug'])
        urls.add(bot['url'])
        names.add(bot['name'])
        added.append(bot['slug'])
    json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(BOTS, 'a', encoding='utf-8').write('\n')
    print(f"added {len(added)}: {added}")
    print(f"skipped (already present) {len(skipped)}: {skipped}")
    print(f"name clashes flagged: {name_clash}")
    print(f"directory now {len(bots)} entries, {len(urls)} unique urls, "
          f"{len({b['slug'] for b in bots})} unique slugs")


if __name__ == '__main__':
    main()
