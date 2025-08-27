# admin-control-spec.md — Ultimate Administrative Control

## Overview
Top-level admin UI to manage **parents**, **children**, approvals, permissions; view **activity logs**;
configure **global settings**; and manage **Billing** (future).

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `AdminTable` with filters/search
- Tabs: **Accounts**, **Activity Logs**, **Global Settings**, **Billing (future)**
- CSV export button on Logs

## Backend Endpoints
- `GET /admin/accounts?role=&status=`
- `POST /admin/accounts/{id}/approve|suspend|reset-password`
- `GET /admin/logs?actor=&entity=&action=&from=&to=`; `GET /admin/logs/export.csv`
- `GET/PUT /admin/settings`
- `GET/POST /admin/billing/*` (future guarded by flag)

## Database Models
- `audit_logs` immutable append-only
- Billing tables as in backend spec

## Activity Logging (detailed)
- Write log on every admin action with actor, IP, before/after snapshots.

## Testing
- Permissions enforced; CSV matches filters; settings persisted.

## Phases & Estimates
- **P1 (40h):** Accounts management + approvals.  
  **Success:** Admin can approve/suspend/reset reliably.
- **P2 (24h):** Activity Logs + CSV export.  
  **Success:** All actions recorded; export works.
- **P3 (12h):** Global settings UI.  
  **Success:** Feature flags & limits apply across app.
- **P4 (24h):** Billing tab (future).  
  **Success:** Renders plan/subscription/payment lists from API (flagged).

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md`, `backend-spec.md`, `billing-spec.md` (future).
