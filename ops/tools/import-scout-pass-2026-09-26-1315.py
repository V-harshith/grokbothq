#!/usr/bin/env python3
"""Scout pass 2026-09-26 13:15 IST (cron 359022f62495).

Fresh-bot pass #2 for the day. Sources, all fetched free, one request each:
  - x.ai/bot/marketplace ItemList (84 curated templates, JSON-LD in the flight payload)
  - cs68614-hash/awesome-grokbot-templates README (1,795 ids)
  - majiayu000/awesome-grok-bot README (2,143 ids)
  - RongleCat/awesome-grok-bot README (2 ids)
  - lroolle/awesome-grokbot-templates README (158 ids)
  - kydlikebtc/awesome-grokbot README (0 ids)
  - divo12/awesome-grok-bot-templates README (19 ids)
  - grokbots.best flight payload (976 records, with author handle + source post)
plus free web_search + fxtwitter for the X side. Zero paid API calls.

Diff basis: catalogue ids vs content/bots.json AND every id already recorded in
ops/*.json + the scout state files (74 never-seen ids).

Verification is ops/tools/share_record_scan.py (the authoritative reader added
07:00 today). Every id in this pass returned HTTP 200 with a share record
carrying botName + description.

Builder handles in this pass are set only where TWO independent sources agree
on the same share id: the platform share record's sharerName, and the author of
the X post that carries that exact share link. All five handle-carrying entries
below were corroborated that way with api.fxtwitter.com (free, no auth), and the
post author's display name matches the platform sharer name in every case.

Held (unchanged policy):
  - 56 rows whose platform display name is the org name "SpaceX" (xAI's own
    first-party template library; attribution not verifiable to a community
    builder, and listing them invites an xAI-endorsement read)
  - rows with no display name at all (Big Tony, Tradbot alias id)
  - 3 blank templates ("Use this template to create a new bot or apply it to an
    existing bot"), anew, The List, "Grok Bot" twins, "Elon Musk (Algorithm &
    constraint)" (a persona of a real named individual)
  - 4 ids that 404: zKmuIjjZJmPOpwkuaCgIj, and daniel xu's
    -sOdLVj33yh8hh7OlHogi / 1HFC3QdqPtcj1FIbKf8oq (his other two are already
    listed); TNPSVnX4Dm-adBvHJbng7 is already listed (LG Laundry Specialist)
  - marketplace-only rows with no share link (QA bot, PM bot, Engineering Lead)

Deterministic + idempotent: re-running never double-adds.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, 'content', 'bots.json')
ADDED_AT = '2026-09-26'
GB = 'https://github.com/majiayu000/awesome-grok-bot'

NEW = [
    {
        'slug': 'job-hunt',
        'name': 'Job Hunt',
        'builder': {'name': 'Anthony', 'x': 'AnthonyDo'},
        'tagline': 'Hand it a target role plus a resume or LinkedIn profile and it searches daily, tailors materials, and drafts applications.',
        'description': 'Tell it the role you want and give it a resume or LinkedIn profile. It searches for matching openings every day, tailors your materials to each one, and drafts applications ready for you to send.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/4DlWbDs7ddKWhgpQ3l71a',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/AnthonyDo/status/2103636106982121977',
    },
    {
        'slug': 'web-3-crypto',
        'name': 'Web 3/ Crypto',
        'builder': {'name': 'Rae', 'x': 'Raester41'},
        'tagline': 'Weekly play-to-earn and DeFi briefing with a beginner lesson plan, game guides, and content ideas for gaming creators.',
        'description': 'A beginner-friendly guide to play-to-earn gaming and DeFi. It sends a weekly news briefing, writes step-by-step lesson plans for newcomers, produces game guides, and suggests content ideas for creators covering the space.',
        'category': 'money',
        'url': 'https://x.ai/bot/F6GRww2AYVsAT2HajH5CK',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Raester41/status/2103635523785064711',
    },
    {
        'slug': 'noshipsherlock',
        'name': 'NoShipSherlock',
        'builder': {'name': 'Nourhan Beyrouti', 'x': 'beyrouti'},
        'tagline': 'Lost-package desk for a store: chases missing and stalled shipments, and never files a claim without a human yes.',
        'description': 'Tracks shipments that are missing, stalled, or marked delivered but never received. It runs the carrier playbook for each case and holds off on filing claims or issuing refunds until a person approves.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/Lll9_CtLlBh_nEOWVQfMY',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/beyrouti/status/2103635867004981608',
    },
    {
        'slug': 'staging-qa-tester',
        'name': 'Staging QA Tester',
        'builder': {'name': 'Nic Ivy', 'x': 'njivy'},
        'tagline': 'Walks a staging site like a real user and grades each feature Pass, Partial, Fail, Blocked or Not found.',
        'description': 'A QA pass for any web app staging site. It works through the features the way a real user would, grades each one, and returns bug reports as markdown and PDF with the evidence attached. It restores what it changes and keeps strict guardrails around accounts, passwords and data.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/PJogrsWFV5ePKHLKwMMlQ',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/njivy/status/2103635667683311946',
    },
    {
        'slug': 'fantasy-football-2',
        'name': 'Fantasy Football',
        'builder': {'name': 'Ian R. Cohen', 'x': 'btclawyerguy'},
        'tagline': 'Weekly NFL fantasy co-pilot for start/sit, waiver and trade calls, with bye planning and gameday pings.',
        'description': 'A weekly fantasy football desk for lineups, waivers and trades, weighted to your league scoring. It plans around byes, swaps players flagged inactive before kickoff, and pings you on touchdowns, big plays and turnovers. Public betting lines are treated as evidence only, and it never changes a lineup or places a bet without your confirmation.',
        'category': 'life',
        'url': 'https://x.ai/bot/uv2Ej8EsdmBpBn0p9FnhH',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/btclawyerguy/status/2103636312729194799',
    },
    {
        'slug': 'tesseract-video-editor',
        'name': 'Tesseract Video Editor',
        'builder': {'name': 'A-A-ron', 'x': ''},
        'tagline': 'Edits footage you already shot into a finished video with captions, sound and motion graphics.',
        'description': 'An editor for footage you already have rather than generated video. It assembles a finished cut with captions, sound and motion graphics, and hands back a portable .tsrct project along with a playable export.',
        'category': 'creative',
        'url': 'https://x.ai/bot/11IubmXmwiQg8UdZY41SK',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'xchat-case-curator',
        'name': 'XChat 사례 큐레이터 봇',
        'builder': {'name': 'Brandon Chung', 'x': ''},
        'tagline': 'X에서 Grok Bot 활용 사례를 주기적으로 찾아 요약·번역해 XChat 그룹에 올려주는 봇. 템플릿이나 구체적인 사용법이 있는 글만 골라요.',
        'description': 'X를 돌며 Grok Bot 같은 주제의 새 활용 사례를 찾고, 템플릿이나 구체적인 사용법이 담긴 글만 골라 요약하고 번역해 내 XChat 그룹에 올려줍니다. 커뮤니티 운영자를 위한 봇입니다.',
        'category': 'research',
        'url': 'https://x.ai/bot/Sg-5129uv9Hi2RRcrjRfi',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'futu-broker-trading',
        'name': 'FUTU 브로커 주식 거래 봇',
        'builder': {'name': 'Brandon Chung', 'x': ''},
        'tagline': 'Futu OpenD로 지정 주문을 넣고 체결되면 알려주는 주식 거래 봇. 모의로 먼저 확인하고, 실전은 종목을 지정할 때만 넣습니다.',
        'description': 'Futu OpenD를 통해 지정 주문을 넣고 체결되면 알려주는 주식 거래 봇입니다. 먼저 모의 계좌로 확인하고, 실전 주문은 종목을 직접 지정했을 때만 넣습니다.',
        'category': 'money',
        'url': 'https://x.ai/bot/cKT95HyhEKDcdZa1_tt2r',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'tallyhand',
        'name': 'Tallyhand',
        'builder': {'name': 'Brandon Pendleton', 'x': ''},
        'tagline': 'Every request in one place with one owner per item, and nothing sent without your OK.',
        'description': 'A request desk that keeps every incoming ask in one place, assigns one owner per item, and holds anything outgoing until you approve it.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/7fExIoCYvACOqWtnY0U0o',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'shipcall',
        'name': 'Shipcall',
        'builder': {'name': 'Brandon Pendleton', 'x': ''},
        'tagline': 'Calls SHIP, FIX FIRST or HOLD before anything goes out, with the exact fixes needed.',
        'description': 'A pre-release gate. It reviews what is about to go out and returns SHIP, FIX FIRST or HOLD with the exact fixes required, so the decision is made before the release rather than after.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/heDLKYR7XvlUURWPVYPZD',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'briefkeep',
        'name': 'Briefkeep',
        'builder': {'name': 'Brandon Pendleton', 'x': ''},
        'tagline': 'One-page brief before the meeting, every commitment logged and carried forward after it.',
        'description': 'Prepares a one-page brief for a meeting, then logs the commitments made in it and carries them into the next conversation so nothing agreed in the room gets dropped.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/JlW3e0RAMYLcjQ5a32rCY',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'shelf-scout',
        'name': 'Shelf Scout',
        'builder': {'name': 'Jacob Smalley', 'x': ''},
        'tagline': 'A weekly reading list of books and articles drawn from the work you have actually been doing.',
        'description': 'Curates a weekly reading list of books and articles, chosen from the work you have really been doing rather than generic founder reading lists.',
        'category': 'life',
        'url': 'https://x.ai/bot/TaRhODlVo4N5mKKH6gTW6',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'bound',
        'name': 'Bound',
        'builder': {'name': 'Jason', 'x': ''},
        'tagline': 'Weekly FastBound A&D audit for FFL dealers: flags disposed sale items whose transfer has no receiving FFL.',
        'description': 'A weekly compliance audit for FastBound users at FFL dealers. It flags disposed sale items that carry a blank transfer number where the dispose-to contact has no FFL, working through the API read-only by default.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/f3FJP1laxNi9tVcRd_lFh',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'slop-forge',
        'name': 'Slop Forge',
        'builder': {'name': 'The Guy', 'x': ''},
        'tagline': 'Paste a niche and get a contest-shaped Grok Bot kit plus a quote-tweet draft in under a minute.',
        'description': 'Takes a single niche keyword and generates a Grok Bot template kit shaped for the template sharing contest, along with a draft quote-tweet. Published as a joke rather than a production workflow.',
        'category': 'creative',
        'url': 'https://x.ai/bot/mX3svMK3zEEfiK1XAeXEk',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
    {
        'slug': 'asana-task-master',
        'name': 'Asana Task Master',
        'builder': {'name': 'Wayne Lowry', 'x': ''},
        'tagline': 'Turns action-worthy Gmail and Outlook emails into dated Asana tasks, and files replies as comments on the task.',
        'description': 'Reads Gmail and Outlook inboxes and converts emails that need action into Asana tasks with due dates. Replies later in the same email thread land as comments on the original task, so nothing stays buried in the inbox.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/S2LodAIjlLw0mB30vN3Gl',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': GB,
    },
]


def main():
    bots = json.load(open(BOTS, encoding='utf-8'))
    slugs = {b['slug'] for b in bots}
    urls = {b['url'] for b in bots}
    added, skipped = [], []
    for bot in NEW:
        if bot['slug'] in slugs or bot['url'] in urls:
            skipped.append(bot['slug'])
            continue
        if len(bot['tagline']) > 140:
            raise SystemExit(f"tagline too long: {bot['slug']} ({len(bot['tagline'])})")
        bots.append(bot)
        slugs.add(bot['slug'])
        urls.add(bot['url'])
        added.append(bot['slug'])
    json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(BOTS, 'a', encoding='utf-8').write('\n')
    print(f"added {len(added)}: {added}")
    print(f"skipped (already present) {len(skipped)}: {skipped}")
    print(f"directory now {len(bots)} entries, {len(urls)} unique urls")


if __name__ == '__main__':
    main()
