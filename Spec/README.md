# Kids Closed-Circle Comms + Gaming Companion — Project Specs

This repository contains the **complete project specifications** for a youth-focused, closed-circle communication platform
(text, audio, video + screen share) with **retro dark-red/pink** aesthetics, **parental oversight**, and an **ultimate admin**
for system-wide governance. Live gameplay streaming is provided on a **dedicated screen**, and kids can share gameplay screenshots.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Devices
Web-first responsive app for **Computer, Laptop, Mac, iOS, Android** (PWA-friendly).

## Security Baselines
- **Closed-circle access:** No public self-signup. Parent-first registration; admin approves parents; parents create/own child accounts.
- **RBAC:** Roles = `ADMIN`, `PARENT`, `CHILD`. Enforce at route and data layer.
- **Auth:** JWT (short-lived access, refresh tokens). Password hashing with Argon2. OAuth for social sign-in (Google/Apple).
- **PII & data protection:** Minimum necessary data. Encrypt sensitive fields at rest (PostgreSQL + app-level AES-256 envelope encryption).
- **Transport:** HTTPS everywhere. Secure cookies (httpOnly, sameSite=strict) for refresh token storage.
- **Rate limiting:** IP + user-based (e.g., 60 req/min) applied to auth & messaging endpoints.
- **Audit:** Immutable admin/parent sensitive actions written to `audit_logs` with actor, action, entity, before/after, timestamp.
- **Media safety:** File-type/size validation, AV scanning hook (stubbed in MVP), EXIF stripping.

---

## Spec Files
See each markdown file in this zip for detailed, phase-based specs with time estimates, testing, success criteria, and dependencies.
