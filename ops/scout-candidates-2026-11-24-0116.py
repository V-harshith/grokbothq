#!/usr/bin/env python3
"""Record the 2026-11-24 01:16 IST scout pass in ops/scout-candidates.json (cap 50 newest)."""
import json

P = 'ops/scout-candidates.json'
FOUND = '2026-11-24 01:16 IST'
VIA = ('grok-bot.directory embedded listing JSON (submittedAt after the 2026-11-23 19:06 IST pass) '
       '-> x.ai/bot page fetched 200, botName + sharerName + description read from the page')

LISTED = [
    ('GitHub Cyber Trends', 'BHSBQQpDMOdUbG9xShpfJ', 'engineering'),
    ('Landlord Liability Incident Reporter', 'x_uqH3XjwPWzweIYuSoqP', 'money'),
    ('Automatic Scam/Fake Account Blocker', 'nTKYnoa_YXxj1wY7PA0Me', 'productivity'),
    ('Health Master Coach', 'a66RfgxnNpCfH3PTUsN8e', 'life'),
    ('My X Family', 'pTNOZAFpLvRSIuxxSmO7C', 'creative'),
    ('Crisis Support Guide', 'yHpOpnKCYx6tHMzx3f532', 'life'),
    ('Vintage Cookbooks', 'fdMyvb4eBJvQeFMeiq4Uu', 'life'),
    ('Doomsday Library Updater', 'JKsT95KRynua4YyATH5s9', 'life'),
    ('WhatsApp', 'kguveFbl4okkrVP-zNd1R', 'productivity'),
    ('Black Friday Deals 2026', 'kbsa5SJT80eGxs_MZHpWh', 'money'),
    ('Fantasy Football Manager', '93Kfl8BxhEbyu46Hl72Br', 'life'),
    ('Grocery Price Checker', 'ii7JO2xu79PtHoh5u8JGD', 'life'),
    ('Repo Analytics', '7tJda9jNms9sfX_44jcvC', 'engineering'),
    ('SARS Tax Desk', 'ieM-uFUYzIfaXgTxegoy1', 'money'),
    ('Search The Engine Optimizer', 'dHwbHyC4p0qHYDgD81Jtd', 'sales'),
    ('Play Store', 'bkQSw1ERgIz4ezsYaa6bc', 'engineering'),
    ('Air Bnb', 'h3Cwu4bi6nPFeWhkDShef', 'money'),
    ("Hershey's GrokBot Template", 'PRVrTDS3zWFma5elzxCA4', 'productivity'),
    ('Small Business Front Desk', 'tC8l2MFU63LYuY5d24NX3', 'sales'),
    ('Feature Ranker', 'Z9P_YTZh-DGTxkm4JrLho', 'productivity'),
    ('Funnel Judge', 'rr145N1wHkg0WDdI2jcRO', 'sales'),
    ('Apt Hunt', 'bP7MAaVMcYE0mRAEB2ZL8', 'life'),
    ('Tender Desk', 'VaKKXFX0bgBrClGeC3rqt', 'sales'),
    ('Rabbit Hole: Daily Curiosity Dispatch', 'SGCmHo7YzUE7VMBEWKpkW', 'research'),
    ('Darkroom: Local Image Workflow Builder', 'daE8wILcEk1t9I6FGFhPm', 'creative'),
    ('Imagine Director', 'ytoSaITVXRTFST2tJfs5c', 'creative'),
    ('Clapback Desk', 'L_8Prn7I-rUqur6BLor33', 'sales'),
    ('Scriptorium', 'vOTCtIDXGcyTbvS-y-CE8', 'creative'),
    ('Viral Oracle', '6y1Eep8vR6PzsIAbOh5Ee', 'sales'),
    ('Pass Mark', 'K2YOYjg6dbyHguJbs_KsK', 'productivity'),
]

REJECTED = [
    ('Spam-Call Scrubber', 'MLJr7RXJx36mYaV2huL3-', 'Kevin McDonald',
     'rejected: same job as three listed Spam-Call Scrubber builds (fUj6TYhiW_cjtzWvbsFgz, '
     'q6EUVmvVIkVZG4PB0bnG1, Z-1lj3U4-IdLhvH-As2vc) — find your number on data brokers, '
     'file the opt-outs, finish the confirmations, re-check on a schedule'),
    ('VA Claims Helper', 'E-QnTP06ULAY9iZzBJXYE', 'X News Network',
     'rejected: same job as listed VA Claims Helper (Antilitist, x.ai/bot/RVEJz3GxUXU_oLysEUCMA) '
     '— near-identical scope: organise claims, write statements, gather records, track deadlines'),
    ('Byline', 'BvfIfl5GA0xeYsMJG8-Bl', 'Joseph Gaither',
     'rejected: same name and same job as listed Byline (Paul McClelland, x.ai/bot/jZJaBRLyctngU0f1gmq0z) '
     '— a sourced long-form article writer; output format differs, the job does not'),
]

cands = json.load(open(P))
for name, bid, cat in LISTED:
    cands.append({'name': name, 'bot_id': bid, 'url': f'https://x.ai/bot/{bid}',
                  'builder_x_handle': '', 'one_line_desc': '', 'source_post_url': '',
                  'category': cat, 'found_at': FOUND, 'found_via': VIA,
                  'status': 'verified, listed'})
for name, bid, builder, reason in REJECTED:
    cands.append({'name': name, 'bot_id': bid, 'url': f'https://x.ai/bot/{bid}',
                  'builder_x_handle': '', 'builder_name': builder, 'one_line_desc': '',
                  'source_post_url': '', 'found_at': FOUND,
                  'found_via': 'x.ai/bot page fetched 200, botName + sharerName confirmed',
                  'status': reason})

cands = cands[-50:]
json.dump(cands, open(P, 'w'), indent=1, ensure_ascii=False)
open(P, 'a').write('\n')
print('candidates now', len(cands))