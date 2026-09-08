# Grok Dark Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the site's visual layer around the approved Grok Dark direction (pure black, hairline borders, mono kickers, restrained motion) across tokens, header, footer, bot cards, identity, and homepage, with zero content-logic changes.

**Architecture:** Single-branch sitewide presentation pass. `src/app/globals.css` carries the new token base and shared component classes; each surface file is rewritten against those tokens; the data layer gains one derived selector (`topInstalledBots`) so homepage numbers stay derived, never hardcoded.

**Tech Stack:** Next.js 16, React 19, Tailwind CSS v4 (`@theme inline`), `next/font/google` (Geist + Geist Mono, already wired), TypeScript.

**Spec:** `docs/superpowers/specs/2026-09-07-grok-dark-redesign-design.md`
**Mockup (source of truth for homepage):** `docs/superpowers/mockups/grok-dark.html` (untracked, never commit)

---

## File structure map

| File | Change | Responsibility |
|---|---|---|
| `src/app/globals.css` | Whole-file rewrite | Single dark token base, shared `.container-x`/`.card`/`.btn`/`.badge`/`.kicker`/ad-unit/reveal/entrance styles. Kills `grid-bg`, `hero-glow`, `hero-bot`, `bot-blink`, `bot-eye`, glow/shadow hover states, pill radii, `.dark` overrides, and the duplicated block. |
| `src/app/layout.tsx` | Surgical removal | Remove `themeScript` const, its `<script>` tag, and the `Script` import. Everything else untouched. Answers spec open item: fonts already use `next/font/google`, no swap needed. |
| `src/components/header.tsx` | Whole-file rewrite | Solid black 60px sticky header, text logo, 6-link nav, preserved mobile menu. Drops `ThemeToggle` and the "List a bot" CTA. |
| `src/components/theme-toggle.tsx` | Delete | Dead after header rewrite. |
| `src/components/footer.tsx` | Whole-file rewrite | Mockup footer: disclaimer row + link row, mono bottom line with derived bot count. |
| `src/data/bots.ts` | Add function | `topInstalledBots(count)` derived selector, mirroring `latestBots`. |
| `src/components/bot-face.tsx` | Whole-file rewrite | Monochrome monogram tile. Same export name and prop signature so all consumers compile untouched. |
| `public/logo.svg`, `src/app/icon.svg` | Whole-file rewrite | Same "G" monogram tile in both. `favicon.ico` untouched. |
| `src/components/bot-card.tsx` | Whole-file rewrite | Mockup card anatomy (name + category chip, tagline, hairline builder/metric row) plus preserved Details link, freshness badge, and `OpenButton`. |
| `src/components/open-button.tsx` | One-line edit | Small variant gains a height override so the new fixed-height `.btn` does not stretch it. Tracking, nofollow, and arrow untouched. |
| `src/app/page.tsx` | Whole-file rewrite | Mockup homepage: hero, stats band, most-installed, browse-by-job, read-first. Keeps `revalidate` and metadata. |
| `src/components/hero-bot.tsx` | Delete | Dead after homepage rewrite. |
| `src/components/bots-browser.tsx` | One-line edit | Filter pills use the shared radius and hairline hover instead of full pills and accent hover. |
| Everything else in `src/` | Untouched | Interior pages inherit tokens; OG images and manifest stay per spec. |

---

### Task 0: Create the work branch

**Files:** none (git state only)

- [ ] **Step 1: Confirm a clean tree on main**

```bash
git status --short
git branch --show-current
```

Expected: `git status --short` prints nothing (only untracked `GEO-ANALYSIS.md` and `docs/superpowers/mockups/` may list as `??` entries; those are never staged). Branch is `main`.

- [ ] **Step 2: Create the redesign branch**

```bash
git checkout -b redesign/grok-dark
git branch --show-current
```

Expected: prints `redesign/grok-dark`.

---

### Task 1: Rewrite `src/app/globals.css` (tokens + shared components)

**Files:**
- Modify: `src/app/globals.css` (whole file)

**Why this exact content:** single dark `:root` (drops light theme and `.dark` overrides); container matches mockup `.wrap` (1080px = 67.5rem, 24px = 1.5rem); `.card`/`.btn` use `var(--r)`; hover states are border-color/color/opacity only; `.kicker` matches the mockup (11px, 0.14em, muted); `.badge` keeps its size but loses the pill radius; stagger/ad/page-enter/reveal blocks are preserved verbatim with bot refs removed; entrance keyframes are new, guarded by `prefers-reduced-motion: no-preference`.

- [ ] **Step 1: Replace the full file with this content**

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

:root {
  --background: #000;
  --surface: #0a0a0a;
  --elevated: #111111;
  --border-c: #1f1f1f;
  --border-hov: #3d3d3d;
  --foreground: #f5f5f5;
  --muted: #8f8f94;
  --accent: #f5f5f5;
  --accent-soft: rgba(255, 255, 255, 0.08);
  --accent-foreground: #000;
  --code-bg: #111111;
  --code-fg: #e5e5e5;
  --r: 10px;
}

@theme inline {
  --color-background: var(--background);
  --color-surface: var(--surface);
  --color-elevated: var(--elevated);
  --color-border: var(--border-c);
  --color-border-hover: var(--border-hov);
  --color-foreground: var(--foreground);
  --color-muted: var(--muted);
  --color-accent: var(--accent);
  --color-accent-soft: var(--accent-soft);
  --color-accent-foreground: var(--accent-foreground);
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
}

html {
  scroll-behavior: smooth;
  color-scheme: dark;
}

body {
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-sans), ui-sans-serif, system-ui, sans-serif;
  font-size: 15px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  font-feature-settings: 'kern' 1, 'liga' 1;
  text-rendering: optimizeLegibility;
}

a {
  color: inherit;
  text-underline-offset: 2px;
  text-decoration-thickness: 1px;
}

.tnum {
  font-variant-numeric: tabular-nums;
}

::selection {
  background: var(--accent);
  color: var(--accent-foreground);
}

@layer components {
  .container-x {
    width: 100%;
    max-width: 67.5rem;
    margin-inline: auto;
    padding-inline: 1.5rem;
  }

  .card {
    background: var(--surface);
    border: 1px solid var(--border-c);
    border-radius: var(--r);
  }

  .card-hover {
    transition: border-color 0.25s cubic-bezier(0.32, 0.72, 0, 1);
  }
  .card-hover:hover {
    border-color: var(--border-hov);
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    height: 44px;
    padding: 0 20px;
    border-radius: var(--r);
    font-size: 14px;
    font-weight: 500;
    line-height: 1;
    white-space: nowrap;
    transition: opacity 0.18s ease-out, background 0.18s ease-out, border-color 0.18s ease-out;
    cursor: pointer;
  }
  .btn:active {
    transform: scale(0.97);
  }

  .btn-primary {
    background: var(--foreground);
    color: var(--background);
  }
  .btn-primary:hover {
    opacity: 0.86;
  }

  .btn-accent {
    background: var(--accent);
    color: var(--accent-foreground);
  }
  .btn-accent:hover {
    opacity: 0.9;
  }

  .btn-ghost {
    border: 1px solid var(--border-c);
    background: transparent;
    color: var(--foreground);
  }
  .btn-ghost:hover {
    border-color: var(--border-hov);
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 0.25rem 0.5rem;
    border-radius: var(--r);
    border: 1px solid var(--border-c);
    color: var(--muted);
  }

  .badge-accent {
    background: var(--accent-soft);
    border-color: transparent;
    color: var(--accent);
  }

  .kicker {
    font-family: var(--font-mono), monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
  }

  .prose-block p {
    color: var(--foreground);
    line-height: 1.75;
    margin-bottom: 1rem;
  }
  .prose-block p:last-child {
    margin-bottom: 0;
  }
}

[data-reveal] .stagger > * {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.5s cubic-bezier(0.32, 0.72, 0, 1), transform 0.5s cubic-bezier(0.32, 0.72, 0, 1);
}
[data-reveal].reveal-in .stagger > * {
  opacity: 1;
  transform: none;
}
[data-reveal].reveal-in .stagger > *:nth-child(2) { transition-delay: 60ms; }
[data-reveal].reveal-in .stagger > *:nth-child(3) { transition-delay: 120ms; }
[data-reveal].reveal-in .stagger > *:nth-child(4) { transition-delay: 180ms; }
[data-reveal].reveal-in .stagger > *:nth-child(5) { transition-delay: 240ms; }
[data-reveal].reveal-in .stagger > *:nth-child(n + 6) { transition-delay: 300ms; }

@media (prefers-reduced-motion: reduce) {
  [data-reveal] .stagger > * {
    opacity: 1;
    transform: none;
    transition: none;
  }
}

.ad-slot {
  width: 100%;
  max-width: 21rem;
}

.ad-card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem 1.125rem;
  border-radius: var(--r);
  background: var(--surface);
  border: 1px solid var(--border-c);
  transition: border-color 0.25s cubic-bezier(0.32, 0.72, 0, 1);
}
.ad-card:hover {
  border-color: var(--border-hov);
}
.ad-card:active {
  transform: scale(0.98);
}

.ad-card-open {
  border-style: dashed;
}

.ad-label {
  font-family: var(--font-mono), monospace;
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.ad-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--foreground);
}

.ad-desc {
  font-size: 0.8125rem;
  line-height: 1.5;
  color: var(--muted);
}

.ad-cta {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent);
}

.ad-via {
  margin-top: 0.375rem;
  text-align: right;
  font-family: var(--font-mono), monospace;
  font-size: 0.625rem;
  color: var(--muted);
  opacity: 0.7;
}

@keyframes page-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: none; }
}
.page-enter {
  animation: page-in 0.4s cubic-bezier(0.32, 0.72, 0, 1) both;
}
@media (prefers-reduced-motion: reduce) {
  .page-enter { animation: none; }
}

[data-reveal] {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s cubic-bezier(0.32, 0.72, 0, 1), transform 0.6s cubic-bezier(0.32, 0.72, 0, 1);
}

[data-reveal].reveal-in {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}

@media (prefers-reduced-motion: no-preference) {
  @keyframes in {
    to { opacity: 1; transform: none; }
  }
  .in {
    opacity: 0;
    transform: translateY(8px);
    animation: in 0.24s ease-out forwards;
  }
  .d1 { animation-delay: 0.03s; }
  .d2 { animation-delay: 0.08s; }
  .d3 { animation-delay: 0.13s; }
}
```

- [ ] **Step 2: Build to verify the stylesheet compiles**

```bash
npm run build
```

Expected: Next.js build completes with no errors.

- [ ] **Step 3: Commit**

```bash
git add src/app/globals.css
git commit -m "redesign: adopt Grok Dark tokens and shared components"
```

---

### Task 2: Remove the theme bootstrap from `src/app/layout.tsx`

**Files:**
- Modify: `src/app/layout.tsx` (2 deletions only)

> Correction: the `Script` import from `next/script` must stay — it is also used by the Umami analytics tag. Only the theme const and its inline tag are removed.

- [ ] **Step 1: Delete the `themeScript` const (lines 63-70)**

Old:

```tsx
/** Applies the saved theme before first paint to avoid a flash. */
const themeScript = `
try {
  var t = localStorage.getItem('gbh-theme');
  var dark = t ? t === 'dark' : true;
  document.documentElement.classList.toggle('dark', dark);
} catch (e) {}
`;

export default function RootLayout({ children }: LayoutProps<"/">) {
```

New:

```tsx
export default function RootLayout({ children }: LayoutProps<"/">) {
```

- [ ] **Step 2: Delete the inline `<script>` tag (line 78)**

Old:

```tsx
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <noscript><style>{`[data-reveal]{opacity:1 !important;transform:none !important}`}</style></noscript>
```

New:

```tsx
      <head>
        <noscript><style>{`[data-reveal]{opacity:1 !important;transform:none !important}`}</style></noscript>
```

- [ ] **Step 3: Build to verify nothing else referenced the theme script**

```bash
npm run build
```

Expected: build clean. The `dark` class on `<html>` stays; all variables are now dark in `:root` so there is no flash to prevent. The `Script` import stays because the Umami tag still uses it.

- [ ] **Step 4: Commit**

```bash
git add src/app/layout.tsx
git commit -m "redesign: remove runtime theme switching"
```

---

### Task 3: Rebuild the header and delete `src/components/theme-toggle.tsx`

**Files:**
- Modify: `src/components/header.tsx` (whole file)
- Delete: `src/components/theme-toggle.tsx`

- [ ] **Step 1: Confirm `ThemeToggle` has no other consumers**

```bash
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "ThemeToggle|theme-toggle"
```

Expected: matches only in `src/components/header.tsx` (import + usage) and the definition file itself. No other consumer exists.

- [ ] **Step 2: Replace the full header file with this content**

```tsx
"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { HomeLink } from "./home-link";

const nav = [
  { href: "/bots", label: "Bots" },
  { href: "/use-cases", label: "Use cases" },
  { href: "/guides", label: "Guides" },
  { href: "/agent", label: "Agent" },
  { href: "/compare", label: "Compare" },
  { href: "/news", label: "News" },
];

export function Header() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background">
      <div className="container-x flex h-[60px] items-center justify-between gap-4">
        <HomeLink className="text-[15px] font-semibold tracking-[-0.01em]">
          <span>
            GrokBot<span className="font-semibold text-muted">HQ</span>
          </span>
        </HomeLink>

        <nav className="hidden items-center gap-[26px] md:flex" aria-label="Main">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`text-[13.5px] transition-[color] duration-[180ms] ease-out hover:text-foreground ${pathname === item.href ? "text-foreground" : "text-muted"}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>

      <div className="border-t border-border md:hidden">
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          className="container-x flex h-10 w-full items-center justify-between text-left text-sm text-muted"
        >
          Menu
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden className={`transition-transform ${open ? "rotate-180" : ""}`}>
            <path d="m6 9 6 6 6-6" />
          </svg>
        </button>
        {open && (
          <nav className="container-x grid gap-1 pb-3" aria-label="Mobile">
            {nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className={`rounded-md px-2 py-2 text-sm hover:bg-elevated hover:text-foreground ${pathname === item.href ? "text-foreground" : "text-muted"}`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
```

- [ ] **Step 3: Delete the toggle component**

```bash
Remove-Item -LiteralPath "src/components/theme-toggle.tsx"
```

- [ ] **Step 4: Build to verify**

```bash
npm run build
```

Expected: build clean, no `theme-toggle` import errors.

- [ ] **Step 5: Commit**

```bash
git add src/components/header.tsx src/components/theme-toggle.tsx
git commit -m "redesign: rebuild solid header, drop theme toggle and CTA"
```

---

### Task 4: Rebuild the footer

**Files:**
- Modify: `src/components/footer.tsx` (whole file)

- [ ] **Step 1: Replace the full footer file with this content**

```tsx
import Link from "next/link";
import { stats } from "@/data/bots";

export function Footer() {
  return (
    <footer className="border-t border-border py-10 pb-14">
      <div className="container-x">
        <div className="flex flex-wrap justify-between gap-8">
          <p className="max-w-[52ch] text-[12.5px] text-muted">
            GrokBot HQ is an independent directory. Not affiliated with xAI. ‘Grok’ is a trademark of xAI, used here descriptively.
          </p>
          <div className="flex flex-wrap gap-5">
            <Link href="/submit" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              Submit a bot
            </Link>
            <Link href="/about" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              About
            </Link>
            <Link href="/faq" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              FAQ
            </Link>
            <a href="mailto:hello@grokbothq.xyz" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              hello@grokbothq.xyz
            </a>
          </div>
        </div>
        <p className="mt-[26px] font-mono text-[11.5px] tracking-[0.02em] text-muted">
          grokbothq.xyz · {stats.bots} bots indexed · every listing opened by hand
        </p>
      </div>
    </footer>
  );
}
```

- [ ] **Step 2: Build to verify**

```bash
npm run build
```

Expected: build clean. The bot count stays derived from `stats.bots`.

- [ ] **Step 3: Commit**

```bash
git add src/components/footer.tsx
git commit -m "redesign: rebuild minimal footer"
```

---

### Task 5: Add `topInstalledBots` to `src/data/bots.ts`

**Files:**
- Modify: `src/data/bots.ts` (append one function after `latestBots`)

- [ ] **Step 1: Insert this function after the `latestBots` function (after line 35)**

```ts
export function topInstalledBots(count = 6): Bot[] {
  return [...bots]
    .filter((b) => typeof b.installs === "number")
    .sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0))
    .slice(0, count);
}
```

Placement anchor (unchanged surrounding code):

```ts
export function latestBots(count = 8): Bot[] {
  return [...bots].sort((a, b) => b.addedAt.localeCompare(a.addedAt)).slice(0, count);
}

export function topInstalledBots(count = 6): Bot[] {
```

- [ ] **Step 2: Build to verify**

```bash
npm run build
```

Expected: build clean.

- [ ] **Step 3: Commit**

```bash
git add src/data/bots.ts
git commit -m "redesign: add topInstalledBots selector"
```

---

### Task 6: Rewrite identity (`bot-face.tsx`, `logo.svg`, `icon.svg`)

**Files:**
- Modify: `src/components/bot-face.tsx` (whole file)
- Modify: `public/logo.svg` (whole file)
- Modify: `src/app/icon.svg` (whole file)

- [ ] **Step 1: Replace the full `bot-face.tsx` with this content**

```tsx
export function BotFace({
  slug,
  name,
  size = 40,
  hue: hueProp,
}: {
  slug: string;
  name: string;
  size?: number;
  hue?: number;
}) {
  void slug;
  void hueProp;
  const initial = name.trim().charAt(0).toUpperCase() || "G";

  return (
    <svg width={size} height={size} viewBox="0 0 40 40" className="block shrink-0" role="img" aria-label={`${name} monogram`}>
      <rect x="1" y="1" width="38" height="38" rx="8" fill="var(--surface)" stroke="var(--border-c)" />
      <text x="20" y="21" textAnchor="middle" dominantBaseline="central" fontFamily="var(--font-sans), sans-serif" fontSize="18" fontWeight="500" fill="var(--foreground)">
        {initial}
      </text>
    </svg>
  );
}
```

The export name and the `slug`/`name`/`size`/`hue` props are unchanged, so `bot-card.tsx`, `use-case-card.tsx`, `combo-card.tsx`, `groups/[slug]/page.tsx`, and `bots/[slug]/page.tsx` compile untouched.

- [ ] **Step 2: Replace both `public/logo.svg` and `src/app/icon.svg` with this identical content**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#000"/>
  <rect x="1" y="1" width="62" height="62" rx="13" fill="none" stroke="#1f1f1f" stroke-width="2"/>
  <text x="32" y="33" text-anchor="middle" dominant-baseline="central" font-family="Geist, Arial, sans-serif" font-size="30" font-weight="600" fill="#f5f5f5">G</text>
</svg>
```

`favicon.ico` is intentionally left as-is.

- [ ] **Step 3: Build to verify**

```bash
npm run build
```

Expected: build clean, all `BotFace` consumers still compile.

- [ ] **Step 4: Commit**

```bash
git add src/components/bot-face.tsx public/logo.svg src/app/icon.svg
git commit -m "redesign: monochrome monogram identity"
```

---

### Task 7: Restyle `bot-card.tsx` and fix the small `OpenButton` height

**Files:**
- Modify: `src/components/bot-card.tsx` (whole file)
- Modify: `src/components/open-button.tsx` (one class string)

- [ ] **Step 1: Replace the full `bot-card.tsx` with this content**

```tsx
import Link from "next/link";
import type { Bot } from "@/data/bots";
import { botOpens } from "@/data/bots";
import { OpenButton } from "./open-button";

export { OpenButton };

function relDate(iso: string): string {
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / 86_400_000);
  if (days <= 0) return "today";
  if (days === 1) return "yesterday";
  if (days < 7) return `${days}d ago`;
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export function BotCard({ bot }: { bot: Bot }) {
  const fresh = Date.now() - new Date(bot.addedAt).getTime() < 7 * 86_400_000;
  const opens = botOpens(bot.slug);
  const installs = typeof bot.installs === "number" ? bot.installs : null;

  return (
    <article className="card card-hover flex flex-col gap-3 p-[22px]">
      <div className="flex items-center justify-between gap-[10px]">
        <h3 className="text-base font-medium tracking-[-0.01em]">
          <Link href={`/bots/${bot.slug}`}>
            {bot.name}
          </Link>
        </h3>
        <span className="whitespace-nowrap rounded-md border border-border px-2 py-[3px] font-mono text-[10.5px] uppercase tracking-[0.08em] text-muted">
          {bot.category}
        </span>
      </div>

      <p className="flex-1 text-[13.5px] text-muted">{bot.tagline}</p>

      <div className="flex items-center justify-between border-t border-border pt-3 text-[12.5px] text-muted">
        {bot.builder.x ? (
          <a
            href={`https://x.com/${bot.builder.x}`}
            target="_blank"
            rel="noopener noreferrer"
            className="transition-[color] duration-[180ms] ease-out hover:text-foreground"
          >
            by @{bot.builder.x}
          </a>
        ) : (
          <span>{bot.builder.name}</span>
        )}
        {opens > 0 ? (
          <span title="Opens from GrokBot HQ readers" className="tnum font-mono text-foreground">
            {opens} opens
          </span>
        ) : installs !== null && installs > 0 ? (
          <span title="Installs reported by the source directory" className="tnum font-mono text-foreground">
            {installs} installs
          </span>
        ) : (
          <span />
        )}
      </div>

      <div className="flex items-center justify-between gap-3">
        <span className="flex items-center gap-3">
          <Link
            href={`/bots/${bot.slug}`}
            className="text-xs font-medium text-muted underline-offset-4 hover:text-foreground hover:underline"
          >
            Details
          </Link>
          {fresh && <span className="text-xs font-medium text-accent">new · {relDate(bot.addedAt)}</span>}
        </span>
        <OpenButton bot={bot} small />
      </div>
    </article>
  );
}
```

- [ ] **Step 2: Fix the small variant height in `open-button.tsx` (line 25)**

Old:

```tsx
      className={`btn btn-accent ${small ? "!px-3 !py-1.5 !text-xs" : ""}`}
```

New:

```tsx
      className={`btn btn-accent ${small ? "!h-7 !px-3 !py-1.5 !text-xs" : ""}`}
```

The new `.btn` sets a fixed 44px height; without `!h-7` the small variant would stretch to full button height. Tracking, `rel`, `aria-label`, and the arrow SVG are untouched.

- [ ] **Step 3: Build to verify**

```bash
npm run build
```

Expected: build clean.

- [ ] **Step 4: Commit**

```bash
git add src/components/bot-card.tsx src/components/open-button.tsx
git commit -m "redesign: restyle bot cards, fix small open-button height"
```

---

### Task 8: Rebuild the homepage and delete `src/components/hero-bot.tsx`

**Files:**
- Modify: `src/app/page.tsx` (whole file)
- Delete: `src/components/hero-bot.tsx`

- [ ] **Step 1: Confirm `HeroBot` has no other consumers**

```bash
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "HeroBot|hero-bot"
```

Expected: matches only in `src/app/page.tsx` (import + usage) and the definition file itself.

- [ ] **Step 2: Replace the full `page.tsx` with this content**

```tsx
import Link from "next/link";
import type { Metadata } from "next";
import { JsonLd } from "@/components/json-ld";
import { categories } from "@/data/categories";
import { botsByCategory, stats, topInstalledBots } from "@/data/bots";
import { guides, type Guide } from "@/data/guides";
import { absUrl, pageMetadata } from "@/lib/seo";

const HOME_DESCRIPTION =
  "Find a Grok bot worth opening. Hand-reviewed directory of the best Grok bots on xAI's platform - browse by category, learn bot combos, and master bot instructions with free guides.";

export const revalidate = 300;

export const metadata: Metadata = pageMetadata({
  title: "GrokBot HQ - The Hand-Reviewed Directory of Grok Bots",
  description: HOME_DESCRIPTION,
  path: "/",
  keywords: ["grok bots", "grok bot directory", "best grok bots", "grok bot list", "free grok bots", "grok bot combos", "grok xai bots", "grok ai bots", "grok bots that work"],
});

const READ_FIRST_SLUGS = [
  "what-are-grok-bots",
  "how-to-create-a-grok-bot",
  "how-to-write-bot-instructions",
];

const LEVELS: Record<string, string> = {
  "what-are-grok-bots": "Beginner",
  "how-to-create-a-grok-bot": "Builder",
  "how-to-write-bot-instructions": "Craft",
};

function levelFor(guide: Guide): string {
  const level = LEVELS[guide.slug];
  if (level) return level;
  const tag = guide.tags[0];
  if (!tag) return "Guide";
  return tag.charAt(0).toUpperCase() + tag.slice(1);
}

export default function HomePage() {
  const installed = topInstalledBots(6);
  const readFirst = READ_FIRST_SLUGS.map((slug) => guides.find((guide) => guide.slug === slug)).filter(
    (guide): guide is Guide => Boolean(guide),
  );

  return (
    <>
      <JsonLd data={[{ "@context": "https://schema.org", "@type": "WebPage", name: "GrokBot HQ - Grok bot directory", url: absUrl("/"), description: HOME_DESCRIPTION }]} />

      <section className="border-b border-border">
        <div className="container-x pb-[72px] pt-[96px]">
          <p className="kicker in">The independent Grok bot directory</p>
          <h1 className="in d1 mb-[18px] mt-5 max-w-[14ch] text-[clamp(40px,6.4vw,64px)] font-medium leading-[1.05] tracking-[-0.035em]">
            Find a Grok bot worth opening.
          </h1>
          <p className="in d2 max-w-[44ch] text-[17px] text-muted">
            Every listing tested by hand. One click opens it in Grok.
          </p>
          <div className="in d3 mt-[34px] flex flex-wrap gap-3">
            <Link href="/bots" className="btn btn-primary">
              Browse all {stats.bots} bots
            </Link>
            <Link href="/submit" className="btn btn-ghost">
              Submit a bot
            </Link>
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="container-x flex flex-wrap">
          {[
            { value: `${stats.bots}`, label: "verified bots" },
            { value: `${stats.builders}`, label: "builders" },
            { value: `${stats.categories}`, label: "categories" },
            { value: "100%", label: "opened by hand before listing" },
          ].map((stat, index, list) => (
            <div key={stat.label} className={`min-w-[200px] flex-1 py-[26px] ${index < list.length - 1 ? "border-r border-border pr-6" : ""}`}>
              <p className="tnum font-mono text-[26px] font-medium tracking-[-0.02em]">{stat.value}</p>
              <p className="mt-1 text-[12.5px] text-muted">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="container-x py-[72px]" id="bots">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Most installed</h2>
          <Link href="/bots" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All bots →
          </Link>
        </div>
        <div className="grid gap-[14px] min-[560px]:grid-cols-2 min-[860px]:grid-cols-3">
          {installed.map((bot) => (
            <a
              key={bot.slug}
              href={bot.url}
              target="_blank"
              rel="noopener noreferrer nofollow"
              className="card card-hover flex flex-col gap-3 p-[22px]"
            >
              <div className="flex items-center justify-between gap-[10px]">
                <h3 className="text-base font-medium tracking-[-0.01em]">{bot.name}</h3>
                <span className="whitespace-nowrap rounded-md border border-border px-2 py-[3px] font-mono text-[10.5px] uppercase tracking-[0.08em] text-muted">
                  {bot.category}
                </span>
              </div>
              <p className="flex-1 text-[13.5px] text-muted">{bot.tagline}</p>
              <div className="flex items-center justify-between border-t border-border pt-3 text-[12.5px] text-muted">
                <span>{bot.builder.x ? `by ${bot.builder.x}` : bot.builder.name}</span>
                <span className="tnum font-mono text-foreground">{bot.installs ?? 0} installs</span>
              </div>
            </a>
          ))}
        </div>
      </section>

      <section className="container-x py-[72px]">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Browse by job</h2>
          <Link href="/use-cases" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All use cases →
          </Link>
        </div>
        <div className="flex flex-wrap gap-[10px]">
          {categories.map((category) => (
            <Link
              key={category.slug}
              href={`/bots/category/${category.slug}`}
              className="inline-flex items-center gap-2 rounded-[10px] border border-border px-[14px] py-[9px] text-[13.5px] transition-[border-color] duration-[180ms] ease-out hover:border-[var(--border-hov)]"
            >
              {category.name}
              <span className="tnum font-mono text-[11px] text-muted">{botsByCategory(category.slug).length}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="container-x py-[72px]">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Read first</h2>
          <Link href="/guides" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All guides →
          </Link>
        </div>
        <div className="grid gap-[14px] min-[860px]:grid-cols-3">
          {readFirst.map((guide) => (
            <Link
              key={guide.slug}
              href={`/guides/${guide.slug}`}
              className="card card-hover flex flex-col gap-[10px] p-5"
            >
              <p className="text-xs text-muted">{levelFor(guide)}</p>
              <h3 className="text-[15.5px] font-medium leading-[1.35] tracking-[-0.01em]">{guide.title}</h3>
              <p className="flex gap-[10px] font-mono text-xs text-muted">
                <span>{guide.readingMinutes} min</span>
                <span>updated {new Date(guide.updatedAt).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span>
              </p>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
```

All homepage numbers are derived (`stats`, `topInstalledBots`, `botsByCategory`, guide `readingMinutes`/`updatedAt`). Dropped sections (fresh, standouts, combos, use cases, news, newsletter, FAQ, CTA) and their imports go with them; ads stay on `/bots` via the untouched `AdSlotCard`.

- [ ] **Step 3: Delete the hero mascot component**

```bash
Remove-Item -LiteralPath "src/components/hero-bot.tsx"
```

- [ ] **Step 4: Build to verify**

```bash
npm run build
```

Expected: build clean, no `hero-bot` import errors.

- [ ] **Step 5: Commit**

```bash
git add src/app/page.tsx src/components/hero-bot.tsx
git commit -m "redesign: rebuild homepage per Grok Dark mockup"
```

---

### Task 9: Interior light pass (bounded, evidence-backed)

**Files:**
- Modify: `src/components/bots-browser.tsx` (one class string)
- Verify-only: everything else listed below

Grep evidence (run before this task) shows the only legacy references outside deleted files are: `backdrop-blur` (header only, fixed in Task 3), `hero-glow`/`HeroBot` (homepage only, fixed in Task 8), `bot-eye` (bot-face only, fixed in Task 6), old blue hex in `.dark` (fixed in Task 1) plus `#0a0a0b` in OG images/manifest and `#101012` in the stats OG image (both intentionally kept per spec: OG images stay), and `rounded-full` utilities that are functional circles, dots, progress bars, step numbers, and floating controls.

- [ ] **Step 1: Align the `/bots` filter pills with the chip pattern (line 40)**

Old:

```tsx
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition-colors ${
                active === tab.slug
                  ? "bg-accent text-accent-foreground"
                  : "border border-border text-muted hover:border-accent hover:text-foreground"
              }`}
```

New:

```tsx
              className={`rounded-[10px] px-3 py-1.5 text-xs font-semibold transition-colors ${
                active === tab.slug
                  ? "bg-accent text-accent-foreground"
                  : "border border-border text-muted hover:border-[var(--border-hov)] hover:text-foreground"
              }`}
```

- [ ] **Step 2: Verify the remaining `rounded-full` hits are functional shapes only**

```bash
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "rounded-full"
```

Expected: matches only in `src/components/combo-card.tsx` (face ring), `src/components/back-to-top.tsx` (circular floating button), `src/components/newsletter-form.tsx` (input; no longer rendered on the homepage), `src/components/site-keys.tsx` (floating controls), `src/app/submit/page.tsx`, `src/app/guides/[slug]/page.tsx`, `src/app/groups/[slug]/page.tsx` (step-number circles), and `src/app/stats/page.tsx` (progress bar and dots). No card, button, chip, or badge pills remain.

- [ ] **Step 3: Verify no other legacy utility or blue-surface hex remains in render code**

```bash
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "hero-glow|grid-bg|backdrop-blur|bot-blink|bot-eye|hero-bot|theme-toggle|ThemeToggle|HeroBot"
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "box-shadow"
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "#101012|#19191c|#262629|#3b82f6|#2563eb"
```

Expected: first and second commands print nothing. Third prints only `src/app/stats/opengraph-image.tsx` line 50 (`#101012`, inside a generated OG image, kept per spec). `#0a0a0b` remains only in `*-opengraph-image.tsx`, `manifest.ts`, and neither is render CSS.

- [ ] **Step 4: Build to verify**

```bash
npm run build
```

Expected: build clean.

- [ ] **Step 5: Commit**

```bash
git add src/components/bots-browser.tsx
git commit -m "redesign: align bot filter pills with Grok Dark chips"
```

---

### Task 10: Final verification (build, route sweep, grep gates)

**Files:** none (verification only)

- [ ] **Step 1: Clean production build**

```bash
npm run build
```

Expected: Next.js build completes with no errors.

- [ ] **Step 2: Start the production server (own shell, leave running)**

```bash
npm start
```

Expected: server listens on `http://localhost:3000`.

- [ ] **Step 3: Sweep every sitemap URL for 200s (second shell, server running)**

```bash
node scripts/route-sweep.mjs http://localhost:3000
```

Expected: every sitemap URL returns 200.

- [ ] **Step 4: Run the spec grep gates**

```bash
Get-ChildItem -Path "src/app/page.tsx","src/components/header.tsx","src/components/footer.tsx","src/components/bot-card.tsx","src/components/open-button.tsx","src/app/globals.css" | Select-String -Pattern "rounded-full"
Get-ChildItem -Path "src" -Recurse -File | Select-String -Pattern "hero-glow|grid-bg|backdrop-blur|box-shadow|theme-toggle|ThemeToggle|HeroBot"
```

Expected: both commands print nothing.

- [ ] **Step 5: Confirm no secrets, mockups, or analysis files are staged**

```bash
git status --short
```

Expected: only intended `src/` modifications and the two component deletions. `GEO-ANALYSIS.md` and `docs/superpowers/mockups/` must not appear as staged (`A`/`M`) entries.

---

## Spec coverage checklist

- Tokens, typography, motion, interaction rules → Task 1 (globals) plus Task 8 hero entrance classes.
- Header (solid, 60px, 6 links, no CTA/toggle) → Task 3.
- Homepage sections, derived numbers, footer copy → Tasks 4, 5, 8.
- Bot card anatomy → Task 7.
- Footer structure → Task 4.
- Interior inheritance + light pass → Task 9.
- Identity (monogram tile, logo/icon swap, favicon stays) → Task 6.
- Constraints (selective `git add`, mockups untracked, no `src` comments, derived numbers, one PR, relative links, CI green, route sweep) → Tasks 0–10 steps as written.
- Testing and verification section → Task 10.
