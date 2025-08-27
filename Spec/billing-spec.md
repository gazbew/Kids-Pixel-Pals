# billing-spec.md — Future Billing Management (Feature-Flagged)

## Overview
Subscription & payment management exposed in Admin; **disabled by default** until activation.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `BillingTab` (plans, subscriptions, payments, refunds), hidden until `features.billing=true`

## Backend Endpoints
- `GET/POST /admin/billing/plans`
- `GET/POST /admin/billing/subscriptions`
- `GET/POST /admin/billing/payments`
- Webhooks endpoint (provider TBD; Stripe suggested) — behind feature flag

## Database Models
- `billing_plans`, `subscriptions`, `payments`

## Testing
- Fake provider in dev; end-to-end unit + integration with mock signatures.

## Phases & Estimates
- **P1 (24h):** Plans CRUD + feature flag wiring.  
  **Success:** Admin can define plans (no charging).
- **P2 (24h):** Subscriptions & payment intents (sandbox).  
  **Success:** Subscription lifecycle in sandbox.
- **P3 (16h):** Reporting & refunds.  
  **Success:** Summaries render; refund flow mocked.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `admin-control-spec.md`, provider credentials when enabled.
