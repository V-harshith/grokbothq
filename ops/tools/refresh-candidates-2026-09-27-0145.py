#!/usr/bin/env python3
"""Refresh ops/scout-candidates.json for the 2026-09-27 01:45 IST pass (cap 50, newest kept)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'ops', 'scout-candidates.json')
FOUND = '2026-09-27T01:45:00+05:30'

# (name, bot_id, handle, one-line desc, source / provenance, status)
NEW = [
    ('Big Tony', 'hBo0iWrkgWTueZe1TyGhm', 'arizoftgames',
     'Escalation bot for unhonoured cancellations, surprise charges and warranty runarounds; drafts firm messages you approve.',
     'https://x.com/arizoftgames/status/2103620479768789351',
     'added to directory in ops/scout-pending (handle from the post, which carries this exact share id, plus both catalogues)'),
    ('Pulse', 'nkmFntyGYALNwmUBMXCWj', 'FariborzBaghaei',
     'Reads gym snaps, meal labels and calendar shots and returns a work and health balance plan morning and evening.',
     'https://x.com/FariborzBaghaei/status/2099902191284719664',
     'added to directory in ops/scout-pending as pulse-4 (name collides with three listed bots); handle from the post, which carries this exact share id, plus both catalogues'),
    ('Settlement Scout', 'eSbC0EjdL3r6XOvB4lhOd', '',
     'Tracks class-action settlements and refunds you qualify for, with deadline reminders and an optional inbox sweep.',
     'https://grokbots.best',
     'added to directory in ops/scout-pending (handle held: the platform display name is the machine-ish string "cokeandrice.akita.algo | Folks Finance" and no source post carries the link)'),
    ('CYBERCAB Fund Desk', '4AYUWc2XcQ64qluMXPV8l', '',
     'Rules-based crypto spot desk for BTC, ETH, SOL and DOGE on a personal Coinbase account with hard risk limits.',
     'https://grokbots.best',
     'added to directory in ops/scout-pending (handle held: catalogues name BrandenSeth; the platform sharer reads "Branden Troutman", which is not a second source agreeing)'),
    ('Vacation Planner', 'cr8KAg2sp0Nyam7-QF-jh', '',
     'Plans holidays end to end, comparing flights and cruises and watching prices until you are ready to book.',
     'https://grokbots.best',
     'added to directory in ops/scout-pending (link in grokbots.best, which calls it Travel Agent; the platform record is authoritative for the name)'),
]

HELD = [
    ('Critique', 'Dkl9wzI9FCt4EhqTHfsk2', '',
     'Still held: the share record carries the literal placeholder description "$3d" and no sharerName.',
     'https://x.com/TNVOLMAN/status/2103815860079198470', 'held: placeholder description on the share record'),
    ('Premarket Desk · 盘前早报', 'GuhaTzThKQG2MKJyHoREx', '',
     'Still held: the share record carries the literal placeholder description "$3d".',
     'https://x.com/alanchen/status/2103697141852151862', 'held: placeholder description on the share record'),
    ('Elon', 'skVoYDfnNUPqUYIxkjXJK', 'darke_mike6767',
     'First-principles sparring partner for hard-tech bets; refuses celebrity impersonation.',
     'https://github.com/cs68614-hash/awesome-grokbot-templates',
     'held: persona of a named individual (standing hold class); live with name and description'),
    ('Elongated Musketeer', 'cxUln0vqOPK7V3RccS0nm', 'egcbatt',
     'Elon Musk personality proxy: first-principles framing, blunt scoreboards, high-agency routines.',
     'https://github.com/cs68614-hash/awesome-grokbot-templates',
     'held: persona of a named individual (standing hold class); live with name and description'),
    ('Elon Musk (Algorithm & constraint)', 'QCwGPAlho0dBvBds_IOWF', 'merirand',
     'Weekly constraint finder that runs a question, delete, simplify, accelerate, automate loop.',
     'https://x.com/merirand/status/2100106954039582867',
     'held: persona of a named individual (standing hold class); live with name and description'),
    ('B', 'Wj3E3oow1J4gjwK4E2vNy', 'BillBuglin',
     'Publishing partner for an off-grid memoir series: manuscript cleanup, covers, KDP packaging, Audible prep.',
     'https://github.com/majiayu000/awesome-grok-bot',
     'held: the share record botName is a single letter, so the card has no usable display name'),
    ('anew', 'qtuoVRf5etpEVPNA29i7H', 'round',
     'Two-word placeholder description ("free webpages") on an otherwise live record.',
     'https://x.com/round/status/2101446607937888535',
     'held: placeholder-quality description, same class as the "$3d" holds'),
]

REJECTED = [
    ('empty botName on a 200', ['4jtnk5wsk0UMpDSNqG4Oc', 'Pa8G-Ldh5jU_jozWEu2Cs',
                                'Uy2oK9854UViaiO0rQ6nC', 'hEmSUvWxccmfAVDGri1R8'],
     'HTTP 200 with no share record: draft or team-only templates. Not queued.'),
    ('404 from a catalogue link', ['5eY-ne8zTXfklIhdOoeAm', 'D5A4QbXMACLWWokY4r3i4',
                                   'Kn0qDWAH3LrNZHhllpPhW', 'MqV14jluu59Fvlj1INiLk',
                                   'QhfOU5SJ60U8g2x2pUFcT', 'evB30VVYLfCGPxCdKoAuX',
                                   'fbfJZmVF5oHghV8XMm2', 'fSBU34VR0gqteP3IOAnr8',
                                   'oowzVaiKyse9a1wwCmHtK4', 'pRoDOS3PHZI7JE-Mn4hb6',
                                   'zKmuIjjZJmPOpwkuaCgIj'],
     'Catalogue entry points at an id that now 404s. Not queued.'),
    ('blank template', ['MT6acytP70wHR526vPvM3'],
     'Share record description is the generic "Use this template to create a new bot". Not queued.'),
    ('re-share of a listed bot', ['4mOGY7Nd_mRvrwZYec4Jq', 'EQgLIMO5Q_sVk3IM9EQbZ',
                                  'wOE4e95HNxhSbrzyLkSI-', 'WJc0G06lrr_H9OEyQ8Ijl',
                                  'VSO9GRfDreEu2ZiXwwZB_'],
     'Second share id for a bot already listed (The List, Full-Spectrum Law Firm OS, Tradbot, '
     'Fantasy Football Manager, Optima by TOATspace). No twin added.'),
]


def main():
    cands = json.load(open(CAND, encoding='utf-8'))
    have = {c['bot_id'] for c in cands}
    fresh = []
    for name, bid, handle, desc, src, status in NEW + HELD:
        if bid in have:
            continue
        fresh.append({
            'name': name,
            'bot_id': bid,
            'url': f'https://x.ai/bot/{bid}',
            'builder_x_handle': handle,
            'one_line_desc': desc,
            'source_post_url': src,
            'found_at': FOUND,
            'status': status,
        })
    out = fresh + cands
    out.sort(key=lambda c: c.get('found_at', ''), reverse=True)
    out = out[:50]
    json.dump(out, open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(CAND, 'a', encoding='utf-8').write('\n')
    trash = os.path.join(os.path.dirname(CAND), 'scout-rejects-2026-09-27-0145.json')
    json.dump([{'class': c, 'ids': i, 'reason': r} for c, i, r in REJECTED],
              open(trash, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(trash, 'a', encoding='utf-8').write('\n')
    print(f"candidates now {len(out)} (added {len(fresh)} fresh, cap 50 newest)")
    print(f"rejects written: {trash}")


if __name__ == '__main__':
    main()
