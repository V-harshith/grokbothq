# grokbothq.xyz — decisions

Judgment calls with no obviously-correct answer, recorded with the reasoning *and* the option that
was discarded. A decision that only exists in someone's memory gets re-litigated, or worse, silently
reversed by the next person (or agent) who reads the audit.

## 1. The 77 duplicate-name clusters: differentiate, do not consolidate

**Audit said:** "Consolidate the 77 duplicate-name clusters (one survivor per name, 301 the rest;
differentiate intent)."

**Decided:** keep every listing; disambiguate instead. Titles and page furniture now say which one a
page is — `Chief of Staff (aryamankhawow) - Grok bot`, plus "52 other listings share the name
'Chief of Staff' — this one is built by @aryamankhawow".

**Because the data contradicts the premise.** Measured before deciding: across all 77 clusters there
are **zero shared URLs**; each entry has a different x.ai bot link and a different builder. "Chief of
Staff" ×53 is 53 different people who each built a bot and gave it the same obvious name. They are
not duplicates — they are distinct products with colliding names, and 301-ing 157 of them would have
deleted a hundred-odd real listings by real builders, in a directory whose whole promise is that
every listing was checked by hand.

**Discarded option:** consolidating anyway, on the theory that the audit's "differentiate intent"
clause covered it. Rejected because the *intent* signal the audit was reading (title/H1/description
alone) is fixed by the disambiguation, which is reversible; a 301 is not.

**Consequence:** the duplicate-intent exposure is addressed where it actually lives — the metadata —
and no listing was lost. If install-count-driven consolidation is ever wanted, that is a product
decision for the owner, not an SEO cleanup.

## 2. Descriptions lose the call to action before they lose a sentence

**Decided:** `composeDescription` keeps the CTA only when the whole description fits beside it.
Otherwise the description gets the full 155-character window and ends on a complete sentence.

**Because the first fix was still wrong.** Trimming the body to make room for "Open X in Grok with
one click." produced `"…sticks around, learns the week, and helps with life Open Jarvis in Grok with
one click."` — no longer cut mid-word, which was the audit's literal complaint, but still broken
English to a reader. The audit measured the character position of the cut; a person reading a search
result measures whether the sentence finishes. The CTA is the cheapest thing on the page to lose.

**Discarded option:** a shorter CTA. It still steals characters from the part that earns the click.

## 3. Titles drop the descriptor rather than cut the name

**Decided:** `composeTitle` tries `name - tagline`, then `name - <category> bot`, then the bare name,
and only clamps the name as a last resort, at 50 characters (the layout appends `" | GrokBot HQ"`).

**Because** 91% of titles ran long (median 109 chars) purely from appending the full tagline, and a
truncated name is worse than a missing descriptor: the name is the query. The fallback keeps the
search intent ("Chief of Staff … Grok bot") without pretending the tagline fits.

## 4. The client-side search holds 600 listings, not 2,594

**Decided:** `/bots` sends the newest 600 listings to the interactive island and displays the exact
directory totals from a separate count (so it can say "600 of 2,588 bots" honestly). The paginated
crawlable series covers everything.

**Because** the island was shipping a **1.5 MB** React flight payload inside a page the audit had
already flagged at 2.2 MB. Weight on the site's discovery path is a mobile problem, and the first
600 listings are what people actually browse.

**Discarded option:** keeping all 2,594 and stripping only the `description` field from the payload.
It would roughly halve the weight while breaking search over descriptions — trading a real feature
for a smaller number.

## 5. Thin listings get honest computed facts, not invented content

**Audit said:** "Add one non-commodity element per listing (editor's note / verified integration
count / 'vs the N similar bots')."

**Decided:** the element is derived, never written: category size, install rank among listings that
publish installs, how many listings share this name, and the last verification date. No listing got
prose a person did not write.

**Because** 1,905 of 2,524 descriptions restate the tagline, and the honest fix for a machine-written
directory is not more machine-written sentences — it is facts only that listing can state, which is
what the audit's own "vs the N similar bots" example describes. Nothing here can go stale silently
either: every number is recomputed at build.

## 6. `/md/*` markdown variants are `noindex`

**Decided:** `X-Robots-Tag: noindex` on the plain-text mirrors.

**Because** they are byte-identical content served for AI agents, and 0 are currently indexed. The
cheapest possible fix is to keep it that way; the alternative (letting a 2,600-page duplicate set
into the index and cleaning up later) is the expensive one.

## 7. Verification dates are stamped by the audit that does the verifying

**Decided:** `scripts/audit-directory.mjs` writes `lastVerifiedAt` on every listing it reaches, by
default, and only when a date actually changes; `--no-stamp` keeps a run read-only.

**Because** a freshness claim nobody records cannot be audited. Stamping only on `--fix` would mean
the site's "Verified <date>" line went stale on exactly the days nothing broke.

## 8. Four roundups, ranked only on published installs

**Decided:** engineering, productivity, money, research — and each page prints how many of its
listings publish install counts (20 of 372 in engineering) next to the ranking.

**Because** only a minority of listings publish anything measurable, so a "best of" that silently
ranked the rest on vibes would be the same fabricated-content problem in a new costume. The coverage
number is the honesty mechanism. Money got a page despite having the thinnest data because it is the
highest-intent category — and its page is largely about why the data is thin.

## 9. Ops writes and builds must not overlap

**Discovered the hard way:** `content/bots.json` was rewritten by the ops scout mid-build, so the
prerendered page set and the runtime map disagreed and `/bots/data` 404'd until a clean rebuild.

**Rule:** check the file's mtime is stable across a build. This is a local hazard only — Vercel
builds from a committed snapshot — but it wasted a verification cycle by producing a failure that
looked like a code bug.

## 10. `AGENTS.md` was not read

The repo's `AGENTS.md` is refused by the safety scanner (curl-exfil pattern; it is generated by
`next dev`). Nothing in this work depends on it, and it was not bypassed. Noted here because the ops
cron is instructed to read that file, and a change that contradicts a rule in it would be invisible
to this audit.
