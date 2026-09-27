#!/usr/bin/env python3
"""Refresh ops/scout-candidates.json and write the 2026-09-27 14:00 IST report.

Candidates file: newest 50 rows only. This pass's rows go on top (the 20 that
went into content/bots.json plus the notable holds and rejects), then the older
rows follow until the cap is reached.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'ops', 'scout-candidates.json')
REPORT = os.path.join(ROOT, 'ops', 'scout-report-2026-09-27-1400.json')
REJECTS = os.path.join(ROOT, 'ops', 'scout-rejects-2026-09-27-1400.json')
FOUND = '2026-09-27T14:00:00+05:30'
ADDED_STATUS = 'verified live (200 + share record with botName and a real description), added to content/bots.json on ops/scout-pending'
TPLDESC = ('grokbot-templates.com/api/templates - free JSON endpoint; it serves one fixed 48-item page '
           '(identical bytes on 20 different offset requests). Handle taken only where the aggregator\'s '
           'twitterHandle and the x.ai share record\'s sharerName agree (that handle\'s display name checked free '
           'via api.fxtwitter.com/HANDLE); otherwise name-only.')

NEW_CANDIDATES = [
    ('SEO Content Desk (seodraft)', 'OkT4Dbjy4xVf7oVBCr8hL', 'chorch_md',
     'SEO content desk: topics from real search volume, drafts from your own evidence, filler stripped before it ships.',
     'https://x.com/chorch_md',
     ADDED_STATUS + '; handle corroborated by api.fxtwitter.com/chorch_md (display name "Chorch" = the share record sharerName). The feed source is the creator profile, not a post.'),
    ('フォーム優先アウトバウンド', '-4fEgwVFAm8w_ULi4pjmC', '',
     'Form-first B2B outreach for Japan: copy gate, daily prep, owner-GO sends, CRM logging, weekly PDCA.',
     'https://x.com/isle_claude/status/2103699353751969828',
     ADDED_STATUS + '; name-only - the post author (isle_claude) and the share record sharer (直人 島) do not agree, so no handle was written.'),
    ('Grok Bot', 'MT6acytP70wHR526vPvM3', 'sammya_sh',
     'Investment research teammate: research, rank and one clear pick, plus a weekly watch brief.',
     'https://x.com/sammya_sh/status/2102971805292167403',
     ADDED_STATUS + '; the post is the builder\'s own ("I built a Grok Bot that turns stock research into a decision") and its body carries this exact share id. Directory name is the live record name, which is generic - it is a fifth shareable row on the storefront, not a re-share of grok-bot-2 (different share id, different description).'),
    ('Forge Coach', 'ZBDynmT5k_WrRqQwoxdrI', 'CoffeeNGrit',
     'Daily workout builder from a short questionnaire on age, fitness, gear and space.',
     'https://x.com/CoffeeNGrit/status/2104045388210508129',
     ADDED_STATUS + '; handle taken because the share record sharer "Coffee and Grit" is the display name of the author of that post (the post body carries the sister bot PFP Studio\'s share id, not this one).'),
    ('PFP Studio', 'EQbigdwH3pEmkYcsbgidx', 'CoffeeNGrit',
     'Three profile pictures from one photo and a named style, then edits on your favourite.',
     'https://x.com/CoffeeNGrit/status/2104045388210508129',
     ADDED_STATUS + '; post body carries this exact share id and is authored by the same account the share record names.'),
    ('Agent Mail', 'j9Cm3GKLDCptPwwxZWbbD', 'JJEnglert',
     'Gives your bot an AgentMail inbox, learns your voice from your outbox, triages the noise.',
     TPLDESC,
     ADDED_STATUS),
    ('Thailand Visa Desk', 'zAzTVZRdvW9AK9okGihzU', 'danhogberg',
     'Thai immigration deadline tracker (90-day reports, TM30, re-entry, TDAC, renewals) with official sources.',
     TPLDESC,
     ADDED_STATUS),
    ('The Coder', 'eWee2PsTChAwOGEKpKpT_', 'ChristieGr55447',
     'Builds and fixes your app, keeps terms/privacy/how-to pages current, security-tests each release.',
     TPLDESC,
     ADDED_STATUS + '; api.fxtwitter.com/ChristieGr55447 is 404, so the handle rests on the aggregator claim plus the name it encodes matching the share record sharer "Christie Groenewald".'),
    ('Time Back Starter', 'JX0GlyQa_XFKC_b8dkAXM', 'AdventureNLearn',
     'Onboarding bot: sets up your first helper bots and one routine in a single sitting.',
     TPLDESC,
     ADDED_STATUS),
    ('Travel Specialist', 'xG8090ZuddD1vqrDdeTHZ', 'ArthurMacwaters',
     'End-to-end travel desk: flights, stays, ground transport, reservations, working links.',
     TPLDESC,
     ADDED_STATUS),
    ('UniFi Protect Alerts', 't9-UluNtR8-sZdrr_bxQU', '',
     'Emails you only for camera events that matter at your entrances; read-only against Protect.',
     TPLDESC,
     ADDED_STATUS + '; name-only - aggregator handle atuor (404 on the profile check) does not match the share record sharer "Matt Routa".'),
    ('Unreal Engine C++ Coder', 'k0jvhLXGv5AAjh6ZxfAAd', '',
     'Writes, fixes and reviews Unreal Engine C++ gameplay code inside your project.',
     TPLDESC,
     ADDED_STATUS + '; name-only - aggregator handle binxdonald resolves to display name "GraveBelt Alpha", which does not match the share record sharer "Binxius"; builder.name is the share record name.'),
    ('Videofy', '6_kAMXqIRrlhdolwzF0x-', '',
     'Remakes an X video in Grok Imagine, beat-synced, lookbook style.',
     TPLDESC,
     ADDED_STATUS + '; name-only - aggregator handle quobetah resolves to "Gerald Baria", which does not match the share record sharer "G Musk".'),
    ('What’s Up Tonight Bot', '5vI-rX7fZpwF0hP5GI2VE', 'stargazer_tim',
     'Nightly stargazing brief: go/no-go, clouds, Moon, planets, ISS, best targets.',
     TPLDESC,
     ADDED_STATUS + '; handle corroborated by api.fxtwitter.com/stargazer_tim (display name "Stargazer Tim", first name matches the share record sharer "Tim Mullin").'),
    ('Wikipedia Watch Bot', 'W_zh1KmptsmuKgl8zz3qp', 'phillipstewart',
     'Summarises what changed on the Wikipedia articles you watch, read from the real diffs.',
     TPLDESC,
     ADDED_STATUS),
    ('X Creator', '6mKW38QZDoaNq1SQxu_PQ', 'cao282828',
     'Runs an X account: sourced news, threads and polls on a schedule, replies to grow.',
     TPLDESC,
     ADDED_STATUS),
    ('X Creator Pulse Bot', '-xm4yCbgrveayEQBJXI3_', '',
     'Tracks your X account against a goal you set with real dated numbers; read-only.',
     TPLDESC,
     ADDED_STATUS + '; name-only - aggregator handle wrapmoney resolves to "Magnus", which does not match the share record sharer "Jason Doty".'),
    ('X Financial Scanner', 'e3jmMweGAwbD4JlUCzHXy', 'DennisW_15',
     'Read-only X markets desk: official accounts plus hot-stock sentiment, and what actually moved.',
     TPLDESC,
     ADDED_STATUS),
    ('Your Dyson Bot', 'XVfXkOFTGn-xN6C7drUHI', '',
     'Controls and reports on connected Dyson devices via MyDyson or Home Assistant.',
     TPLDESC,
     ADDED_STATUS + '; name-only - api.fxtwitter.com/ucdpilot is 404 and the aggregator handle does not match the share record sharer "Vijay Kandhalu".'),
    ('YouTube Clipper', 'H2qTNvMCgLSoL8FhSESlk', 'itsmechase',
     'Clips any YouTube video to an MP4 from a link and a timestamp, 4K where the source allows.',
     TPLDESC,
     ADDED_STATUS),
    ('Critique', 'Dkl9wzI9FCt4EhqTHfsk2', '',
     'Kill or pursue verdict on an X post or content idea.',
     'https://x.com/TNVOLMAN/status/2103815860079198470',
     'HELD (re-confirmed): live 200, but the share record description is still the literal placeholder "$3d". Same hold as the previous passes.'),
    ('Premarket Desk · 盘前早报', 'GuhaTzThKQG2MKJyHoREx', '',
     'Three-minute pre-open brief on a US watchlist.',
     'https://x.com/alanchen/status/2103697141852151862',
     'HELD (new): live 200, post carries this exact share id (18,013 views), but the share record description is the literal placeholder "$3d" - listed nowhere until the record carries a real description.'),
    ('The List', '4mOGY7Nd_mRvrwZYec4Jq', '',
     'GrokBotGod in-bot newsletter drops.',
     'https://grokbots.best',
     'SKIPPED as a re-share: live 200 and identical in substance to the already-listed the-list (U-eydTXJP7aN4W9dcUL5k, GrokBotGod, same tagline) - a second share id of the same bot, not a new one.'),
    ('Optima by TOATspace', 'VSO9GRfDreEu2ZiXwwZB_', '',
     'Forgetting desk: clears leftover rules so bots stop following killed jobs.',
     'https://x.com/TOATspace/status/2102970382378529216',
     'SKIPPED as a re-share: live 200, third share id of the Optima bot the directory already carries twice (optima-by-toatspace, optima-by-toatspace-2). The share record sharer is "gemini sub001", not the builder, so it adds nothing.'),
    ('VPS bot', 'KkQ9TOi5k9f2O60a-dx4T', '',
     'proxy VPS setup and tuning in Simplified Chinese.',
     TPLDESC,
     'REJECTED on policy, not on verification: live 200 with a real description, but it is a censorship-circumvention/proxy-VPS deployment helper. Left out on the AGENTS.md "when in doubt, leave it out" rule.'),
    ('Grok Bot (blank template shells)', 'hEmSUvWxccmfAVDGri1R8 / Uy2oK9854UViaiO0rQ6nC / Pa8G-Ldh5jU_jozWEu2Cs', '',
     'template placeholder text only.',
     'https://grokbots.best',
     'REJECTED: 200 but no share record (ownerType TEAM, empty botName) - the generic "Use this template to create a new bot or apply it to an existing bot" shell. Same reject class as every earlier pass.'),
    ('Moonshot', 'fSBU34VR0gqteP3IOAnr8', '',
     'Two tech podcasts digested into briefs.',
     'https://grokbot.dev',
     'REJECTED: the registry feed still carries this share id but the page is now 404 - dead id, not queued.'),
]


def main():
    rows = []
    for name, bid, handle, desc, source, status in NEW_CANDIDATES:
        rows.append({
            'name': name,
            'bot_id': bid,
            'url': 'https://x.ai/bot/' + bid.split(' ')[0],
            'builder_x_handle': handle,
            'one_line_desc': desc,
            'source_post_url': source,
            'found_at': FOUND,
            'status': status,
        })
    old = json.load(open(CAND, encoding='utf-8'))
    seen = {r['bot_id'] for r in rows}
    kept = [r for r in old if r.get('bot_id') not in seen]
    out = (rows + kept)[:50]
    json.dump(out, open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(CAND, 'a', encoding='utf-8').write('\n')
    print('candidates file: %d new rows, %d kept, capped at %d' % (len(rows), len(kept), len(out)))

    report = {
        'run': '2026-09-27 14:00 IST scout pass (cron 359022f62495)',
        'branch': 'ops/scout-pending',
        'push': True,
        'push_reason': '20 verified new bots (>= 3 gate met)',
        'method': ('Live fetch of every candidate x.ai/bot link with ops/tools/share_record_scan.py '
                   '(HTTP 200 + share record carrying botName and a real description). '
                   'Zero paid API calls: web_search + api.fxtwitter.com + curl/urllib only.'),
        'counts': {
            'candidates_screened': 27,
            'live_and_verifiable': 25,
            'added_to_directory': 20,
            'held': 4,
            'rejected': 4,
            'directory_after': 2265,
            'published_after': 2261,
            'builders_after': 1012,
        },
        'sources': {
            'grokbot.dev registry feed': ('1,292 items, generated_at 2026-09-27T05:08:20Z, newest added_at '
                                          '2026-09-26T23:56:52Z. Only one item landed since the 07:50 pass and it was '
                                          'already listed: the Sept 29 contest surge has paused.'),
            'grokbots.best': '1,020 records, 9 unseen share ids, 5 usable (4 were blank shells or the marketplace link).',
            'grokbot-templates.com/api/templates': ('new this pass - free JSON, 48 items per response and the response is '
                                                     'static (identical bytes on 20 offset requests across ~2 minutes), '
                                                     '16 of the 48 were new by share id and by name.'),
            'x.ai/bot/marketplace': ('rendered via web_extract: 62 Add links, 10 not listed by id, but all 10 are already '
                                     'listed under other share ids (Projects Manager, figma bro, tinkabot, Researchy, '
                                     'Nightly Audit Engineer, Tech Demos, Clip Bot, Credit Card Max, Sawyer Merritt Home '
                                     'Robots, last30days).'),
            'grokbotpulse.com': '10 links, none new.',
            'grokbots.page': '523 links, none new.',
            'x.ai/news': 'newest article is still Grok Bot customer support (Sep 22) - nothing to add to news.json.',
        },
        'rotation': {
            'sampled': 28,
            'live': 28,
            'dead': 0,
            'renamed': 0,
            'seed': 2026092714,
            'tool': 'ops/tools/rotation-2026-09-27-1400.py',
        },
        'marketing_signals_checked_with': 'api.fxtwitter.com per post (views/likes/bookmarks read live, not from search snippets)',
        'marketing_signals': [
            {'post': 'https://x.com/bot/status/2103936247995752705',
             'what': 'Grok Bot now connects to your finances (new Finance integration)',
             'stats': '22,164,366 views, 4,821 likes, 1,373 bookmarks (Sep 26)',
             'note': 'clears both thresholds (>100K views, >1K bookmarks) - first signal in three passes'},
            {'post': 'https://x.com/elonmusk/status/2103958249922072840',
             'what': 'Elon quote-posting the Finance integration',
             'stats': '22,309,284 views, 11,370 likes, 1,470 bookmarks (Sep 26)'},
            {'post': 'https://x.com/chrisparkX/status/2103872878328385990',
             'what': 'Grok Bot to XChat coming soon',
             'stats': '25,103 views, 442 likes, 26 bookmarks - below threshold, recorded for context only'},
        ],
        'blocked_sources': [
            'x.ai/bot/marketplace and the category pages ship no x.ai/bot links in the server HTML '
            '(client-rendered); web_extract was used instead.',
        ],
        'tools': ['ops/tools/fetch-registry-feed.py', 'ops/tools/share_record_scan.py',
                  'ops/tools/rotation-2026-09-27-1400.py',
                  'ops/tools/import-scout-pass-2026-09-27-1400.py',
                  'ops/tools/refresh-candidates-2026-09-27-1400.py'],
    }
    json.dump(report, open(REPORT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(REPORT, 'a', encoding='utf-8').write('\n')
    print('wrote %s' % os.path.basename(REPORT))

    rejects = {
        'run': '2026-09-27 14:00 IST scout pass',
        'rejected': [
            {'name': 'Grok Bot', 'bot_id': 'hEmSUvWxccmfAVDGri1R8',
             'reason': 'HTTP 200 but no share record: ownerType TEAM, empty botName, generic template shell.',
             'source': 'grokbots.best'},
            {'name': 'Grok Bot', 'bot_id': 'Uy2oK9854UViaiO0rQ6nC',
             'reason': 'HTTP 200 but no share record (same blank shell).',
             'source': 'grokbots.best'},
            {'name': 'Grok Bot', 'bot_id': 'Pa8G-Ldh5jU_jozWEu2Cs',
             'reason': 'HTTP 200 but no share record (same blank shell).',
             'source': 'grokbots.best'},
            {'name': 'Moonshot', 'bot_id': 'fSBU34VR0gqteP3IOAnr8',
             'reason': '404 - the registry feed still lists the share id but the page is gone.',
             'source': 'grokbot.dev registry feed'},
            {'name': 'VPS bot', 'bot_id': 'KkQ9TOi5k9f2O60a-dx4T',
             'reason': 'verified live but rejected on policy: proxy-VPS / censorship-circumvention deployment helper.',
             'source': 'grokbot-templates.com'},
        ],
        'held': [
            {'name': 'Critique', 'bot_id': 'Dkl9wzI9FCt4EhqTHfsk2',
             'reason': 'live, but the share record description is still the literal placeholder "$3d" (standing hold).'},
            {'name': 'Premarket Desk · 盘前早报', 'bot_id': 'GuhaTzThKQG2MKJyHoREx',
             'reason': 'live and carrying a real post (18,013 views), but the share record description is "$3d".'},
            {'name': 'The List', 'bot_id': '4mOGY7Nd_mRvrwZYec4Jq',
             'reason': 'second share id of the already-listed the-list.'},
            {'name': 'Optima by TOATspace', 'bot_id': 'VSO9GRfDreEu2ZiXwwZB_',
             'reason': 'third share id of an already-listed bot; sharer is not the builder.'},
            {'name': 'SpaceX-named first-party pack (56 rows)', 'bot_id': 's* share ids',
             'reason': 'standing hold - the platform display name on those rows is the org name "SpaceX", so attribution is not verifiable.'},
        ],
    }
    json.dump(rejects, open(REJECTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(REJECTS, 'a', encoding='utf-8').write('\n')
    print('wrote %s' % os.path.basename(REJECTS))


if __name__ == '__main__':
    main()
