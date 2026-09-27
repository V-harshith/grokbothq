#!/usr/bin/env python3
"""Refresh ops/scout-candidates.json for the 19:30 pass (cap 50, newest kept)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'ops', 'scout-candidates.json')
FOUND = '2026-09-26T19:30:00+05:30'

# (name, bot_id, handle, one-line desc, source post / provenance, status)
NEW = [
    ('Reply Desk', '8lLjBC7bXUqbfh-vLG9jf', 'lonzom10',
     'Drafts replies to customer emails, messages and public reviews for a local service business, for you to send.',
     'https://x.com/lonzom10/status/2103749418457681951', 'added to directory in ops/scout-pending'),
    ('Requirement Engineer Bot', '5KADFS8AIIDOlow5tS34Z', 'FishxCD',
     'Turns a project brief into a structured requirements spec another bot can implement and verify.',
     'https://x.com/FishxCD/status/2103810502510215640', 'added to directory in ops/scout-pending'),
    ('Apply Bot', '2GdkYgGlc91A6d6MPXCkZ', 'Kylebauer',
     'Finds live job descriptions, remaps your evidence onto each posting rubric and applies at volume with queue pacing.',
     'https://x.com/Kylebauer/status/2103765740642083259', 'added to directory in ops/scout-pending'),
    ('Teddy', '1CN_MjQ2E4oT3hnJXscGB', 'JackLocke',
     'Chief of staff bot: inbox triage, calendar, tasks and coordination of your other bots, draft-first.',
     'https://x.com/JackLocke/status/2103805162578231363', 'added to directory in ops/scout-pending'),
    ('Find an apartment with budget', '9iMoFiWKRlnobZbxxS8kx', '',
     'Searches budget apartments near your workplace, weighing price, commute time and local crime.',
     'https://x.com/TheAyoFrancis/status/2103780690395373997',
     'added to directory in ops/scout-pending (handle held: platform sharer "Ayomide Fagbohungbe" does not line up with post author @TheAyoFrancis)'),
    ('Researcher AI Desk', '89JF_2TtrVf27zelZ8pZ8', '',
     'Research operations desk with a live to-do, a morning surface and a schedule you set; mail is read draft-first.',
     'https://x.com/original_Tree/status/2103806334953230846',
     'added to directory in ops/scout-pending (handle held: platform sharer "David Anderson" does not line up with post author @original_Tree)'),
    ('Kids Daily Spark', 'Lpl_fDQ5Jhj2sfoCWy1Hf', 'HelloBenL',
     'One-page daily STEM brief per child: a real concept, a hook, a 30-second try-it and soft art.',
     'https://x.com/HelloBenL/status/2103753503596564871', 'added to directory in ops/scout-pending'),
    ('Travel Advisor', 'CO9aQ2BdGGHEJH0wXTGV7', 'thefit24couple',
     'Plans multi-day trips from live official sources and proposes reservations, never booking or paying itself.',
     'https://x.com/thefit24couple/status/2103779539235250191', 'added to directory in ops/scout-pending'),
    ('Airfield Electrical Bid Scout', 'PWBPqcCqUbEUPozXozRc3', 'thefit24couple',
     'Finds and qualifies public bids for airfield lighting, NAVAIDs, FAA fiber and underground electrical work.',
     'https://x.com/thefit24couple/status/2103777435087249670', 'added to directory in ops/scout-pending'),
    ('Thaw', 'CvO94wB4V27zmL1haDbQL', '',
     'Scores sample water pipes for 12-month failure risk with a synthetic-data random forest; a learning demo.',
     'https://x.com/thebytorsnowdog/status/2103743916964970548',
     'added to directory in ops/scout-pending (handle held: platform sharer "Ian Dunsmore" does not line up with post author @thebytorsnowdog)'),
    ('Fortnite Drop Brief', 'QNiJmH32K4YqAEafHRF__', 'IHybben',
     'Daily Fortnite briefing covering the shop, patches, downtime, events and labelled leaks.',
     'https://x.com/IHybben/status/2103780983459959139', 'added to directory in ops/scout-pending'),
    ('Construction Manager Bot', 'QrJpjStFV2WBIaI8wirO6', '',
     'Field-first construction manager for US civil work: site cards, photo-to-RFI drafts, spec and code checks.',
     'https://x.com/HenryBeagle808/status/2103749805625536556',
     'added to directory in ops/scout-pending (handle held: platform sharer "Wayne Higa" does not line up with post author @HenryBeagle808)'),
    ('Interview to Book / 故事成书', 'XuGcpLoS77HdZoupGOlnp', 'jackhu_bangzhu',
     'One question at a time, turning spoken or written answers into a printable memoir with a cover.',
     'https://x.com/jackhu_bangzhu/status/2103734020211442101', 'added to directory in ops/scout-pending'),
    ('每週公平分發代幣掃描', 'kO0E0KzOkpUnPJQLmzBFm', '',
     'Weekly scan of new fair-mint token launches: 0 to 10 scores against earlier breakout traits, scam checks, mailed report.',
     'https://x.com/slowbtc/status/2103802372984361061',
     'added to directory in ops/scout-pending (handle held: platform sharer "Allen Chien" does not line up with post author @slowbtc)'),
    ('Quant Backtest Lab · 量化回测台', 'TolT21zChD6bYj0ZEA7pE', 'jackhu_bangzhu',
     'Backtests trading rules on A-shares, US equities and crypto spot with costs included; research only.',
     'https://x.com/jackhu_bangzhu/status/2103739894090829964', 'added to directory in ops/scout-pending'),
    ('Running Coach', 'o4hvGfkH_LOiP0YbT22og', 'IHybben',
     'Reads Garmin run data, reviews each run and sets the next recovery-gated session.',
     'https://x.com/IHybben/status/2103818102014132424', 'added to directory in ops/scout-pending'),
    ('Volatile Stock Options', 'kuhoazDWLEsY-kXvHBwtU', 'KVTay316',
     'Screens volatile US call options across multiple sources for personal research, not advice.',
     'https://x.com/KVTay316/status/2103780405736587652', 'added to directory in ops/scout-pending'),
    ('Ship Desk', 'thMhD-rbJ0Osd274RGohH', '',
     'Promotes staging to production behind a locked tip, keeping checkout fail-closed until you flip go.',
     'https://x.com/usgworld/status/2103747605503041761',
     'added to directory in ops/scout-pending (handle held: platform sharer "Umashankar Gummadidala" does not line up with post author @usgworld)'),
    ('Higgins', 'pobs233eUgpZLtlxoyyEn', 'thefit24couple',
     'Evening and weekend concierge that finds plans and prepares bookings, but never books or pays.',
     'https://x.com/thefit24couple/status/2103780998437826823', 'added to directory in ops/scout-pending'),
    ('X Thread & Article Writer', 'xLeBNzgp0Z6IUGxyt8sj4', 'sigarellano',
     'Turns notes and links into X threads and articles in your own voice; drafts only.',
     'https://x.com/sigarellano/status/2103737235413860615',
     'added to directory in ops/scout-pending (handle from two aggregators + the post carrying the link; the platform share record has no sharerName)'),
    ('Vern', 'rDEpX2aSCERCaVJACxNz7', 'ahoop',
     'Private relationship CRM that reminds you of birthdays and overdue check-ins and never messages anyone.',
     'https://x.com/ahoop/status/2103809460972200282', 'added to directory in ops/scout-pending'),
    ('Grok Bot Tutorial', 'VBmzZaD3abMPl53kwWuYp', '',
     'A 20-lesson hands-on Grok Bot course with exercises and tips for new users.',
     'https://github.com/RongleCat/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('CodeFix Buddy', '-3H90YMhn2cE-CO1jj3-2', '',
     'Coding sidekick: paste an error for a fix, describe a build for working code, or ask for an explanation.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Pick Buddy', 'TVm2a-XMbS82AU0MMLyHq', '',
     'Scores 2 to 6 options on fit, cost, time, risk and upside, picks a winner and can plan the next steps.',
     'https://github.com/majiayu000/awesome-grok-bot', 'added to directory in ops/scout-pending'),
    ('Personalized Localized Name Gen', 'A5MrnZ1SGhd4yOX-ZlWBh', 'MarioSaputra',
     'Generates localized first and last names for a target country, in the local script where one exists.',
     'https://x.com/MarioSaputra/status/2103721921473077408', 'added to directory in ops/scout-pending'),
    ('Heckler', 'OkrPAOW9hkj4IGpOLrsGY', 'XploreFutureX',
     'Roasts your other bots real mistakes with a meme per roast, and each roast doubles as a verified fix list.',
     'https://x.com/XploreFutureX/status/2103727100842623465', 'added to directory in ops/scout-pending'),
    ('Repo Monkey', 'evdmG7ilYN01Nu4NBXPyQ', 'Keranik',
     'Turns GitHub notifications, pull requests and CI into a short list of what actually needs you.',
     'https://x.com/Keranik/status/2103723687920669124', 'added to directory in ops/scout-pending'),
    ('QA bot', 'lKQWoQAvYgg_7Bkg2R-m7', '',
     'Runs the acceptance checklist on a live deploy and reports pass or fail before you ship.',
     'https://x.ai/bot/marketplace',
     'added to directory in ops/scout-pending (marketplace row whose share link was previously unavailable; link now resolves)'),
    ('PM bot', 'FeeqMRMJr2jwixCROZcIh', '',
     'Writes the dated scope cut, what is in and what is out, and waits for your approval before engineering starts.',
     'https://x.ai/bot/marketplace',
     'added to directory in ops/scout-pending (marketplace row whose share link was previously unavailable; link now resolves)'),
    ('Engineering Lead', 'Ks3X7JpD-6I86s3zkJFRh', '',
     'Owns the loop from Cloud Agent splits to CI and review, pinging you only on blockers or done work.',
     'https://x.ai/bot/marketplace',
     'added to directory in ops/scout-pending (marketplace row; the marketplace record declares handle poteto but no second source agrees, so the handle is empty)'),
    ('Live Shorts Desk', 'r-Ctb7rwRVFOY-_p_T9eX', 'MadnessOfMouth',
     'Live show to YouTube Shorts desk with a locked checklist and a publish hold until you say go.',
     'https://x.com/MadnessOfMouth/status/2103720549146890590', 'added to directory in ops/scout-pending'),
]

HELD = [
    ('Critique', 'Dkl9wzI9FCt4EhqTHfsk2', '',
     'Platform share record carries the literal placeholder description "$3d" and no sharerName, so the listing cannot be verified.',
     'https://x.com/TNVOLMAN/status/2103815860079198470', 'held: placeholder description on the share record'),
    ('Premarket Desk · 盘前早报', 'GuhaTzThKQG2MKJyHoREx', '',
     'Platform share record carries the literal placeholder description "$3d", so the listing cannot be verified. The registry feed summary is not a substitute for the platform record.',
     'https://x.com/alanchen/status/2103697141852151862', 'held: placeholder description on the share record'),
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
    print(f"candidates now {len(out)} (added {len(fresh)} fresh, cap 50 newest)")


if __name__ == '__main__':
    main()
