#!/usr/bin/env python3
"""Rotation sample for the 2026-09-27 14:00 IST pass.

Opens a deterministic rotation of existing published listings with the
authoritative reader (ops/tools/share_record_scan.py), reports dead links
(which get status: pending) and renamed listings (name corrected to the live
share record), and touches nothing else. Sample is seeded by the date so it
walks the directory over successive passes.
"""
import json
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, 'content', 'bots.json')
TOOL = os.path.join(ROOT, 'ops', 'tools', 'share_record_scan.py')
N = 28
SEED = 2026092714


def main():
    bots = json.load(open(BOTS, encoding='utf-8'))
    pool = [b for b in bots if b.get('status') == 'published'
            and b.get('addedAt') != '2026-09-27']
    rng = random.Random(SEED)
    sample = rng.sample(pool, N)
    ids = [b['url'].rsplit('/', 1)[-1] for b in sample]
    p = subprocess.run([sys.executable, TOOL] + ids, capture_output=True, text=True,
                       timeout=900)
    rows = {}
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith('{'):
            r = json.loads(line)
            rows[r['bot_id']] = r
    dead, renamed, ok = [], [], 0
    for b in sample:
        bid = b['url'].rsplit('/', 1)[-1]
        r = rows.get(bid)
        if not r:
            dead.append((b['slug'], 'no reader output'))
            continue
        if r['status'] != '200' or not r.get('ok'):
            dead.append((b['slug'], f"http {r['status']} / {r.get('reason')}"))
            continue
        ok += 1
        live = r.get('name')
        if live and live != b['name'] and b['name'].lower() != live.lower():
            renamed.append({'slug': b['slug'], 'was': b['name'], 'now': live,
                            'sharer': r.get('sharer')})
            b['name'] = live
    if dead:
        for slug, why in dead:
            for b in bots:
                if b['slug'] == slug:
                    b['status'] = 'pending'
                    b['pendingReason'] = f'rotation {SEED}: {why}'
    if dead or renamed:
        json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        open(BOTS, 'a', encoding='utf-8').write('\n')
    print(f"rotation sampled {len(sample)}: {ok} live, {len(dead)} dead, "
          f"{len(renamed)} renamed")
    print('dead:', dead)
    print('renamed:', json.dumps(renamed, ensure_ascii=False))


if __name__ == '__main__':
    main()
