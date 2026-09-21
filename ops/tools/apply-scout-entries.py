#!/usr/bin/env python3
"""Apply a scout run's verified entries to content/bots.json + ops/scout-candidates.json.

Usage: apply-scout-entries.py /tmp/new_entries.json [--dead /tmp/dead.json]
Guards: refuses duplicate url/slug against the file it writes.
"""
import json, sys, datetime

entries_path = sys.argv[1]
dead_path = None
if '--dead' in sys.argv:
    dead_path = sys.argv[sys.argv.index('--dead') + 1]

BOTS = 'content/bots.json'
CANDS = 'ops/scout-candidates.json'

bots = json.load(open(BOTS))
if isinstance(bots, dict):
    bots = bots['bots']

existing_urls = {b['url'].rstrip('/') for b in bots}
existing_slugs = {b['slug'] for b in bots}
new = json.load(open(entries_path))

added, skipped = [], []
for e in new:
    if e['url'].rstrip('/') in existing_urls or e['slug'] in existing_slugs:
        skipped.append(e['slug'])
        continue
    bots.append(e)
    existing_urls.add(e['url'].rstrip('/'))
    existing_slugs.add(e['slug'])
    added.append(e)

json.dump(bots, open(BOTS, 'w'), indent=2, ensure_ascii=False)
open(BOTS, 'a').write('\n')

now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
cands = json.load(open(CANDS))
if not isinstance(cands, list):
    cands = cands.get('candidates', [])
cand_urls = {c.get('url') for c in cands}
for e in added:
    if e['url'] in cand_urls:
        continue
    cands.append({
        'name': f"{e['name']} by {e['builder']['name']}".strip(),
        'bot_id': e['url'].rsplit('/', 1)[-1],
        'url': e['url'],
        'builder_x_handle': e['builder']['x'] or None,
        'one_line_desc': e['tagline'],
        'source_post_url': e.get('source'),
        'found_at': now,
        'stage': 'verified+shipped',
    })
for d in (json.load(open(dead_path)) if dead_path else []):
    if any(c.get('bot_id') == d['bot_id'] for c in cands):
        continue
    cands.append({
        'name': d.get('name') or '',
        'bot_id': d['bot_id'],
        'url': f"https://x.ai/bot/{d['bot_id']}",
        'builder_x_handle': d.get('handle'),
        'one_line_desc': d.get('desc', '')[:160],
        'source_post_url': d.get('post'),
        'found_at': now,
        'stage': 'rejected',
        'reason': f"share page returned HTTP {d['code']} on live check",
    })
cands = cands[-50:]
json.dump(cands, open(CANDS, 'w'), indent=1, ensure_ascii=False)

print(f'added {len(added)} bots (total {len(bots)}), skipped dupes {len(skipped)}, candidates file {len(cands)}')
for s in skipped:
    print('  skip-dupe:', s)
