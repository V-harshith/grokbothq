#!/usr/bin/env python3
"""Back-check: re-verify every id held in an ops record for a reason the reader bug
could have produced ("placeholder" description / "no share record"), then report
which of them are in fact live and listable.

The 07:00 pass flagged this gap and did not run it. Uses the authoritative reader.
"""
import glob
import json
import re
import importlib.util
import concurrent.futures

spec = importlib.util.spec_from_file_location('srs', '/root/grokbothq/ops/tools/share_record_scan.py')
srs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srs)

BAD = re.compile(r'no share record|placeholder|draft/team-only', re.I)
ID = re.compile(r'x\.ai/bot/([A-Za-z0-9_-]{10,})')

if __name__ == '__main__':
    listed = set(ID.findall(open('/root/grokbothq/content/bots.json', encoding='utf-8').read()))
    suspects = {}
    for path in glob.glob('/root/grokbothq/ops/*.json'):
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for m in re.finditer(r'x\.ai/bot/([A-Za-z0-9_-]{10,})', text):
            win = text[max(0, m.start() - 600):m.end() + 600]
            if BAD.search(win):
                suspects.setdefault(m.group(1), []).append(path.split('/')[-1])
    todo = {k: v for k, v in suspects.items() if k not in listed}
    print(f"suspect ids: {len(suspects)}, not already listed: {len(todo)}")
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(srs.fetch, k): k for k in todo}
        for f in concurrent.futures.as_completed(futs):
            out[futs[f]] = f.result()
    live = [k for k, v in out.items() if v.get('ok')]
    print(f"re-verified live now: {len(live)}")
    for k in sorted(live):
        v = out[k]
        print(json.dumps({'id': k, 'sharer': v.get('sharer'), 'name': v.get('name'),
                          'desc_len': len(v.get('desc') or ''), 'desc': v.get('desc'),
                          'cited_in': todo[k]}, ensure_ascii=False))
    for k, v in out.items():
        if not v.get('ok'):
            print(json.dumps({'id': k, 'still_not_ok': v.get('reason'), 'cited_in': todo[k]}, ensure_ascii=False))
