# auth-spec.md — Authentication & Roles

## Overview
Closed-circle auth with **parent-first** registration, **admin approval** for parents, and parent-owned **child account creation**.
Supports **social login** (Google/Apple) in addition to username/password.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `CenteredAuthForm` (username/password centered on page)
- `SocialAuthButtons`
- `ParentRegisterForm`
- `AdminApprovalBadge` (read-only state indicator)

## Backend Endpoints
- `POST /auth/parent/register`
- `POST /auth/login`
- `POST /auth/oauth/{provider}`
- `POST /auth/child` (parent token required)
- `POST /auth/admin/approve` (admin only)
- `POST /auth/refresh`, `POST /auth/logout`

## Database Models
- `users`: role enum[`ADMIN`,`PARENT`,`CHILD`], parent_id (nullable for CHILD), approved_by_admin bool
- Indexes on email, parent_id

## Integration Points
- Issues JWTs; frontend stores access in memory; refresh in httpOnly cookie.
- Role guards used across chat, calls, streams, screenshots.

## Testing Requirements
- Unit: password hashing, token rotation, role checks.
- Integration: parent-register → admin-approve → child-create → child-login.
- E2E: social login happy path, denied unapproved parent.

## Implementation Phases
- **P1 (24h):** Parent registration/login + admin approval.  
  **Success:** Unapproved parents cannot create children; approved can.
- **P2 (12h):** Social login providers.  
  **Success:** OAuth tokens validated; role assigned as PARENT pending approval.
- **P3 (8h):** Hardening: rate limits, lockouts, 2FA optional.  
  **Success:** Brute-force mitigated; suspicious IPs throttled.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `backend-spec.md` for tokens; `admin-control-spec.md` for approval UI.
