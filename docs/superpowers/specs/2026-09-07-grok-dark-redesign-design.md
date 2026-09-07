# GrokBot HQ — Grok Dark Redesign

Date: 2026-09-07
Status: Approved direction (Grok Dark, of 3 mockups), spec pending user review
Scope: Sitewide visual redesign of `src/` surfaces. Zero content-logic changes.

## Goal

Rebuild the site's visual layer around the approved **Grok Dark** direction: a stark
minimal monochrome aesthetic aligned with Grok/xAI's own web presence. Kill the generic
dark-AI-directory look (blue-tinted surfaces, glow gradients, backdrop-blur header,
hover lift shadows, rounded-full pills) and replace it with pure black, hairline borders,
mono kickers, and restrained 240ms interactions.

The approved reference is `docs/superpowers/mockups/grok-dark.html` (uncommitted). It is
the single source of truth for layout, copy, and token values on the homepage.

## Non-goals

- No changes to data flow, content JSON, routes, or site logic. The redesign touches
  presentation in `src/` only.
- No new dependencies. Fonts (Geist, Geist Mono) via `next/font/google` (already the
  Next.js-native path; check `src/app/layout.tsx` for the current font setup and swap if
  needed).
- No copy rewrites beyond what the mockup specifies for redesigned surfaces. AGENTS.md
  rule 4 (preserve existing editorial voice) applies to guide/article bodies, which are
  not redesigned beyond typography.

## Design tokens

From the mockup's `:root`. These become CSS custom properties in `globals.css`:

| Token | Value | Use |
|---|---|---|
| `--bg` | `#000` | page background |
| `--panel` | `#0a0a0a` | card background |
| `--elev` | `#111111` | elevated surfaces (if needed) |
| `--line` | `#1f1f1f` | hairline borders |
| `--line-hov` | `#3d3d3d` | border hover state |
| `--ink` | `#f5f5f5` | primary text |
| `--mut` | `#8f8f94` | secondary text |
| `--r` | `10px` | border radius (cards, buttons, chips) |

Typography: Geist 300/400/500/600 for UI, Geist Mono 400/500 for kickers, numbers, and
meta. Body 15px/1.55. Mono kickers 11px, `letter-spacing: .14em`, uppercase.

## Components to change

### 1. `src/app/globals.css`
Replace the current color/base layer: neutral `#000` background, remove `grid-bg` and
`hero-glow` utilities, adopt the token block above. Base font settings per mockup
(15px body, Geist stack). Motion: entrance keyframes (fade + 8px rise, 240ms ease-out)
with `.d1/.d2/.d3` stagger delays, all guarded by
`@media (prefers-reduced-motion: no-preference)`.

### 2. `src/components/header.tsx`
Sticky, `#000` solid background (no backdrop-blur), 60px height, 1px `--line` bottom
border. Logo: "GrokBot**HQ**" with HQ at `--mut`. Nav: 6 routes (Bots, Use cases, Guides,
Agent, Compare, News) at 13.5px `--mut`, hover to `--ink` (color transition only, no
underlines, no transforms).

### 3. `src/app/page.tsx` (homepage)
Per the mockup exactly:
- **Hero**: mono kicker "The independent Grok bot directory", H1
  "Find a Grok bot worth opening." (clamp 40–64px, weight 500, `-0.035em` tracking),
  sub "Every listing tested by hand. One click opens it in Grok.", CTAs "Browse all
  700 bots" (white solid, black text) + "Submit a bot" (hairline outline).
- **Stats band**: 4 cells with hairline separators: 700 verified bots / 442 builders /
  8 categories / 100% opened by hand. Mono tabular numerals.
- **Most installed**: 3-col grid of 6 bot cards (real top-installed bots from
  `content/bots.json`), each: name + mono category chip, one-line tagline,
  builder handle + mono install count, hairline card with `--line-hov` border on hover.
  Cards link to the bot's x.ai/bot URL.
- **Browse by job**: 8 category chips with mono counts (real counts from content).
- **Read first**: 3 guide cards (title, level label, mono meta: minutes + updated date).
- **Footer**: independence disclaimer (curly apostrophes: `&lsquo;Grok&rsquo;`), links
  (Submit, About, FAQ, mailto), mono bottom line "grokbothq.xyz · 700 bots indexed ·
  every listing opened by hand".

### 4. `src/components/bot-card.tsx`
Restyle to the mockup's card anatomy (top row name + category chip, tagline, hairline
bottom row with builder + mono installs). This is the shared card used across `/bots`,
category pages, etc., so it inherits the new tokens.

### 5. `src/components/footer.tsx`
Match the mockup footer structure: flex row disclaimer + links, mono bottom line.

### 6. Interior pages (`/bots`, `/new`, `/featured`, `/use-cases`, `/guides`, `/news`,
`/stats`, `/about`, `/faq`, `/submit`, `/groups`, `/integrations`, `/compare`, detail pages)
Interior pages inherit tokens automatically once globals change. A light pass per page:
kill any residual `hero-glow`/`grid-bg`/blue-tinted utility classes, align page headers
to the mono-kicker + tight-H2 pattern, ensure buttons follow the solid-white /
hairline-outline pair. No layout restructuring beyond that.

## Interaction rules

- Entrance animation: 240ms ease-out fade + 8px translateY, staggered 30/80/130ms,
  `prefers-reduced-motion` guarded.
- Hover states: border-color and color transitions only (180ms ease-out). No shadows, no
  translateY lifts, no scale, no gradients anywhere.
- Primary button hover: `opacity: .86` on white solid.

## Typography rules

- Curly apostrophes (`&rsquo;`/`&lsquo;` or the literal characters) in all shipped copy;
  no em-dashes (AGENTS.md standard).
- Tabular numerals via `font-variant-numeric: tabular-nums` on stat/install/meta numbers.
- Kickers: mono, 11px, uppercase, `.14em` tracking.

## Constraints & guards

1. `GEO-ANALYSIS.md` is untracked; never stage it (use selective `git add`).
2. Mockup files in `docs/superpowers/mockups/` stay uncommitted; they are working
   references only and are never staged.
3. No code comments in `src/` (AGENTS.md).
4. Content stays in `content/*.json`; homepage reads bot/guide/category data through the
   existing data layer. Numbers on the homepage must be the real values the data layer
   serves (700/442/8, real install counts, real category counts) — never hardcoded
   strings that can drift. If a stat is currently derived, keep deriving it.
5. One PR for the redesign (`ops/daily-...` or dedicated `redesign/grok-dark` branch),
   CI green before merge, route sweep after.
6. Buttons/links keep absolute URLs where the mockup uses them (`https://grokbothq.xyz/...`);
   in the codebase these become standard relative/next/link hrefs matching the repo's
   existing link conventions.

## Testing & verification

1. `npm run build` clean.
2. `npm start` + `node scripts/route-sweep.mjs http://localhost:3000` — all sitemap
   URLs return 200.
3. Visual spot-check of homepage against `grok-dark.html` mockup (side-by-side in
   browser).
4. Grep gates: no `grid-bg`, `hero-glow`, `backdrop-blur`, `rounded-full` remnants in
   redesigned surfaces; no `box-shadow` outside allowed none; no hex values for the old
   blue-tinted surfaces (`#101012`, `#19191c`, `#262629`).

## Open items (decide in plan, not now)

- Whether `next/font/google` Geist swap is needed or layout.tsx already uses a
  compatible setup.
- OG image / favicon updates to match the new aesthetic (probably out of scope; PR #22
  just shipped OG cards).
- The `/agent` and `/compare` pages' specific layouts (they inherit tokens; only token
  sweep, not redesign).
