# Pixira Legal and Support Localization Design

Date: 2026-07-23

## Goal

Bring the public Pixira Support and Terms of Use pages to the same 29
languages/locales already offered by the Privacy Policy, without changing the
existing public URLs.

## Approved approach

Use the Privacy Policy's existing static-page pattern:

- one `support.html` document with a language navigation list and 29 localized
  sections;
- one `terms.html` document with a language navigation list and 29 localized
  sections;
- stable fragment IDs in the form `#lang-<locale>`;
- explicit `lang` attributes on every navigation link and section;
- `dir="rtl"` for Arabic and Hebrew;
- no JavaScript, cookies, automatic redirects, or external services;
- English (United States) remains the fallback reference translation.

Separate files per locale would multiply links and deployment surface. A
JavaScript-only language switcher would hide content when scripting is
unavailable and make review harder. The static single-page structure therefore
has the lowest operational and accessibility risk.

## Locale contract

Both pages must contain exactly the same 29 locale IDs as `privacy.html`:

`ko`, `en-US`, `el`, `nl`, `nb`, `da`, `de`, `ru`, `ro`, `ms`, `vi`, `sv`,
`es-MX`, `ar`, `uk`, `it`, `id`, `ja`, `zh-Hans`, `cs`, `th`, `tr`, `pt-BR`,
`pl`, `fr-FR`, `fi`, `hu`, `he`, and `hi`.

Each locale must have one navigation link, one section, one unique heading ID,
and one localized “back to language list” link.

## Terms source of truth

The Korean and English sections are the semantic master copies. Before
translation, remove stale product claims from the current public page:

- do not state that there are six free cameras or promise a permanent
  “Classic pack” composition;
- do not state that premium bodies are individually purchasable;
- state that all current camera bodies and filters are available on the free
  tier, which currently includes up to seven completed saves per local calendar
  day;
- describe the current products as Pixira Pro monthly and yearly
  auto-renewing subscriptions plus a one-time Pixira Pro lifetime unlock, each
  providing unlimited saves;
- do not hardcode a trial length. If a trial is offered, its eligibility and
  duration are the values shown by Apple at purchase time;
- prices and currencies are the localized values displayed by Apple;
- subscriptions can be managed or cancelled through the user's Apple Account
  subscription settings;
- refunds are handled under Apple's policies;
- purchase restoration applies to eligible purchases associated with the same
  Apple Account;
- the Apple Standard EULA applies because Pixira does not provide a custom
  EULA.

This wording remains accurate when App Store Connect prices, trials, or the
catalog change.

## Support source of truth

Preserve the current factual FAQ scope:

- how to contact support and what diagnostic information to include;
- camera permission;
- microphone permission for video sound and Pro audio levels;
- saving to Photos;
- no Pixira account or login;
- purchases and restoration through Apple App Store and StoreKit;
- no upload of captured media to Pixira-operated servers.

Every localized support section links to its matching Privacy Policy locale and
the footer links to both Privacy Policy and Terms of Use.

## Presentation and accessibility

Reuse the current `.language-nav`, `.policy-language`, `.localized-meta`, and
RTL CSS. Update generic class naming only if needed by both page types.
Navigation targets must remain visible with a 44-point minimum touch target.
The pages must remain usable at a 320 CSS-pixel viewport and with reduced
motion enabled.

## Verification

Before publication:

1. Parse all three HTML pages and compare their locale-link and locale-section
   sets.
2. Confirm 29 unique navigation targets and 29 unique sections on Support and
   Terms.
3. Confirm every fragment target, `aria-labelledby` target, internal page link,
   stylesheet link, and `mailto:` link resolves.
4. Confirm Arabic and Hebrew sections and navigation labels use RTL.
5. Confirm stale claims (`3-day`, `3일`, `6 default`, `기본 6개`, and
   `individual bodies`) are absent.
6. Render desktop and 320-pixel mobile screenshots and inspect navigation,
   wrapping, focus visibility, RTL layout, and footer links.
7. Push the reviewed commit and confirm GitHub Pages serves the new commit and
   all three public URLs return HTTP 200.

## Translation quality boundary

The translations must preserve the Korean/English meaning and Apple product
names. They are product-localization drafts, not jurisdiction-specific legal
advice. A qualified native legal reviewer remains appropriate before using a
translation as a locally negotiated custom EULA; Pixira currently relies on
Apple's Standard EULA.
