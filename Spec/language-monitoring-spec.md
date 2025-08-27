# language-monitoring-spec.md — Future Language Monitoring (Optional)

## Overview
Future capability to **flag** potentially unsafe language in chats/streams. Review in Parent/Admin dashboards.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Approach (future)
- Hook message pipeline with a moderation microservice (rule-based to start).
- Store flags in `message_flags` table; never block delivery in MVP (flag-only).

## Backend
- Async worker processes messages; rates limited per user.

## Database Models
- `message_flags(id, message_id, rule, severity, created_at)`

## Testing
- Synthetic test messages; precision/recall metrics (manual review).

## Phases & Estimates
- **P1 (24h):** Rule engine + storage; UI badges.  
  **Success:** Parents/Admins see flagged counts.
- **P2 (40h):** ML model integration + thresholds.  
  **Success:** False positives reduced; escalation rules working.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `chat-spec.md`, `admin-control-spec.md`, `parental-oversight-spec.md`.
