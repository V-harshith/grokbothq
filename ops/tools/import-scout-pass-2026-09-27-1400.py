#!/usr/bin/env python3
"""Scout pass 2026-09-27 14:00 IST (cron 359022f62495). Adds this pass's
verified bots to content/bots.json.

Sources, all free, one request per host (except the registry feed's two known
endpoints and the pipeline site's single page):
  - grokbot.dev community registry feed via ops/tools/fetch-registry-feed.py
    (1,292 items, generated_at 2026-09-27T05:08:20Z; newest item added_at
    2026-09-26T23:56:52Z, so only one item landed since the 07:50 pass
    snapshot and that one was already listed - the Sept 29 contest surge has
    paused, not resumed).
  - grokbots.best payload (1,020 records). 9 of its share ids were not in the
    directory; 3 are the blank "Use this template to create a new bot" shells
    and one is the /bot/marketplace link itself, so 5 were real candidates.
  - grokbot.dev side surfaces re-checked: x.ai/bot/marketplace (rendered via
    web_extract - 62 Add links, 10 not listed by id, but every one of those 10
    is already listed under another share id, e.g. Projects Manager, figma bro,
    tinkabot, last30days, Sawyer Merritt's Home Robots), grokbotpulse.com
    (10 links, none new), grokbots.page (523 links, none new), x.ai/news
    (newest article still Grok Bot customer support, Sep 22 - nothing to add).
  - NEW surface this pass: grokbot-templates.com/api/templates, a free JSON
    endpoint (shareId, shareUrl, name, description, category, twitterHandle).
    It serves one fixed 48-item page (identical bytes on 20 different offset
    requests), of which 16 were new by share id and by name. All 16 were
    opened live and all 16 passed, though one (VPS bot) is held on policy.
  - free web_search + api.fxtwitter.com for the X side.

Verification is ops/tools/share_record_scan.py (authoritative reader: HTTP 200
AND a share record carrying a botName AND a real description). 27 ids opened
this pass, 25 passed, 20 were added. Zero paid API calls.

Handle rule: written only where the source that carries that exact share link
is authored by that handle AND a second source agrees, usually the platform
share record's sharerName matching that account's display name (checked free
through api.fxtwitter.com/HANDLE). Where the two disagree - the aggregator's
twitterHandle versus the share record's sharerName - the handle is left empty
and the row is name-only, same as the earlier name-only rows.

Deterministic + idempotent: re-running never double-adds.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, 'content', 'bots.json')
ADDED_AT = '2026-09-27'
BEST = 'https://grokbots.best'
FEED = 'https://grokbot.dev'
TPL = 'https://grokbot-templates.com'

NEW = [
    {
        'slug': 'seo-content-desk',
        'name': 'SEO Content Desk (seodraft)',
        'builder': {'name': 'Chorch', 'x': 'chorch_md'},
        'tagline': 'Plans, drafts and audits SEO blog content off real search demand.',
        'description': 'An SEO content desk for people who publish their own blog. It picks topics from real search volume, builds drafts from your own evidence rather than generic filler, and runs quality checks that strip padding before anything ships. Tied to seodraft.app.',
        'category': 'creative',
        'url': 'https://x.ai/bot/OkT4Dbjy4xVf7oVBCr8hL',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/chorch_md',
    },
    {
        'slug': 'form-first-outbound',
        'name': 'フォーム優先アウトバウンド',
        'builder': {'name': '直人 島', 'x': ''},
        'tagline': 'Japan B2B outreach worked form-first, with a copy gate and owner-GO sends.',
        'description': 'A Japan-focused B2B outreach desk that works form-first. It preps a daily batch behind a copy quality gate, sends only after the owner says GO, logs every touch in the CRM, and runs a weekly PDCA review. Aimed at AI advisory offers and similar SMB pitches.',
        'category': 'sales',
        'url': 'https://x.ai/bot/-4fEgwVFAm8w_ULi4pjmC',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/isle_claude/status/2103699353751969828',
    },
    {
        'slug': 'grok-bot-6',
        'name': 'Grok Bot',
        'builder': {'name': 'Shmuel Ashlem', 'x': 'sammya_sh'},
        'tagline': 'Stock research teammate that ranks the options and returns one pick.',
        'description': 'An investment research teammate. Give it stocks or funds and it researches current market data, fundamentals, earnings, risks and upside, ranks the candidates against each other, and returns a clear pick. It can also keep watching the ones you care about and send a weekly brief.',
        'category': 'money',
        'url': 'https://x.ai/bot/MT6acytP70wHR526vPvM3',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/sammya_sh/status/2102971805292167403',
    },
    {
        'slug': 'forge-coach',
        'name': 'Forge Coach',
        'builder': {'name': 'Coffee and Grit', 'x': 'CoffeeNGrit'},
        'tagline': 'Builds you a workout every morning from your age, gear and space.',
        'description': 'A daily workout builder. It asks a short set of questions about your age, fitness, health, gear and training space, then writes a session for you and delivers it each morning at the time you pick.',
        'category': 'life',
        'url': 'https://x.ai/bot/ZBDynmT5k_WrRqQwoxdrI',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/CoffeeNGrit/status/2104045388210508129',
    },
    {
        'slug': 'pfp-studio',
        'name': 'PFP Studio',
        'builder': {'name': 'Coffee and Grit', 'x': 'CoffeeNGrit'},
        'tagline': 'Turns a photo into three profile pictures you can keep editing.',
        'description': 'A profile picture studio. Send a photo, name a style such as a cartoon, a film look or a time period, and it returns three options to choose from. It then keeps editing your favourite until you are happy with it.',
        'category': 'creative',
        'url': 'https://x.ai/bot/EQbigdwH3pEmkYcsbgidx',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/CoffeeNGrit/status/2104045388210508129',
    },
    {
        'slug': 'agent-mail',
        'name': 'Agent Mail',
        'builder': {'name': 'JJ Englert', 'x': 'JJEnglert'},
        'tagline': 'Gives your bot an email address, learns your voice, triages the noise.',
        'description': 'Sets up an AgentMail inbox for your own bot. It learns your writing voice from your sent mail, triages incoming noise on its own, and pings you only when something genuinely needs a person.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/j9Cm3GKLDCptPwwxZWbbD',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'thailand-visa-desk',
        'name': 'Thailand Visa Desk',
        'builder': {'name': 'Daniel Hogberg', 'x': 'danhogberg'},
        'tagline': 'Tracks Thai immigration deadlines and explains the rules with sources.',
        'description': 'A Thailand immigration tracker. It keeps an eye on 90-day reports, TM30 filings, re-entry permits, TDAC and visa renewals, reminds you before each deadline, and explains the current rules with links to official sources. General information, not legal advice.',
        'category': 'life',
        'url': 'https://x.ai/bot/zAzTVZRdvW9AK9okGihzU',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'the-coder',
        'name': 'The Coder',
        'builder': {'name': 'Christie Groenewald', 'x': 'ChristieGr55447'},
        'tagline': 'Builds and fixes your app, keeps its legal pages current, tests each release.',
        'description': 'A coding assistant for small products. It builds and fixes your app, keeps the terms, privacy and how-to-use pages in step with every release, and tests each version for security before it goes live.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/eWee2PsTChAwOGEKpKpT_',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'time-back-starter',
        'name': 'Time Back Starter',
        'builder': {'name': 'AdventureNLearn', 'x': 'AdventureNLearn'},
        'tagline': 'Sets up your first helper bots and one routine in a single sitting.',
        'description': 'An onboarding bot for people new to Grok Bot. Tell it what eats your week and it sets up your first helper bots and one recurring routine in a single sitting.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/JX0GlyQa_XFKC_b8dkAXM',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'travel-specialist',
        'name': 'Travel Specialist',
        'builder': {'name': 'Arthur MacWaters', 'x': 'ArthurMacwaters'},
        'tagline': 'Owns flights, stays and ground transport end to end.',
        'description': 'A travel desk for people who do not want to plan. It owns flights, stays, ground transport and reservations, compares options on the same constraints, and hands back working links plus photos where visuals help.',
        'category': 'life',
        'url': 'https://x.ai/bot/xG8090ZuddD1vqrDdeTHZ',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'unifi-protect-alerts',
        'name': 'UniFi Protect Alerts',
        'builder': {'name': 'Matt Routa', 'x': ''},
        'tagline': 'Emails you only for the camera events that matter at your entrances.',
        'description': 'Watches UniFi Protect cameras and emails you, or anyone you nominate, only for events that matter at your entrances, such as a person detected while you are away or late at night. It reads from Protect and never writes to it.',
        'category': 'life',
        'url': 'https://x.ai/bot/t9-UluNtR8-sZdrr_bxQU',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'unreal-engine-cpp-coder',
        'name': 'Unreal Engine C++ Coder',
        'builder': {'name': 'Binxius', 'x': ''},
        'tagline': 'Writes and reviews Unreal Engine C++ gameplay code inside your project.',
        'description': 'An Unreal Engine coding assistant for solo developers and small teams. It writes, fixes and reviews C++ gameplay code for characters, weapons, AI, inventory and UI directly in your project, then walks you through the editor-side steps.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/k0jvhLXGv5AAjh6ZxfAAd',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'videofy',
        'name': 'Videofy',
        'builder': {'name': 'G Musk', 'x': ''},
        'tagline': 'Remakes an X video in Grok Imagine, beat-synced and lookbook ready.',
        'description': 'Paste an X video link and it returns a close remake built in Grok Imagine, including fashion and brand lookbooks with outfit changes and cuts synced to the beat. Aimed at X creators who want short motion pieces without an editing timeline.',
        'category': 'creative',
        'url': 'https://x.ai/bot/6_kAMXqIRrlhdolwzF0x-',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'whats-up-tonight-bot',
        'name': 'What’s Up Tonight Bot',
        'builder': {'name': 'Tim Mullin', 'x': 'stargazer_tim'},
        'tagline': 'Nightly stargazing brief: go or no-go, clouds, Moon, planets and the ISS.',
        'description': 'A nightly stargazing brief for your location. It gives a go or no-go call, cloud cover, what the Moon and planets are doing, when the ISS passes, and the best targets for the evening. The chat version of whatsuptonight.ca.',
        'category': 'life',
        'url': 'https://x.ai/bot/5vI-rX7fZpwF0hP5GI2VE',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'wikipedia-watch-bot',
        'name': 'Wikipedia Watch Bot',
        'builder': {'name': 'Phillip.png', 'x': 'phillipstewart'},
        'tagline': 'Summarises what changed on the Wikipedia articles you watch, from real diffs.',
        'description': 'Tells you what changed on the English Wikipedia articles you care about, read from the actual diffs. Paste a watchlist for a summary, or name a few articles to watch closely and get notified when they move.',
        'category': 'research',
        'url': 'https://x.ai/bot/W_zh1KmptsmuKgl8zz3qp',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'x-creator',
        'name': 'X Creator',
        'builder': {'name': 'Juan', 'x': 'cao282828'},
        'tagline': 'Posts sourced news, threads and polls on schedule to grow your X account.',
        'description': 'Runs an X account in any niche. It posts sourced news, threads and polls on a schedule and replies to larger accounts, aiming at follower growth and creator payout eligibility.',
        'category': 'sales',
        'url': 'https://x.ai/bot/6mKW38QZDoaNq1SQxu_PQ',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'x-creator-pulse-bot',
        'name': 'X Creator Pulse Bot',
        'builder': {'name': 'Jason Doty', 'x': ''},
        'tagline': 'Tracks your X account against your goals using real dated numbers.',
        'description': 'Tracks your X account against goals you set, such as follower targets or creator payout eligibility, using dated numbers rather than estimates. It also reports whether each post beat your usual performance. Read-only: it never posts or writes.',
        'category': 'sales',
        'url': 'https://x.ai/bot/-xm4yCbgrveayEQBJXI3_',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'x-financial-scanner',
        'name': 'X Financial Scanner',
        'builder': {'name': 'Dennis W', 'x': 'DennisW_15'},
        'tagline': 'Read-only markets desk that scans official accounts and hot-stock chatter.',
        'description': 'A read-only X markets desk. It scans official and economic accounts plus hot-stock sentiment, then tells you what is new, why it matters and which tickers are in play. It stays quiet when nothing material moved.',
        'category': 'money',
        'url': 'https://x.ai/bot/e3jmMweGAwbD4JlUCzHXy',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'your-dyson-bot',
        'name': 'Your Dyson Bot',
        'builder': {'name': 'Vijay Kandhalu', 'x': ''},
        'tagline': 'Controls and reports on your Dyson devices through MyDyson or Home Assistant.',
        'description': 'Controls connected Dyson devices at home through MyDyson or Home Assistant. Plain requests such as air quality, auto mode or starting the robot vacuum, and it reports the device state it actually sees.',
        'category': 'life',
        'url': 'https://x.ai/bot/XVfXkOFTGn-xN6C7drUHI',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
    },
    {
        'slug': 'youtube-clipper',
        'name': 'YouTube Clipper',
        'builder': {'name': 'Chase McCaskill', 'x': 'itsmechase'},
        'tagline': 'Clips any YouTube video to an MP4 from a link and a timestamp.',
        'description': 'Clips any YouTube video. Give it a link plus a timestamp or a description of the moment, and it returns an MP4 file, in 4K whenever the source allows it.',
        'category': 'creative',
        'url': 'https://x.ai/bot/H2qTNvMCgLSoL8FhSESlk',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': TPL,
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
            raise SystemExit("tagline too long: %s (%d)" % (bot['slug'], len(bot['tagline'])))
        bots.append(bot)
        slugs.add(bot['slug'])
        urls.add(bot['url'])
        names.add(bot['name'])
        added.append(bot['slug'])
    json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(BOTS, 'a', encoding='utf-8').write('\n')
    print("added %d: %s" % (len(added), added))
    print("skipped (already present) %d: %s" % (len(skipped), skipped))
    print("name clashes flagged: %s" % (name_clash,))
    published = [b for b in bots if b.get('status') != 'pending']
    print("directory now %d entries, %d unique urls, %d unique slugs, %d published"
          % (len(bots), len(urls), len(slugs), len(published)))


if __name__ == '__main__':
    main()
