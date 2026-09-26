#!/usr/bin/env python3
"""Refresh ops/scout-candidates.json for the 13:15 pass (cap 50, newest kept)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'ops', 'scout-candidates.json')
FOUND = '2026-09-26T13:22:00+05:30'

NEW = [
    ('Job Hunt', '4DlWbDs7ddKWhgpQ3l71a', 'AnthonyDo',
     'Daily shortlist of matching openings from a target role plus a resume or LinkedIn profile, with tailored materials and drafted applications.',
     'https://x.com/AnthonyDo/status/2103636106982121977', 'added to directory in ops/scout-pending'),
    ('Web 3/ Crypto', 'F6GRww2AYVsAT2HajH5CK', 'Raester41',
     'Play-to-earn and DeFi briefing with a weekly news digest, a beginner lesson plan, game guides, and content ideas for gaming creators.',
     'https://x.com/Raester41/status/2103635523785064711', 'added to directory in ops/scout-pending'),
    ('NoShipSherlock', 'Lll9_CtLlBh_nEOWVQfMY', 'beyrouti',
     'Lost-package desk for a store: tracks missing, stalled and delivered-but-not-received shipments and runs carrier playbooks, holding claims and refunds for a human yes.',
     'https://x.com/beyrouti/status/2103635867004981608', 'added to directory in ops/scout-pending'),
    ('Staging QA Tester', 'PJogrsWFV5ePKHLKwMMlQ', 'njivy',
     'QA pass over a staging site: grades every feature Pass, Partial, Fail, Blocked or Not found and delivers markdown/PDF bug reports with evidence.',
     'https://x.com/njivy/status/2103635667683311946', 'added to directory in ops/scout-pending'),
    ('Fantasy Football', 'uv2Ej8EsdmBpBn0p9FnhH', 'btclawyerguy',
     'Weekly NFL co-pilot for start/sit, waiver and trade calls with bye planning, inactive swaps and gameday pings. Distinct bot from the listed fantasy-football slug (different builder and share id), so it is slugged fantasy-football-2.',
     'https://x.com/btclawyerguy/status/2103636312729194799', 'added to directory in ops/scout-pending'),
    ('Tesseract Video Editor', '11IubmXmwiQg8UdZY41SK', '',
     'Edits existing footage into a finished video with captions, sound and motion graphics; returns a portable .tsrct project plus a playable export. Display name "A-A-ron" on the platform; no handle corroborated.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('XChat 사례 큐레이터 봇', 'Sg-5129uv9Hi2RRcrjRfi', '',
     'Korean-language bot that finds fresh Grok Bot use cases on X, picks only posts with templates or concrete how-tos, summarises and translates them into a XChat group.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('FUTU 브로커 주식 거래 봇', 'cKT95HyhEKDcdZa1_tt2r', '',
     'Korean-language bot that places limit orders through Futu OpenD and reports fills; tested on paper first, live orders only when the ticker is named.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Tallyhand', '7fExIoCYvACOqWtnY0U0o', '',
     'Request desk: one place for every ask, one owner per item, and nothing sent without approval.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Shipcall', 'heDLKYR7XvlUURWPVYPZD', '',
     'Pre-release gate that returns SHIP, FIX FIRST or HOLD with the exact fixes required.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Briefkeep', 'JlW3e0RAMYLcjQ5a32rCY', '',
     'Prepares a one-page brief before a meeting, then logs every commitment made and carries it forward.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Shelf Scout', 'TaRhODlVo4N5mKKH6gTW6', '',
     'Weekly reading list of books and articles drawn from the work you have actually been doing.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Bound', 'f3FJP1laxNi9tVcRd_lFh', '',
     'Weekly FastBound A&D audit for FFL dealers: flags disposed sale items with a blank TTSN where the dispose-to contact has no FFL. API-only, read-only by default.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Slop Forge', 'mX3svMK3zEEfiK1XAeXEk', '',
     'Generates a contest-shaped Grok Bot kit and a draft quote-tweet from a single niche keyword. Published as a joke.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Asana Task Master', 'S2LodAIjlLw0mB30vN3Gl', '',
     'Turns action-worthy Gmail and Outlook emails into dated Asana tasks; replies in the same thread land as comments on the original task.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
]

HELD = [
    ('QA bot', None, '', 'marketplace-only row (x.ai/bot/marketplace/bots/qa-bot) with a live description but no share link, so there is no x.ai/bot/<id> url to verify or list.',
     'https://x.ai/bot/marketplace/bots/qa-bot', 'held: marketplace-only, no share link'),
    ('PM bot', None, '', 'marketplace-only row (x.ai/bot/marketplace/bots/pm-bot) with a live description but no share link.',
     'https://x.ai/bot/marketplace/bots/pm-bot', 'held: marketplace-only, no share link'),
    ('Engineering Lead', None, '', 'marketplace-only row (x.ai/bot/marketplace/bots/engineering-lead) with a live description but no share link.',
     'https://x.ai/bot/marketplace/bots/engineering-lead', 'held: marketplace-only, no share link'),
    ('Big Tony', 'hBo0iWrkgWTueZe1TyGhm', '', 'live but the share record carries no display name at all, so there is no builder to attribute it to.',
     'https://github.com/majiayu000/awesome-grok-bot', 'held: no display name'),
    ('Chief of Staff (daniel xu)', '-sOdLVj33yh8hh7OlHogi', '', '404 on the share link published in his demo post; his other two links are already listed. Logged, not queued.',
     'https://x.com/danieldxu_/status/2093480750146552176', 'rejected: 404'),
    ('The pm (daniel xu)', '1HFC3QdqPtcj1FIbKf8oq', '', '404 on the share link published in his demo post. Logged, not queued.',
     'https://x.com/danieldxu_/status/2093480750146552176', 'rejected: 404'),
    ('(unlisted id)', 'zKmuIjjZJmPOpwkuaCgIj', '', '404 in the catalogue sources; no share record.',
     'https://github.com/majiayu000/awesome-grok-bot', 'rejected: 404'),
    ('Tradbot (alias id)', 'wOE4e95HNxhSbrzyLkSI-', '', 'marketplace-side alias id of the already-listed tradbot (uY_7s1TZILVzUeJ9lLOx9). Same name and description; adding it would create a duplicate twin.',
     'https://github.com/majiayu000/awesome-grok-bot', 'held: alias of a listed bot'),
]


def main():
    old = json.load(open(CAND, encoding='utf-8'))
    out = []
    for name, bid, handle, desc, src, status in NEW:
        out.append({
            'name': name,
            'bot_id': bid,
            'url': f'https://x.ai/bot/{bid}' if bid else src,
            'builder_x_handle': handle,
            'one_line_desc': desc,
            'source_post_url': src,
            'found_at': FOUND,
            'status': status,
        })
    for name, bid, handle, desc, src, status in HELD:
        out.append({
            'name': name,
            'bot_id': bid or '',
            'url': f'https://x.ai/bot/{bid}' if bid else src,
            'builder_x_handle': handle,
            'one_line_desc': desc,
            'source_post_url': src,
            'found_at': FOUND,
            'status': status,
        })
    out.extend(old)
    json.dump(out[:50], open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(CAND, 'a', encoding='utf-8').write('\n')
    print(f"candidates file: was {len(old)}, now {len(out[:50])} (cap 50)")


if __name__ == '__main__':
    main()
