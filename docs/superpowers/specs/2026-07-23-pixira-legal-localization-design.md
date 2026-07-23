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

The Korean section is the canonical legal copy. The English (United States)
section is its controlled reference translation. A clause-by-clause bilingual
parity check must pass before the English copy is used as the translation source
for the other 27 locales.

Before translation, remove stale product claims from the current public page:

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
- Pixira's terms supplement the Apple license terms shown for the user's
  storefront. Link to the Apple Standard EULA without making an enduring claim
  about whether App Store Connect has a custom EULA configured.

This wording remains accurate when App Store Connect prices, trials, or the
catalog change.

Because this is a material rewrite, the Terms effective date is 2026-07-23 in
all 29 locales. Each localized section carries the same operator identity,
contact email, and effective date.

## Support source of truth

Preserve the current factual FAQ scope:

- how to contact support and what diagnostic information to include;
- camera permission;
- microphone permission for video sound and Pro audio levels;
- saving to Photos;
- no Pixira account or login;
- Pixira Pro monthly/yearly subscriptions and the lifetime unlock are processed
  by the Apple App Store and StoreKit;
- eligible Pixira Pro access can be restored through the in-app restore action,
  and Pixira does not receive or store payment-card details;
- no upload of captured media to Pixira-operated servers.

Every localized support section links to its matching Privacy Policy locale and
the footer links to both Privacy Policy and Terms of Use.

## Presentation and accessibility

Reuse the current `.language-nav`, `.policy-language`, `.localized-meta`, and
RTL CSS. Update generic class naming only if needed by both page types.
Navigation links must have a computed minimum height of 44 CSS pixels. The
pages must remain usable at a 320 CSS-pixel viewport. With
`prefers-reduced-motion: reduce`, computed `scroll-behavior` must be `auto`.

## Verification

Before publication:

1. Parse all three HTML pages and compare their locale-link and locale-section
   sets.
2. Confirm 29 unique navigation targets and 29 unique sections on Support and
   Terms.
3. Confirm every fragment target, `aria-labelledby` target, internal page link,
   stylesheet link, and `mailto:` link resolves.
4. Confirm Arabic and Hebrew sections and navigation labels use RTL.
5. Confirm every locale has the same eight Terms headings, the same seven
   purchase/subscription bullets, and the same seven Support topics. Review a
   29-row clause matrix covering acceptance, Apple license terms, free-tier
   quota, all three Pro products, dynamic trial eligibility/duration,
   auto-renewal/cancellation, refund, restoration, user content, liability,
   governing law, and contact. Reject any missing or contradictory clause.
6. Confirm stale claims (`3-day`, `3일`, `6 default`, `기본 6개`, and
   `individual bodies`) are absent.
7. Confirm every Terms section carries the 2026-07-23 effective date and the
   same operator/contact identity.
8. Inspect the most recent available App Store Connect evidence for the
   monthly, yearly, and lifetime product identifiers. Publication wording must
   remain dynamic for any live value that cannot be proven, including trial
   availability, trial length, price, currency, and eligibility. Do not claim
   that no custom EULA exists.
9. Use computed styles to confirm 44 CSS-pixel language targets and
   `scroll-behavior: auto` under reduced motion. Render desktop and 320-pixel
   mobile screenshots and inspect navigation,
   wrapping, focus visibility, RTL layout, and footer links.
10. Push the reviewed commit and confirm the Pages build reports `built`, the
   remote `main` SHA equals the reviewed local SHA, and all canonical public
   URLs return HTTP 200:
   `https://hipman8-hue.github.io/pixira-legal/`,
   `/privacy`, `/support`, and `/terms`.

## Translation quality boundary

The translations must preserve the Korean/English meaning and Apple product
names. They are product-localization drafts, not jurisdiction-specific legal
advice. A qualified native legal reviewer remains appropriate before using a
translation as a locally negotiated custom EULA; Pixira currently relies on
Apple's Standard EULA.
