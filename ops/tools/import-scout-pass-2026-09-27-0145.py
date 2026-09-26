#!/usr/bin/env python3
"""Scout pass 2026-09-27 01:45 IST (cron 359022f62495).

Sources, all free, one request each:
  - grokbot.dev community registry feed (1,254 items, 1,048 with a share_url,
    plus the source post per item) via ops/tools/fetch-registry-feed.py
  - grokbots.best flight payload (1,004 bot links, author handle when present)
  - six awesome-grokbot catalogue READMEs (majiayu000, RongleCat, cs68614-hash,
    divo12, plus grokbots.page and the x.ai/bot/marketplace ItemList)
  - grokbotpulse.com (new surface checked this pass: 10 links, all already listed)
  - free web_search + api.fxtwitter.com for the X side.
Zero paid API calls.

Verification is ops/tools/share_record_scan.py (authoritative reader): HTTP 200
AND a share record carrying a botName AND a real description. 87 new ids were
opened; 60 passed that bar.

Of those 60, 56 are the standing hold "first-party rows whose platform display
name is the org name SpaceX" (the s<hex> ids). The five below are the rest, plus
one rotation rename fix.

Builder handles: written only where the post carrying that exact share link is
authored by that handle and a second source agrees. Big Tony and Pulse both have
the post expanded with fxtwitter and the body shown to carry the exact share id.
CYBERCAB Fund Desk, Vacation Planner and Settlement Scout have no source post, so
the creator is recorded name-only (or empty) rather than guessed.

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
        'slug': 'big-tony',
        'name': 'Big Tony',
        'builder': {'name': 'Arizoft Games', 'x': 'arizoftgames'},
        'tagline': 'Escalation bot for unhonoured cancellations, surprise charges and warranty runarounds.',
        'description': 'An escalation bot for bad customer service. It takes on cancellations that were not honoured, charges that appear from nowhere, retention traps, fraud cleanups and warranty runarounds, builds the case, drafts firm messages for you to approve, and keeps following up until a real person settles it.',
        'category': 'money',
        'url': 'https://x.ai/bot/hBo0iWrkgWTueZe1TyGhm',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/arizoftgames/status/2103620479768789351',
    },
    {
        'slug': 'pulse-4',
        'name': 'Pulse',
        'builder': {'name': 'Fariborz Baghaei Naeini', 'x': 'FariborzBaghaei'},
        'tagline': 'Reads gym snaps, meal labels and calendar shots and returns a work and health balance plan.',
        'description': 'A vision-first coach for work and health balance. Drop in gym photos, meal labels and calendar screenshots and it returns a green, amber or red plan each morning and evening, plus a Friday wrap. Times follow your timezone, it reports readable facts only, and it drafts rather than acts.',
        'category': 'life',
        'url': 'https://x.ai/bot/nkmFntyGYALNwmUBMXCWj',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/FariborzBaghaei/status/2099902191284719664',
    },
    {
        'slug': 'settlement-scout',
        'name': 'Settlement Scout',
        'builder': {'name': '', 'x': ''},
        'tagline': 'Tracks class-action settlements and refunds you qualify for, with deadline reminders.',
        'description': 'Tracks payouts you can actually claim, including class-action settlements and overdue refunds. It briefs you on verified new ones, warns you before a deadline passes, and can sweep your inbox for settlement notices, with you approving every claim.',
        'category': 'money',
        'url': 'https://x.ai/bot/eSbC0EjdL3r6XOvB4lhOd',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': BEST,
    },
    {
        'slug': 'cybercab-fund-desk',
        'name': 'CYBERCAB Fund Desk',
        'builder': {'name': 'Branden Troutman', 'x': ''},
        'tagline': 'Rules-based crypto spot desk for BTC, ETH, SOL and DOGE on a personal Coinbase account.',
        'description': 'An hourly spot trading desk for BTC, ETH, SOL and DOGE on your own Coinbase account, published with hard risk limits: 25% maximum per trade, three trades a day and a 12% daily stop. Built for small, rules-based crypto trading. Not financial advice.',
        'category': 'money',
        'url': 'https://x.ai/bot/4AYUWc2XcQ64qluMXPV8l',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': BEST,
    },
    {
        'slug': 'vacation-planner',
        'name': 'Vacation Planner',
        'builder': {'name': 'McDubleNOpickle', 'x': ''},
        'tagline': 'Plans holidays end to end, comparing flights and cruises and watching prices.',
        'description': 'Plans a holiday end to end: comparing flights and cruises, finding stays, building day-by-day itineraries, handling airport and port logistics, and watching prices until you are ready to book.',
        'category': 'life',
        'url': 'https://x.ai/bot/cr8KAg2sp0Nyam7-QF-jh',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': BEST,
    },
]

# Rotation fix: the live share record for this listing now carries the name "Jess".
RENAME = {'url_tail': 'Nmv2fCQEcQc3EHzVXJZKN', 'name': 'Jess'}


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
    renamed = []
    for b in bots:
        if b['url'].endswith(RENAME['url_tail']) and b['name'] != RENAME['name']:
            renamed.append((b['name'], RENAME['name']))
            b['name'] = RENAME['name']
    json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(BOTS, 'a', encoding='utf-8').write('\n')
    print(f"added {len(added)}: {added}")
    print(f"skipped (already present) {len(skipped)}: {skipped}")
    print(f"renamed: {renamed}")
    print(f"directory now {len(bots)} entries, {len({b['url'] for b in bots})} unique urls")


if __name__ == '__main__':
    main()
