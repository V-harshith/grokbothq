#!/usr/bin/env python3
"""Route the remaining generic keywords on grokbothq.

The anchor rule required "grok" in every keyword, so the generic terms already
sitting in our own seed list (ops/../full_pull.py) had no owner page. This adds
the pages for them:

  guides/what-are-ai-agents   <- what are ai agents, ai agents for business
  guides/custom-ai-agents     <- custom ai agents, build custom ai agents
  guides/best-ai-agents       <- best ai agents, ai agents list, ai agent directory
  compare/chatbot-vs-ai-agent <- chatbot vs ai agent, ai chatbot vs ai agent

(best ai chatbot / ai chatbot / ai chatbot comparison already shipped as
compare/best-ai-chatbot.)

Every page keeps the site's Grok identity and links back into the directory.
No invented benchmarks: where a claim would need a test we did not run, the
page says so.
"""
import json

G = "/root/grokbothq/content/guides.json"
C = "/root/grokbothq/content/compare.json"

guides = json.load(open(G))
compares = json.load(open(C))

have_g = {g.get("slug") for g in guides}
have_c = {c.get("slug") for c in compares}

NEW_GUIDES = [
    {
        "slug": "what-are-ai-agents",
        "title": "What Are AI Agents? A Plain-English Explanation",
        "seoTitle": "What Are AI Agents? Plain-English Guide (2026)",
        "description": "An AI agent is a model that can act, not just answer: it takes steps, uses tools, checks results and keeps going. Here is the plain difference from a chatbot.",
        "readingMinutes": 6,
        "updatedAt": "2026-09-22",
        "tags": ["ai agents", "what are ai agents", "ai agent basics", "grok bots"],
        "quickAnswer": "An AI agent is an AI system that takes actions toward a goal instead of only replying to a message. A chatbot answers your question and stops. An agent is given a goal, a set of tools it is allowed to use, and permission to run in a loop: it decides a step, does it, looks at the result, and decides the next step. Most of what people call an agent in 2026 is a language model wrapped in that loop with tools attached. The hard part was never the model, it is deciding which tools it may touch and where a human has to approve.",
        "intro": "The word agent is doing a lot of work right now, and most of it is marketing. Strip that away and there is a real, simple distinction underneath: a chatbot replies, an agent acts. This page explains the difference without the jargon, and where the genuine difficulty sits.",
        "sections": [
            {
                "heading": "The one-line difference",
                "body": [
                    "You type a question into a chatbot and it types an answer. The interaction ends when it replies. You type a goal into an agent and it works through the steps needed to reach it, using tools along the way, and comes back when it is done or stuck.",
                    "If you ask a chatbot to book a table, it writes you a nice paragraph about how to book a table. If you give an agent the same goal and a tool that can send an email, it composes the request and sends it, then checks whether anyone replied."
                ]
            },
            {
                "heading": "What actually makes something an agent",
                "list": [
                    "A goal rather than a prompt - the instruction describes an outcome, not a single answer",
                    "Tools it is allowed to call - a search, an API, a file, a browser, a messaging channel",
                    "A loop - it takes a step, reads the result, and decides the next step instead of stopping after one reply",
                    "Memory of what it has done so far, at minimum within the task",
                    "Somewhere a human can interrupt, approve or stop it"
                ],
                "body": [
                    "Remove the loop and the tools and you are back to a chatbot with a nicer prompt. That is why so many products that call themselves agents are really just assistants with a system prompt."
                ]
            },
            {
                "heading": "Where agents cause trouble",
                "body": [
                    "The model is rarely the failure point. The failure is permissions. An agent with a tool that can send email, move money, or delete a file will eventually do the wrong thing with it, because it is optimising for the goal you gave it and does not share your judgement about edge cases.",
                    "The pattern that holds up in practice is narrow tools and a human gate on anything irreversible. Give the agent a read-only tool by default. Make the destructive action require a person to press the button. Log every call so you can see what it did and reconstruct why."
                ]
            },
            {
                "heading": "How this relates to Grok bots",
                "body": [
                    "A Grok bot is a published agent-style assistant: instructions plus a task, shared as a link that opens for anyone. It is the lightweight end of the spectrum - no infrastructure, no tool integrations to configure, a bot you can hand to someone else in one click.",
                    "That makes it a reasonable way to test whether an idea is worth building properly. Publish the bot, see whether people use it and where it breaks, and only then decide whether the full version with real tools and a database is worth the build."
                ]
            }
        ]
    },
    {
        "slug": "custom-ai-agents",
        "title": "Custom AI Agents: What Building One Actually Involves",
        "seoTitle": "Custom AI Agents: How to Build One (2026 Guide)",
        "description": "A custom AI agent is instructions, tools and data shaped around one job. Here is what that means in practice, the three ways to build one, and what to sort out first.",
        "readingMinutes": 7,
        "updatedAt": "2026-09-22",
        "tags": ["custom ai agents", "build ai agent", "ai agents for business", "grok bots"],
        "quickAnswer": "A custom AI agent is a general model narrowed to one job: instructions that define the task, tools it is allowed to use, and the context it needs to do the work. There are three ways to get one. The lightest is a published bot - write the instructions well and share a link. The middle path is an agent platform, where you add tools and knowledge without writing infrastructure. The heaviest is code: your own loop, your own tools, your own hosting. Most business jobs that look like they need the third are solved by the first, and the way to find out is to ship the cheap version and watch where it fails.",
        "intro": "Custom sounds expensive. Usually it is not: the custom part of a custom agent is almost always the instructions and the judgement around it, not the software. Here is the honest breakdown of the three routes and what each actually costs you.",
        "sections": [
            {
                "heading": "What custom really means",
                "body": [
                    "You are not training a model. In almost every practical case you are taking a general model and constraining it: telling it the job, giving it the knowledge it needs, and limiting what it is allowed to do. That constraint layer is the whole product.",
                    "Two agents with the same underlying model and different instructions will behave completely differently. One will be useful and one will be a liability. That is why the instructions matter more than the model choice, and why the interesting work in 2026 is in writing them well rather than in picking a provider."
                ]
            },
            {
                "heading": "The three routes, from cheapest to heaviest",
                "list": [
                    "Published bot - instructions plus a task, shared as a link. Minutes to build, nothing to host, easiest to throw away if the idea is wrong.",
                    "Agent platform - the same instructions plus tools: a search, an inbox, a database, an integration. Still no infrastructure to run, but you now have permissions to reason about.",
                    "Own code - your own loop, your own tools, your own hosting and logging. Justified when you need a guarantee the platforms cannot give you, or when the agent touches something sensitive."
                ],
                "body": [
                    "The temptation is to start at the bottom because it feels more serious. That is backwards. The first version exists to find out whether the task is worth automating at all, and a link you can publish in an afternoon answers that question faster than a repo."
                ]
            },
            {
                "heading": "Sort these out before you build anything",
                "list": [
                    "The job in one sentence, with a named outcome - if you cannot write it, the agent will not know it either",
                    "What it may touch: read-only by default, and a named list of anything destructive",
                    "Where a human approves - anything irreversible or customer-facing needs a gate",
                    "What good looks like, so you can measure whether the agent is doing the job or just looking busy",
                    "What happens when it fails, because it will"
                ]
            },
            {
                "heading": "The failure mode to plan for",
                "body": [
                    "Custom agents fail quietly. They produce plausible output that is wrong, and because it reads well nobody checks it. The defence is boring: log every action, sample the output on a schedule, and keep the agent's permissions narrower than you think it needs.",
                    "This is also why the cheaper routes are worth taking seriously. A published bot you can watch for a week tells you more about whether the job is automatable than three weeks of building the heavy version."
                ]
            }
        ]
    },
    {
        "slug": "best-ai-agents",
        "title": "Best AI Agents in 2026: How to Choose One",
        "seoTitle": "Best AI Agents 2026: How to Choose (Not a Hype List)",
        "description": "There is no best AI agent, only the right category for the job. Here is how to sort agents by what they actually do, and how to test one in an afternoon.",
        "readingMinutes": 6,
        "updatedAt": "2026-09-22",
        "tags": ["best ai agents", "ai agents list", "ai agent directory", "grok bots"],
        "quickAnswer": "There is no best AI agent in 2026, because agents are not one category. Assistants with tools are good at drafting and research. Coding agents are good at repositories. Browser agents are good at repetitive web tasks. Published task bots are good at one narrow job you can hand to someone else. The useful question is not which is best, it is which category your job falls into, and then whether the cheapest option in that category survives a real test. Test with your own work, not a demo.",
        "intro": "Every list of the best AI agents is written by someone selling one. This page does something different: it sorts agents by the category of work they are actually suited to, and explains how to test a candidate in an afternoon rather than trusting a review.",
        "sections": [
            {
                "heading": "Why the lists are useless",
                "body": [
                    "Agents get compared on tasks that are chosen to flatter them. A coding agent looks unbeatable on a coding benchmark and useless at replying to customers, and neither fact is controversial. Ranking them against each other produces a number nobody can use.",
                    "The honest framing is category first. Decide what kind of work you are automating, then compare within that category only."
                ]
            },
            {
                "heading": "The categories that hold up",
                "list": [
                    "Assistant with tools - drafting, research, summarising, light automation. The safest place to start.",
                    "Coding agent - works inside a repository, opens changes for review. Strong at bounded tasks, needs a review step.",
                    "Browser agent - drives a real browser through repetitive web work. Powerful, and the fastest way to accidentally do something irreversible.",
                    "Narrow published bot - one job, handed over as a link. Cheap to try, easy to judge, and the right first attempt at most business tasks."
                ]
            },
            {
                "heading": "How to test one in an afternoon",
                "list": [
                    "Take three real tasks you actually did this week, including one that annoyed you",
                    "Run them through the candidate without adjusting how you word things",
                    "Count how many you would ship without editing. That number, not the demo, is the answer",
                    "Check what it did, not just what it produced - did it take an action you did not expect",
                    "Read the permission model before you give it anything that can send, delete or pay"
                ],
                "body": [
                    "If it does not clear that bar on your own work, no ranking is going to rescue it."
                ]
            },
            {
                "heading": "Browse before you build",
                "body": [
                    "Before commissioning anything custom, it is worth seeing what people have already published for the job. A directory of working bots is a cheap way to discover that someone solved your problem last month, or that the task is harder than it looked because twelve attempts all stalled in the same place.",
                    "The bots list on this site is a good place to start, and the comparison pages cover where published bots beat a full build and where they do not."
                ]
            }
        ]
    },
]

NEW_COMPARES = [
    {
        "slug": "chatbot-vs-ai-agent",
        "title": "Chatbot vs AI Agent: What Is the Actual Difference?",
        "seoTitle": "Chatbot vs AI Agent: The Real Difference (2026)",
        "description": "A chatbot answers, an agent acts. Compare how they are built, what they need, where each fails, and which one your job actually calls for.",
        "other": "AI chatbots",
        "updatedAt": "2026-09-22",
        "verdict": {
            "summary": "A chatbot is built to produce a reply; an agent is built to reach an outcome. That single difference drives everything else - the tools, the permissions, the failure modes and how much supervision it needs. Most jobs people want automated are better served by a chatbot or a published bot than by a full agent, because the expensive part of an agent is not the intelligence, it is the authority you have to hand it.",
            "chooseGrokBots": [
                "The job is a sequence of steps rather than a single answer",
                "Something outside the conversation has to change - an email sends, a record updates, a file is produced",
                "You want the output published as a link others can run, not a conversation you have to repeat",
                "You can name the one outcome that means it succeeded"
            ],
            "chooseOther": [
                "You need a considered reply to a question, not an action taken",
                "You are drafting, researching or summarising and a human will do the acting",
                "The task needs judgement you are not ready to delegate",
                "You want to try something with no permissions granted at all"
            ]
        },
        "rows": [
            {
                "aspect": "What it is for",
                "grok": "Reaching an outcome - it works until the job is done or it is stuck",
                "other": "Producing a reply - the interaction ends when it answers"
            },
            {
                "aspect": "How you use it",
                "grok": "You give it a goal and it decides the steps",
                "other": "You give it a prompt and it decides the words"
            },
            {
                "aspect": "What it needs to work",
                "grok": "Instructions, tools, a loop, and a place a human can interrupt",
                "other": "Instructions and context. No tools, so nothing to misuse"
            },
            {
                "aspect": "Where it fails",
                "grok": "It takes a real action you did not want, because it optimises for the goal you gave it",
                "other": "It is confidently wrong in prose, which costs you reading time rather than money"
            },
            {
                "aspect": "How you publish it",
                "grok": "A link that opens for anyone, with the task built in",
                "other": "Usually stays private - it is a tool for you, not a thing to hand over"
            },
            {
                "aspect": "Blast radius",
                "grok": "As large as the permissions you granted, so grant narrowly",
                "other": "None - it cannot change anything outside the conversation"
            }
        ],
        "sections": [
            {
                "heading": "The distinction that matters",
                "body": [
                    "Both are language models underneath. The difference is what happens after the first output. A chatbot stops. An agent reads its own result and decides what to do next, and that loop is what lets it finish a multi-step job - and also what lets it wander.",
                    "This is why the two are not competitors so much as different tools. Asking which is better is like asking whether a calculator is better than a spreadsheet."
                ]
            },
            {
                "heading": "The cost is authority, not intelligence",
                "body": [
                    "Making an agent smarter is the easy part, and the part everyone markets. Making it safe is the hard part, and it is entirely about what you let it touch. Every tool you attach is a permission, and permissions are where agents do damage.",
                    "The practical rule: read-only by default, an explicit named list of anything destructive, and a human gate on anything irreversible or customer-facing. An agent without those is not a productivity gain, it is a liability with good copy."
                ]
            },
            {
                "heading": "Which one your job calls for",
                "body": [
                    "If the deliverable is text someone will read, you want a chatbot or a well-written bot - faster, cheaper and nothing to supervise. If the deliverable is a change in the world, you want an agent, and you should budget for the supervision rather than pretending it will not be needed.",
                    "A useful test: write down what has to be different when the job is done. If the answer is a document or an answer, use a chatbot. If the answer is an email sent, a record created or a file produced, you are describing an agent."
                ]
            }
        ],
        "faqs": [
            {
                "q": "Is an AI agent just a chatbot with tools?",
                "a": "Not quite. Tools are necessary but the defining feature is the loop: the agent reads the result of its own action and decides the next step. A chatbot with a tool attached that fires once is still a chatbot."
            },
            {
                "q": "Are agents better than chatbots?",
                "a": "No. They are for different jobs. An agent can change things outside the conversation, which is exactly why it needs narrower permissions and more supervision than a chatbot."
            },
            {
                "q": "Do I need an agent for a simple automation?",
                "a": "Usually not. If the steps are fixed and known, a plain script or a scheduled job is cheaper, faster and far more predictable than an agent deciding each step for itself."
            },
            {
                "q": "What is the biggest risk with agents?",
                "a": "Permissions. An agent with access to something that sends, deletes or pays will eventually use it in a way you did not intend, because it optimises for the goal rather than for your judgement about edge cases."
            }
        ]
    },
]

added = []
for g in NEW_GUIDES:
    if g["slug"] not in have_g:
        guides.append(g); added.append("guide  " + g["slug"])
for c in NEW_COMPARES:
    if c["slug"] not in have_c:
        compares.append(c); added.append("compare " + c["slug"])

json.dump(guides, open(G, "w"), indent=1)
json.dump(compares, open(C, "w"), indent=1)

print("added:")
for a in added:
    print("  ", a)
print(f"\nguides now: {len(guides)}  compares now: {len(compares)}")
print("guide slugs :", [g["slug"] for g in guides])
print("compare slugs:", [c["slug"] for c in compares])
