# Pixira Legal and Support Localization Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish accurate, accessible Support and Terms of Use pages in the same 29 locales as the existing Pixira Privacy Policy.

**Architecture:** Keep each public URL as a no-JavaScript static HTML page. Reuse the Privacy Policy's language navigation and section structure, treat Korean as the canonical legal copy and English (US) as the controlled translation source, then add the remaining 27 locale sections with stable fragment IDs and explicit language/direction metadata.

**Tech Stack:** Static HTML/CSS, Python 3 standard library validation, GitHub Pages.

---

## File map

- Create `scripts/check_localizations.py`: structural and content-contract verifier for all three public pages.
- Create `docs/reviews/2026-07-23-localization-clause-matrix.md`: reproducible 29-row semantic review evidence and translation provenance.
- Modify `support.html`: current support source text plus 29 localized sections.
- Modify `terms.html`: corrected current product/legal source text plus 29 localized sections.
- Modify `style.css`: shared page-section and 44×44 CSS-pixel language-target rules if required.
- Preserve `privacy.html`: authoritative locale list and existing privacy content.

## Chunk 1: Contract and Support

### Task 1: Add the failing localization contract

**Files:**
- Create: `scripts/check_localizations.py`
- Read: `privacy.html`
- Test: `support.html`
- Test: `terms.html`

- [x] **Step 1: Write a standard-library verifier**

The verifier must parse each page with `html.parser`, extract `.language-nav`
fragment links and `.policy-language` section IDs, and fail unless Support and
Terms exactly match Privacy's ordered 29-locale contract. It must also verify
unique IDs, fragment targets, `aria-labelledby` targets, stylesheet/internal
links, `mailto:` links, RTL metadata for Arabic/Hebrew, Terms heading/bullet
counts, Support topic counts, Terms-only effective-date/operator/contact
parity, localized back-to-language-list links, Support's payment-card-storage
disclosure, and stale claim absence. It must also reject `<script>`,
meta-refresh redirects, external runtime resources, missing locale-matched
`privacy#lang-<locale>` Support links, and a missing Apple Standard EULA link in
each Terms locale. It must reject Korean/English claims that either a custom
EULA exists or no custom EULA exists. A `--page support` or `--page terms`
mode must run only the selected page's contract; the default mode validates
both.

- [x] **Step 2: Run the verifier and confirm RED**

Run:

```bash
python3 scripts/check_localizations.py
```

Expected: nonzero exit because `support.html` and `terms.html` have only Korean
and English sections.

- [x] **Step 3: Commit the failing contract**

```bash
git add scripts/check_localizations.py
git commit -m "test: define legal locale contract"
```

### Task 2: Localize the Support page

**Files:**
- Modify: `support.html`
- Modify: `style.css` only if the existing shared classes do not meet the measurable contract
- Test: `scripts/check_localizations.py`

- [ ] **Step 1: Replace the bilingual layout with the 29-locale structure**

Copy the ordered navigation contract from `privacy.html`. Add exactly seven
localized topics per section: contact, camera permission, microphone
permission, Photos saving, account/login, the three current Pixira Pro
products/restoration, and server upload behavior. Do not refer to separately
purchasable premium bodies.

- [ ] **Step 2: Link each locale to matching legal fragments**

Each support section must link to `privacy#lang-<locale>` and the page footer
must link to both `privacy` and `terms`.

- [ ] **Step 3: Run the verifier**

Run:

```bash
python3 scripts/check_localizations.py --page support
```

Expected: exit 0 with 29 Support navigation links and 29 Support sections.
Then run the default command and confirm it still fails only because Terms has
not yet been localized.

- [ ] **Step 4: Commit Support**

```bash
git add support.html style.css
git commit -m "feat: localize Pixira support in 29 languages"
```

## Chunk 2: Terms and Publication

### Task 3: Correct and localize Terms of Use

**Files:**
- Modify: `terms.html`
- Create: `docs/reviews/2026-07-23-localization-clause-matrix.md`
- Test: `scripts/check_localizations.py`

- [ ] **Step 1: Inspect current App Store Connect evidence**

Inspect the newest available evidence for `com.pixira.pro.monthly`,
`com.pixira.pro.yearly`, and `com.pixira.pro.lifetime` before freezing the
source copy. Record the evidence path/date and proven product types in the
clause-matrix document. Keep price, currency, trial, eligibility, and custom
EULA wording dynamic where current live evidence is unavailable.

- [ ] **Step 2: Correct the Korean canonical copy**

Set the effective date to 2026-07-23. Remove the stale six-camera/Classic-pack,
three-day-trial, premium-content, individual-body, same-price renewal, and
custom-EULA assertions. State the current free tier (all current bodies and
filters, up to seven completed saves per local calendar day), Pixira Pro
monthly/yearly auto-renewing subscriptions, lifetime one-time unlock, unlimited
saves, Apple-displayed dynamic price/trial details, management/cancellation,
refund, restoration, and the supplemental relationship to Apple storefront
license terms. Each locale must link to
`https://www.apple.com/legal/internet-services/itunes/dev/stdeula/`.
The copy must remain neutral about whether a custom EULA is configured.

- [ ] **Step 3: Create the controlled English (US) parity copy**

Match every heading and purchase/subscription bullet clause-for-clause with the
Korean canonical copy.

- [ ] **Step 4: Run the Korean/English parity gate**

Run a clause matrix over the Korean and English sections and confirm each of the
eight headings, seven purchase/subscription bullets, and all semantic items in
the design spec appear once without contradiction. Do not use English as the
translation source until this gate passes.

- [ ] **Step 5: Add the other 27 locale sections**

Use the exact locale order, IDs, headings, metadata, and RTL behavior defined by
Privacy. Every locale must preserve all eight headings and seven
purchase/subscription bullets.

- [ ] **Step 6: Complete the reproducible semantic matrix**

Create one row per locale with a checkbox and exact section/paragraph pointer
for acceptance, Apple license terms, free quota, monthly/yearly/lifetime
products, dynamic trial, renewal/cancellation, refund, restoration, user
content, liability, governing law, contact, and the seven Support topics.
Record that the Korean canonical copy and controlled English source were
produced in this repository and the other locale copies were translated from
that English source. A reviewer must mark each row PASS only after checking the
localized text against the clause mapping; any missing or contradictory item is
FAIL and blocks publication.

- [ ] **Step 7: Run the full verifier**

Run:

```bash
python3 scripts/check_localizations.py
```

Expected: exit 0 with 29 navigation links and 29 sections for Privacy, Support,
and Terms; no stale claims.

- [ ] **Step 8: Commit Terms and semantic evidence**

```bash
git add terms.html docs/reviews/2026-07-23-localization-clause-matrix.md
git commit -m "feat: localize corrected Pixira terms in 29 languages"
```

### Task 4: Visual, semantic, and deployment verification

**Files:**
- Verify: `privacy.html`
- Verify: `support.html`
- Verify: `terms.html`
- Verify: `style.css`

- [ ] **Step 1: Run structural and repository checks**

```bash
python3 scripts/check_localizations.py
git diff --check main...HEAD
git status --short
```

Expected: verifier exits 0, no whitespace errors, only intentional commits.

- [ ] **Step 2: Run eight current designer-eye browser passes**

Serve the worktree locally, capture desktop and 320 CSS-pixel screenshots for
Support and Terms. Save current-build evidence for eight distinct passes:

1. desktop alignment, radii, padding, color roles, highlight/shadow direction,
   and depth;
2. 320 CSS-pixel navigation wrapping and screenshot artifacts;
3. Korean/English typography and optical centering;
4. long Latin strings in German, French, and Brazilian Portuguese;
5. CJK, Thai, and Devanagari wrapping;
6. Arabic RTL alignment and touch targets;
7. Hebrew RTL alignment and touch targets;
8. keyboard focus, 44×44 CSS-pixel targets, footer links, and reduced motion.

Computed language-link width and height must each be at least 44 CSS pixels.
No design or release PASS is allowed with fewer than all eight evidence-backed
passes.

- [ ] **Step 3: Complete the 29-row semantic matrix**

For every Terms locale, verify and sign off the clause-matrix row. For every
Support locale, verify and sign off the seven source topics. Record reviewer,
date, result, and evidence pointer for each row.

- [ ] **Step 4: Run spec and quality reviews**

Dispatch a spec-compliance reviewer, then a code/content-quality reviewer.
Resolve all findings and re-run the verifier after every correction.

- [ ] **Step 5: Review current App Store Connect evidence**

Inspect the newest available App Store Connect evidence for
`com.pixira.pro.monthly`, `com.pixira.pro.yearly`, and
`com.pixira.pro.lifetime`. Record whether each SKU and purchase type is proven.
Confirm that the published copy does not hardcode any unproven trial, price,
currency, eligibility, or custom-EULA state. An unproven dynamic value is a
publication pass only when the copy delegates it to the value Apple displays at
purchase time; a contradictory product type or SKU is a release blocker.

- [ ] **Step 6: Commit review fixes**

```bash
git add support.html terms.html style.css scripts/check_localizations.py
git commit -m "fix: resolve legal localization review"
```

Create the commit only when review produces changes.

- [ ] **Step 7: Push and verify GitHub Pages**

Push the reviewed feature branch, fast-forward `main` only after final release
review, then confirm remote `main` SHA, GitHub Pages build state `built`, and
HTTP 200 for:

- `https://hipman8-hue.github.io/pixira-legal/`
- `https://hipman8-hue.github.io/pixira-legal/privacy`
- `https://hipman8-hue.github.io/pixira-legal/support`
- `https://hipman8-hue.github.io/pixira-legal/terms`

After the build, download the deployed `privacy`, `support`, `terms`, and
`style.css` bodies without query parameters. Compare their SHA-256 hashes with
the reviewed local files and run the locale/content verifier against the
downloaded HTML. HTTP 200 without matching reviewed content is a deployment
failure.
