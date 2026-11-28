import json, html, re

BOTS = '/root/grokbothq/content/bots.json'
CANDS = '/root/grokbothq/ops/scout-candidates.json'
NOW = '2026-11-28 17:17 IST'
DATE = '2026-11-28'
SRC = 'https://botshelf.dev/new/'

verified = json.load(open('/root/grokbothq/ops/scout-verified-2026-11-28.json'))
entries = json.load(open('/root/.hermes/cache/scratch/entries.json'))

# The x.ai page and the listing disagree on who these belong to, so leave the handle empty.
NO_HANDLE = {'AKpIdEorRP_b1mhyYqrsc', 'ZAikMECAs4YnTeFJ-1Nyl', 'y5AZQ6GQ2PGzrTn_-jkLZ',
             'M-QNzE5X8KP7tf5T9lD_v'}

CATOK = {'money', 'sales', 'research', 'life', 'creative', 'engineering', 'productivity'}

bots = json.load(open(BOTS))
seen_url = {b['url'] for b in bots}
seen_slug = {b['slug'] for b in bots}

vids = {v['id'] for v in verified}
print('verified:', len(verified), '| entries:', len(entries))
print('verified without entry:', [v['id'] for v in verified if v['id'] not in entries])
print('entry without verified:', [k for k in entries if k not in vids])

added = []
for v in verified:
    bid = v['id']
    e = entries.get(bid)
    if not e:
        continue
    url = 'https://x.ai/bot/' + bid
    tag, desc, slug, cat = e['tag'], e['desc'], e['slug'], e['cat']
    problems = []
    if slug in seen_slug:
        problems.append('slug taken')
    if url in seen_url:
        problems.append('url listed')
    if len(tag) > 140:
        problems.append('tagline %d' % len(tag))
    if cat not in CATOK:
        problems.append('bad cat ' + cat)
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        problems.append('non-ascii slug')
    if problems:
        print('REJECT', slug, problems)
        continue
    bx = '' if bid in NO_HANDLE else e.get('bx', v['shelf_handle'])
    bname = e.get('bname') or v['page_sharer'] or v['shelf_creator'] or bx
    bots.append({
        'slug': slug, 'name': html.unescape(v['name']),
        'builder': {'name': bname, 'x': bx},
        'tagline': tag, 'description': desc, 'category': cat,
        'url': url, 'addedAt': DATE, 'status': 'published', 'source': SRC,
    })
    added.append((v, e, bname, bx))
    seen_url.add(url)
    seen_slug.add(slug)

json.dump(bots, open(BOTS, 'w'), indent=1, ensure_ascii=False)
print('bots.json now', len(bots), '| added', len(added))

cands = json.load(open(CANDS))
have = {c['bot_id'] for c in cands}
for v, e, bname, bx in added:
    if v['id'] in have:
        continue
    cands.append({
        'name': html.unescape(v['name']), 'bot_id': v['id'],
        'url': 'https://x.ai/bot/' + v['id'],
        'builder_x_handle': bx, 'builder_name': bname,
        'one_line_desc': e['tag'], 'source_post_url': SRC, 'found_at': NOW,
        'found_via': 'botshelf.dev/new (RSS + HTML, newest first) -> x.ai/bot page fetched 200, bot name and description confirmed',
        'status': 'verified, listed',
    })
cands = cands[-50:]
json.dump(cands, open(CANDS, 'w'), indent=1, ensure_ascii=False)
print('candidates now', len(cands))
