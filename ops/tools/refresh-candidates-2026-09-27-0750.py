#!/usr/bin/env python3
"""Refresh ops/scout-candidates.json for the 2026-09-27 07:50 IST pass (cap 50).

The 36 additions are read straight out of the pass's import script so the two
files can never drift. Holds are appended with their reason.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAND = os.path.join(ROOT, 'ops', 'scout-candidates.json')
IMP = os.path.join(ROOT, 'ops', 'tools', 'import-scout-pass-2026-09-27-0750.py')
FOUND = '2026-09-27T07:50:00+05:30'

HANDLE_NOTE = ('handle from the post carrying this exact share id plus grokbots.best '
               'naming the same account')
HANDLE_NOTE_RECORD = ('handle from the post carrying this exact share id; the platform '
                      'share record names the same person')
NAME_ONLY = ('listed name-only: the author of the post that carries this share id and the '
             'platform share record do not agree')

HELD = [
    ('Critique', 'Dkl9wzI9FCt4EhqTHfsk2', '',
     'Still held: the share record carries the literal placeholder description "$3d" and no sharerName.',
     'https://x.com/TNVOLMAN/status/2103815860079198470',
     'held: placeholder description on the share record (verified live again this pass)'),
]


def main():
    spec = importlib.util.spec_from_file_location('imp', IMP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fresh = []
    for b in mod.NEW:
        if b['builder'].get('x'):
            note = HANDLE_NOTE if b['slug'] in (
                '3-day-notice-validator', 'it-department-lead', 'calendar-liftoff', 'quill',
                'scriptsprint', 'solopreneur-chief-of-staff', 'mamboitalianobot', 'shawn',
                'handyman', 'pal', 'brew-what-you-got', 'ai-security-advisor',
                'the-box-of-names') else HANDLE_NOTE_RECORD
        else:
            note = NAME_ONLY
        fresh.append({
            'name': b['name'],
            'bot_id': b['url'].rsplit('/', 1)[-1],
            'url': b['url'],
            'builder_x_handle': b['builder'].get('x', ''),
            'one_line_desc': b['tagline'],
            'source_post_url': b['source'],
            'found_at': FOUND,
            'status': f"added to directory in ops/scout-pending ({note})",
        })
    for name, bid, handle, desc, src, status in HELD:
        fresh.append({
            'name': name, 'bot_id': bid, 'url': f'https://x.ai/bot/{bid}',
            'builder_x_handle': handle, 'one_line_desc': desc,
            'source_post_url': src, 'found_at': FOUND, 'status': status,
        })
    cands = json.load(open(CAND, encoding='utf-8'))
    have = {c['bot_id'] for c in cands}
    added = [c for c in fresh if c['bot_id'] not in have]
    out = (added + cands)[:50]
    out.sort(key=lambda c: c.get('found_at', ''), reverse=True)
    out = out[:50]
    json.dump(out, open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(CAND, 'a', encoding='utf-8').write('\n')
    print(f"candidates file: {len(out)} entries (added {len(added)} fresh, cap 50)")


if __name__ == '__main__':
    main()
