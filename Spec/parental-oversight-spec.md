# parental-oversight-spec.md — Parent Controls & Linking

## Overview
**Parent-first** flow. Parents register, are approved by admin, and create/link child accounts. Dashboard shows usage.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `ParentRegisterForm`, `ChildAccountCreator`, `ParentalDashboard`
- Dashboard widgets: recent games, chat activity counters, time online

## Backend Endpoints
- `POST /auth/parent/register` → pending approval
- `POST /auth/admin/approve` (admin only)
- `POST /auth/child` (parent creates child)
- `GET /parent/dashboard` (aggregates usage)

## Database Models
- `users` (role relationships), `audit_logs` for sensitive actions

## Testing
- Parent cannot view other families; child data scoped to parent; approval gating works.

## Phases & Estimates
- **P1 (32h):** Registration/approval + child creation.  
  **Success:** Parent can add child; child login works.
- **P2 (24h):** Dashboard aggregation & charts.  
  **Success:** Accurate usage data shown; respects privacy.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md`, `chat-spec.md`, `video-calling-spec.md`, `live-gameplay-spec.md` for metrics.
