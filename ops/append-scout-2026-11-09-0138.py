#!/usr/bin/env python3
"""Append scout-verified bots to content/bots.json (2026-11-09 01:38 IST run).

Every entry below was opened live at https://x.ai/bot/<id> and confirmed HTTP 200
with the bot name present on the page before queueing (see ops/scout-candidates.json).
Source: readmultiplex.com/grokbot-rocks directory crawl + x.ai pages.
"""
import json
import re

PATH = 'content/bots.json'
TODAY = '2026-11-09'

NEW = [
    dict(slug='bot-self-improvement', name='Bot Self Improvement',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Audits your Grok Bot usage export and ranks where the tokens actually go.',
         desc='Takes an export of your Grok Bot usage and works out which bots and runs spend the most, which ones keep repeating the same result, and which jobs one bot could own alone. Delivers a ranked fix list.',
         category='productivity',
         features=['Token use by bot and run', 'Repeated or idle runs flagged', 'Ranked fix list'],
         bot_id='9BHgJqRj-s38cp8vfMQUc',
         source='https://x.com/BrianRoemmele/status/2112249592133935133'),
    dict(slug='meal-ingredient-shopper', name='Meal Ingredient Shopper',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Turns a recipe into a scaled ingredient list and a cart you approve.',
         desc='Give it a recipe and the number of servings; it scales the quantities, groups the shopping into a list, and can build a grocery cart that only checks out after you approve it.',
         category='life',
         features=['Scales recipes to servings', 'Grouped shopping list', 'Cart needs your approval'],
         bot_id='zFlBJV-8p1LwP4xgleCwl',
         source='https://x.com/BrianRoemmele/status/2110174733660742018'),
    dict(slug='three-quotes', name='Three Quotes',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Writes a job spec, finds local pros, and collects three comparable quotes.',
         desc='Writes up the job so every tradesperson quotes the same scope, finds licensed local pros, calls them to check availability, and returns three quotes side by side.',
         category='life',
         features=['One scope for every pro', 'Licensed local pros', 'Quotes compared side by side'],
         bot_id='GNFPzVh1EezMS0JiNHgcr',
         source='https://x.com/BrianRoemmele/status/2117679311511761308'),
    dict(slug='attic-archivist', name='Attic Archivist',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Identifies old photos, tapes and records, with cited resale prices.',
         desc='For boxes of old records, photos, slides, tapes or home movies: it says what each item is, what it sells for with sources cited, and what is worth digitising rather than keeping.',
         category='life',
         features=['Item identification', 'Prices with citations', 'Digitise-or-keep call'],
         bot_id='EJ4VNEozcv5NsRl07pt9Z',
         source='https://x.com/BrianRoemmele/status/2117320396370530726'),
    dict(slug='bot-bodyguard', name='Bot Bodyguard',
         builder=('Brian Roemmele', ''),
         tagline='Weekly read-only audit of what each of your bots can reach and send.',
         desc='Checks every bot on the account for the data and tools it can reach, flags anything new or unusual since last week, and explains the risk in plain language. Read-only, so it changes nothing.',
         category='productivity',
         features=['Weekly access review', 'New and unusual access flagged', 'Read-only'],
         bot_id='abPHs-nvdICU7XiRDyrSg'),
    dict(slug='claim-denial-fighter', name='Claim Denial Fighter',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Decodes a denied insurance claim and drafts the appeal.',
         desc='Reads a denial letter and explanation of benefits, finds the appeal deadline, works out the stated reason for denial, and drafts an appeal letter for you to review and send.',
         category='life',
         features=['Denial letter and EOB decoded', 'Deadline tracked', 'Appeal drafted'],
         bot_id='6J_YPko7HNztETQzvBYM6',
         source='https://x.com/BrianRoemmele/status/2116951368829403569'),
    dict(slug='estate-settler', name='Estate Settler',
         builder=('Brian Roemmele', ''),
         tagline='One checklist and drafted letters for settling someone’s estate.',
         desc='After a death, it builds a single checklist with every deadline tracked and drafts the notifications and account-closing letters a family has to send, one step at a time.',
         category='life',
         features=['Deadlines tracked', 'Notifications drafted', 'Account closures listed'],
         bot_id='DaegPVp52kfKdmYoPQ3S7'),
    dict(slug='new-patient-booker', name='New Patient Booker',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Finds nearby doctors taking new patients and books once you say yes.',
         desc='Searches doctors and dentists near you who are accepting new patients, labels insurance network status as stated, shows reviews side by side, and books only with your approval.',
         category='life',
         features=['Accepts-new-patients filter', 'Insurance status labelled', 'Books only on approval'],
         bot_id='IhQTTIBBCNtx7qpFzQhgl',
         source='https://x.com/BrianRoemmele/status/2117679838903648616'),
    dict(slug='product-alert-bot', name='Product Alert Bot',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Watches one exact product spec at your chosen stores and pings on stock.',
         desc='Tracks a specific model, colour, size, storage and carrier at the stores you pick, then messages you the moment it is buyable for shipping or pickup.',
         category='life',
         features=['Exact spec matching', 'Chosen stores only', 'Stock alert'],
         bot_id='DhB7TMKfeP7Vx0mMr9Tjq',
         source='https://x.com/BrianRoemmele/status/2117767350493823204'),
    dict(slug='read-every-app', name='Read Every App',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Reads every app’s privacy policy and quotes the data-selling lines.',
         desc='Goes through the privacy policy and terms of each app on your phone, quotes the exact sentence where it reserves the right to sell, share or use your data, and drafts a deletion request.',
         category='productivity',
         features=['Policy and terms read', 'Exact clauses quoted', 'Deletion request drafted'],
         bot_id='cpzlb3uf_hY7BnAg0AEmc',
         source='https://x.com/brianroemmele/status/2117775975052386630'),
    dict(slug='warranty-registration-bot', name='Warranty & Registration Bot',
         builder=('Brian Roemmele', 'BrianRoemmele'),
         tagline='Finds the warranty or card benefit that covers a broken item.',
         desc='For something broken, damaged or stolen, it looks across product warranties, credit card purchase protection and home or auto insurance, then shows which cover applies and what to file.',
         category='life',
         features=['Warranty lookup', 'Card benefit check', 'Claim path shown'],
         bot_id='Z4GWGgi_gyDCAAiv05TsG',
         source='https://x.com/BrianRoemmele/status/2117765640484475173'),
    dict(slug='small-claims-complaint-filer', name='Small Claims & Complaint Filer',
         builder=('Brian Roemmele', ''),
         tagline='Walks an unresolved refund or repair dispute up to small claims.',
         desc='For people a business will not refund, repair, deliver for or answer: it steps from a demand letter to a regulator complaint to small claims paperwork, keeping dates and evidence in order.',
         category='life',
         features=['Demand letter drafted', 'Regulator complaint path', 'Small claims paperwork'],
         bot_id='-nyhSPkH9g1M8nq_PfWgG'),
    dict(slug='x-money-bill-pay-guard', name='X Money Bill Pay Guard',
         builder=('Brian Roemmele', ''),
         tagline='Reviews X Money charges and bills, and approves every payment with you.',
         desc='Reads your X Money account for duplicate or odd charges and upcoming bills, then asks you to approve each payment one by one. It states plainly that it is not a financial adviser.',
         category='money',
         features=['Duplicate charge check', 'Upcoming bills', 'Per-payment approval'],
         bot_id='10ZAtArrlz36Tr9WBSOy5'),
    dict(slug='trendlines-tutor', name='Trendlines Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Beginner-to-expert lessons on drawing and using trendlines.',
         desc='A structured chart-reading tutor for trendlines: a placement chat first, then lessons with check questions and quizzes, ending in a mastery exam. Progress is saved between sessions.',
         category='money',
         features=['Placement chat', 'Lessons and quizzes', 'Mastery exam'],
         bot_id='RU-UWYm0ky7HFmjanfL0s'),
    dict(slug='entry-triggers-tutor', name='Entry Triggers Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Structured lessons on entry triggers, from placement chat to final exam.',
         desc='Teaches entry triggers in order: a placement chat sets the starting level, lessons come with check questions and quizzes, and a final exam tests the whole sequence.',
         category='money',
         features=['Placement chat', 'Check questions and quizzes', 'Final exam'],
         bot_id='y2NuommHwkKelIcmh_ZQr'),
    dict(slug='support-resistance-tutor', name='Horizontal Support/Resistance Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Five graded lessons on horizontal support and resistance.',
         desc='Covers horizontal support and resistance from scratch: placement first, five lessons with exercises, quizzes after each one, and a mastery exam at the end.',
         category='money',
         features=['Five lessons', 'Exercises and quizzes', 'Mastery exam'],
         bot_id='-7gsVGAQDqia9emepeXrP'),
    dict(slug='market-structure-tutor', name='Market Structure Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Market structure lessons built on CryptoCred’s series, with two exams.',
         desc='A market structure tutor that follows CryptoCred’s teaching: five lessons with quizzes, exercises in between, and two exams. Levels adapt to how you answer the placement chat.',
         category='money',
         features=['Five lessons', 'Based on CryptoCred’s series', 'Two exams'],
         bot_id='SBYu4x-Rm_K0pgN7wapyR'),
    dict(slug='pattern-failure-tutor', name='Pattern Failure Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Teaches when chart patterns fail and what that signal means.',
         desc='A tutor for pattern failure: a placement chat sets the level, then lessons with check questions and quizzes, then a final exam on spotting a failed pattern early.',
         category='money',
         features=['Placement chat', 'Pattern-failure drills', 'Final exam'],
         bot_id='qzbgDGNJyp5Ef8SxZb1hk'),
    dict(slug='rsi-tutor', name='RSI Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Lessons on the Relative Strength Index up to a mastery exam.',
         desc='Teaches the Relative Strength Index from first principles: a placement chat, then lessons with check questions, quizzes and a mastery exam. Saves progress between sessions.',
         category='money',
         features=['Beginner to expert path', 'Lessons and quizzes', 'Mastery exam'],
         bot_id='OpxxnAarJDKsy00daqXnt'),
    dict(slug='top-down-approach-tutor', name='Top-Down Approach Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Teaches chart analysis from the higher timeframe down.',
         desc='A tutor for top-down chart analysis: it starts at the higher timeframe, works down through the lower ones, and checks each step with questions, quizzes and a final exam.',
         category='money',
         features=['Higher to lower timeframe', 'Check questions', 'Final exam'],
         bot_id='sYjpaSlOCVPlsAHL_Mu_j'),
    dict(slug='trade-management-tutor', name='Trade Management Tutor',
         builder=('Hoem Crypto', ''),
         tagline='Audits your own trade interventions and teaches management rules.',
         desc='A trade management tutor that also audits how you intervene in live trades, covers managing winners and losers and the rules around the Dead Zone, and runs to a mastery exam.',
         category='money',
         features=['Intervention audit', 'Winner and loser handling', 'Mastery exam'],
         bot_id='QmC5gbGLHexNCrlOh81Uv'),
    dict(slug='network-ned-office', name='Network Ned',
         builder=('James Harrison', ''),
         tagline='Plans the network for a small office, shop or church.',
         desc='A network design helper for small sites: it plans internet, Wi-Fi, switches, guest networks, cameras and backups, and lays the gear out in a setup someone can follow.',
         category='engineering',
         features=['Small-site network plan', 'Wi-Fi and switching layout', 'Guest and camera networks'],
         bot_id='qHJHrp64deGRRHLmMP0Ql'),
    dict(slug='legal-advisor-bot', name='Legal Advisor',
         builder=('XPixel', ''),
         tagline='Plain-English legal analysis for multi-jurisdiction questions.',
         desc='Takes legal questions that cross jurisdictions, spots the issues, explains them in plain English, and drafts letters or outlines a strategy with the next steps listed.',
         category='assistants',
         features=['Issue spotting', 'Plain-English analysis', 'Draft letters'],
         bot_id='YAGa694NcNPa_Aqh_cMCc'),
    dict(slug='builder-spec', name='Builder',
         builder=('Avid', ''),
         tagline='Builds software from a SPEC.md with tests and a written report.',
         desc='Works from a SPEC.md to build original software with open-source dependencies, adds automated tests, and hands back a test report. It waits for owner approval and never publishes on its own.',
         category='engineering',
         features=['SPEC.md driven', 'Automated tests', 'Test report and approval gate'],
         bot_id='iCKWgIWPwg2dZe0GUlsgI'),
    dict(slug='viral-autopsy', name='Viral Autopsy',
         builder=('painn', ''),
         tagline='Breaks down why posts go viral in your niche, daily.',
         desc='Watches what is going viral in your part of X, explains why each hook worked, and sends a short daily report. On request it writes hooks in your voice.',
         category='research',
         features=['Niche viral tracking', 'Hook breakdown', 'Daily report'],
         bot_id='H29yEjYY2CqbJFlklSDII'),
    dict(slug='animator-remotion', name='Animator',
         builder=('Nima Owji', ''),
         tagline='Builds multi-scene animated videos in code from a description.',
         desc='A motion graphics designer: describe an idea and it builds a story-driven multi-scene animation in Remotion, with Lottie elements and rendered video output.',
         category='creative',
         features=['Multi-scene animation', 'Remotion code output', 'Lottie support'],
         bot_id='Hp85sZKzJNjabj8hakjee'),
    dict(slug='beowulf-standup', name='Beowulf',
         builder=('HexTurtleGd', ''),
         tagline='One generalist bot for planning, building, research and operations.',
         desc='A single assistant billed as a standup ally: it plans, builds, checks, researches, creates and operates, and walks new owners through setup with its Standup Guide.',
         category='assistants',
         features=['Planning and building', 'Research and checks', 'Guided setup'],
         bot_id='aUWkVIzWbrNkJUtQctKcw'),
]


def main():
    bots = json.load(open(PATH))
    is_list = isinstance(bots, list)
    items = bots if is_list else bots.get('bots', [])
    slugs = {b['slug'] for b in items}
    urls = set()
    for b in items:
        m = re.search(r'x\.ai/bot/([A-Za-z0-9_-]+)', b.get('url', ''))
        if m:
            urls.add(m.group(1).lower())

    added = []
    for n in NEW:
        if n['slug'] in slugs:
            print('skip slug collision:', n['slug'])
            continue
        if n['bot_id'].lower() in urls:
            print('skip url already listed:', n['bot_id'])
            continue
        entry = {
            'slug': n['slug'],
            'name': n['name'],
            'builder': {'name': n['builder'][0], 'x': n['builder'][1]},
            'tagline': n['tagline'][:140],
            'description': n['desc'],
            'category': n['category'],
            'url': 'https://x.ai/bot/' + n['bot_id'],
            'addedAt': TODAY,
            'status': 'published',
            'features': n['features'],
        }
        if n.get('source'):
            entry['source'] = n['source']
        items.append(entry)
        slugs.add(n['slug'])
        urls.add(n['bot_id'].lower())
        added.append(entry)

    with open(PATH, 'w') as f:
        json.dump(bots, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('added', len(added), '-> total', len(items))


if __name__ == '__main__':
    main()
