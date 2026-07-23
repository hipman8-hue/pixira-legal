# Pixira Terms Localization Clause Matrix

Date: 2026-07-23  
Stage: A — Korean canonical copy and controlled English (United States) parity copy  
Scope: `terms.html` sections `#lang-ko` and `#lang-en-US` only

## App Store Connect evidence reviewed before drafting

The newest available local App Store Connect evidence is the read-only
2026-07-16 snapshot set in
`/Users/mac/Documents/secondcam/pricing/source/`. Its ASC observation window is
2026-07-15 16:35:40.365–16:35:50.335 UTC (2026-07-16
01:35:40.365–01:35:50.335 KST).

Primary evidence:

- `/Users/mac/Documents/secondcam/pricing/source/asc_raw_prices_2026-07-16.json`
  — captured 2026-07-15 16:35:50.707 UTC; authenticated user-opened Chrome
  session; read-only ASC Iris API data.
- `/Users/mac/Documents/secondcam/pricing/source/asc_raw_availability_2026-07-16.json`
  — captured 2026-07-15 16:35:50.710 UTC.
- `/Users/mac/Documents/secondcam/pricing/source/asc_get_request_log_2026-07-16.json`
  — captured 2026-07-15 16:35:50.710 UTC; recorded methods are GET and the
  capture is marked read-only.
- `/Users/mac/Documents/secondcam/pricing/source/asc_current_prices_2026-07-16.json`
  and
  `/Users/mac/Documents/secondcam/pricing/source/asc_availability_2026-07-16.json`
  — normalized 175-storefront snapshots derived from the raw capture.
- `/Users/mac/Documents/secondcam/pricing/source/manifest.json`
  — newest file by mtime (2026-07-16 03:54:22 KST); records the observation
  window, hashes, and 525 expected price cells.

### Product findings

| Product identifier | ASC evidence at observation time | Proven classification used for drafting | Not proven and therefore not frozen into the Terms |
|---|---|---|---|
| `com.pixira.pro.monthly` | Subscription resource `6780975582`; name `Pixira Pro Monthly`; `subscriptionPeriod: ONE_MONTH`; `state: READY_TO_SUBMIT`; 175 configured price rows and 175 supported-territory rows | Monthly recurring subscription. “Recurring” is an inference from the ASC subscription resource and one-month period; it is not a quoted `recurring: true` field. | Approval, live sale, storefront visibility, completed purchases, trial availability or terms, present/future displayed price or currency, and purchase eligibility |
| `com.pixira.pro.yearly` | Subscription resource `6780975999`; name `Pixira Pro Yearly`; `subscriptionPeriod: ONE_YEAR`; `state: READY_TO_SUBMIT`; 175 configured price rows and 175 supported-territory rows | Yearly recurring subscription. “Recurring” is an inference from the ASC subscription resource and one-year period; it is not a quoted `recurring: true` field. | Approval, live sale, storefront visibility, completed purchases, trial availability or terms, present/future displayed price or currency, and purchase eligibility |
| `com.pixira.pro.lifetime` | In-app purchase resource `6780974466`; name `Pixira Pro Lifetime`; `inAppPurchaseType: NON_CONSUMABLE`; `state: READY_TO_SUBMIT`; 175 configured price rows and 175 supported-territory rows | One-time non-consumable purchase identified as Pixira Pro Lifetime | Approval, live sale, storefront visibility, completed purchases, present/future displayed price or currency, purchase eligibility, entitlement implementation, and perpetual service availability |

The three configured supported-territory sets are equal. The frozen snapshot
contains point-in-time customer-price fields, but those fields do not establish
what Apple currently shows a user. The capture does not include a GET for
introductory offers, so it proves neither the presence nor absence of a trial
and proves no trial length. It also contains no evidence establishing which
license text Apple currently presents for a storefront. Accordingly, the
source copy defers price, currency, trial availability, eligibility, duration,
conversion, and applicable Apple license text to what Apple presents.

## Korean/English semantic parity matrix

Translation provenance: the Korean (`ko`) text was written in this repository
as the canonical legal source. The English (`en-US`) text was produced in this
repository as a controlled clause-by-clause translation of that Korean source.
The English text was checked against the Korean meaning, not treated as an
independent policy source. Each pointer below is a stable HTML fragment in the
current Stage A artifact.

| # | Required meaning | Korean canonical pointer | Controlled English pointer | Provenance and review result |
|---:|---|---|---|---|
| 1 | Download/use constitutes acceptance; do not use the App if the user does not agree | `terms.html#terms-ko-acceptance` | `terms.html#terms-en-US-acceptance` | Korean canonical → controlled English; clause meaning and condition checked — **PASS** |
| 2 | The Apple license terms presented for the user’s storefront apply; Pixira Terms supplement them; one Standard EULA reference; no assertion about ASC license configuration | `terms.html#terms-ko-apple-license` | `terms.html#terms-en-US-apple-license` | Korean canonical → controlled English; hierarchy and neutral state checked — **PASS** |
| 3 | Free tier includes all currently offered camera bodies and filters, with up to seven completed saves per local calendar day | `terms.html#terms-ko-purchase-free-tier` | `terms.html#terms-en-US-purchase-free-tier` | Korean canonical → controlled English; catalog scope, completion event, count, and local-day boundary checked — **PASS** |
| 4 | Pixira Pro monthly is an auto-renewing subscription providing unlimited saves | `terms.html#terms-ko-purchase-pro-products` | `terms.html#terms-en-US-purchase-pro-products` | Korean canonical → controlled English; product cadence, renewal type, and benefit checked — **PASS** |
| 5 | Pixira Pro yearly is an auto-renewing subscription providing unlimited saves | `terms.html#terms-ko-purchase-pro-products` | `terms.html#terms-en-US-purchase-pro-products` | Korean canonical → controlled English; product cadence, renewal type, and benefit checked — **PASS** |
| 6 | Pixira Pro lifetime is a one-time purchase providing unlimited saves | `terms.html#terms-ko-purchase-pro-products` | `terms.html#terms-en-US-purchase-pro-products` | Korean canonical → controlled English; purchase type and benefit checked — **PASS** |
| 7 | Amount charged, price, and currency are what Apple displays; payment is processed through the user’s Apple Account | `terms.html#terms-ko-purchase-apple-display` | `terms.html#terms-en-US-purchase-apple-display` | Korean canonical → controlled English; all dynamic display fields and payment channel checked — **PASS** |
| 8 | Monthly/yearly subscriptions renew until cancelled; renewal/cancellation is managed in Apple Account subscription settings; no same-price or fixed-hour promise | `terms.html#terms-ko-purchase-renewal-cancellation` | `terms.html#terms-en-US-purchase-renewal-cancellation` | Korean canonical → controlled English; renewal, cancellation, settings path, and excluded fixed assertions checked — **PASS** |
| 9 | A trial exists only if Apple offers one; eligibility, duration, and paid conversion are what Apple displays; no hardcoded duration | `terms.html#terms-ko-purchase-trial` | `terms.html#terms-en-US-purchase-trial` | Korean canonical → controlled English; offer condition and three dynamic fields checked — **PASS** |
| 10 | Eligible purchases can be restored through Pixira’s in-app Restore Purchases action while signed in with the same Apple Account | `terms.html#terms-ko-purchase-restore` | `terms.html#terms-en-US-purchase-restore` | Korean canonical → controlled English; eligibility, in-app action, and account identity checked — **PASS** |
| 11 | Refund requests and processing follow Apple’s policies | `terms.html#terms-ko-purchase-refunds` | `terms.html#terms-en-US-purchase-refunds` | Korean canonical → controlled English; responsible policy source checked — **PASS** |
| 12 | The user must act lawfully, respect rights and applicable Apple terms, avoid prohibited manipulation/distribution, and secure device/account access | `terms.html#terms-ko-responsibilities` | `terms.html#terms-en-US-responsibilities` | Korean canonical → controlled English; duties and legal-permission exception checked — **PASS** |
| 13 | The user retains rights in captured/created content and is responsible for necessary rights, consents, and lawful capture/save/share | `terms.html#terms-ko-user-content` | `terms.html#terms-en-US-user-content` | Korean canonical → controlled English; ownership and responsibility checked — **PASS** |
| 14 | The App is provided as-is/as-available to the lawful extent; no uninterrupted/error-free promise; indirect-damage limit preserves non-excludable rights | `terms.html#terms-ko-liability` | `terms.html#terms-en-US-liability` | Korean canonical → controlled English; disclaimer, damage categories, and mandatory-rights savings checked — **PASS** |
| 15 | Republic of Korea law governs while mandatory local consumer protections and lawful court jurisdiction remain preserved | `terms.html#terms-ko-governing-law` | `terms.html#terms-en-US-governing-law` | Korean canonical → controlled English; governing law and consumer/jurisdiction savings checked — **PASS** |
| 16 | Terms may change for App/legal requirements; changes are posted with a new effective date; continued use after effect constitutes agreement | `terms.html#terms-ko-changes-contact` | `terms.html#terms-en-US-changes-contact` | Korean canonical → controlled English; change reason, notice, date, and acceptance effect checked — **PASS** |
| 17 | Contact is `hipman8@gmail.com` | `terms.html#terms-ko-changes-contact` | `terms.html#terms-en-US-changes-contact` | Korean canonical → controlled English; identical mailto target checked — **PASS** |

## Stage A structural self-check

- Heading count and order: eight in Korean and eight in English — **PASS**.
- Purchase/subscription heading parity:
  `terms.html#terms-ko-purchases` ↔
  `terms.html#terms-en-US-purchases` — Korean canonical → controlled English;
  umbrella scope checked — **PASS**.
- Purchase-list count and order: one
  `data-contract="purchase-terms"` list with the same seven keyed direct items
  in each section — **PASS**.
- Localized metadata: effective date, operator, and contact match the
  same-locale Privacy section — **PASS**.
- Back links: Korean and English labels match their same-locale Privacy
  sections — **PASS**.
- Apple Standard EULA: exactly one link in each localized section — **PASS**.
- Stale fixed product, trial-length, renewal-price, and individual-body claims:
  absent — **PASS**.
- Stage A section boundary: only `ko` and `en-US` Terms sections exist. The
  29-link navigation is intentionally already present; the remaining 27
  sections are Task 3 Stage B work.
