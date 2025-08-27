# main-spec.md — Overall Blueprint, Phases & Git Rules

## App Description
A **closed-circle WhatsApp/Skype-style** platform for kids with admin-predefined access.
Features include **text chat, audio chat, video calls with screen sharing, live gameplay broadcast (separate screen), screenshot sharing,
profiles with game credentials**, onboarding flow, **parental oversight (parent-first)**, and **ultimate administrative control**.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Personas
- **Child:** Chats, calls, broadcasts gameplay, uploads screenshots, manages game usernames (and **securely** stored credentials).
- **Parent:** Registers first, creates/links child accounts, monitors activity, manages settings.
- **Admin (System Owner):** Approves parents, oversees all accounts, global settings, audit logs, future billing.

## Non-Goals (for MVP)
- Public discovery/friending outside the approved circle.
- Ads or marketing overlays.
- Full billing activation (scoped for a future phase).
- Advanced language moderation ML (future).

## Environments
- **Local dev:** Docker Compose (FastAPI, PostgreSQL, Redis, optional Coturn).
- **Staging/Prod:** Managed Postgres, object storage for media, HTTPS, TURN server.

## High-Level Architecture
- **Frontend:** Next.js 14 App Router + TS + Shadcn UI + Tailwind; WebRTC UIs; Socket client; PWA support.
- **Backend:** FastAPI (REST + WebSocket), SQLAlchemy 2.0, PostgreSQL, Redis pub/sub, Argon2 passwords, JWT.
- **Media:** Object storage (S3-compatible) abstraction; local disk for dev.
- **RTC:** WebRTC with STUN; Coturn TURN server for NAT traversal.

## Phased Roadmap & Estimates
All estimates assume 1–2 full-time engineers. Adjust proportionally for team size.

### Phase 1 — MVP (3 weeks)
- Auth (parent-first), child linking, admin approval
- Centered login + social login
- Profiles (photo upload, game credentials with encryption)
- 1:1 & group text chat; basic audio notes
- Screenshot upload & gallery
**Success Criteria:** Users (parent/child) can sign in, chat, set profiles, and share screenshots.  
**Estimate:** ~120 hours.  
> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

### Phase 2 — Realtime Media (3 weeks)
- Video calls (1:1, group), screen share toggle
- Dedicated **Live Gameplay** streaming screen with viewer list, chat, reactions
**Success Criteria:** Stable calls (<400ms one-way), broadcast start/stop, 10 simultaneous viewers in stream.  
**Estimate:** ~120 hours.  
> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

### Phase 3 — Oversight & Admin (3 weeks)
- Parental dashboard (usage overview)
- Ultimate Admin Control: account mgmt, approvals, suspensions
- **Audit logs** with filters & CSV export
**Success Criteria:** Parents & Admins can review activity and manage accounts; logs reflect all admin actions.  
**Estimate:** ~120 hours.  
> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

### Phase 4 — Future (2 weeks stub)
- **Billing management** (plans, subscriptions, transactions) — **feature-flagged OFF** by default
- Language monitoring scaffolding (flag pipeline) — optional
**Success Criteria:** Billing domain model + admin UI present but disabled; toggle enables sandbox flows.  
**Estimate:** ~80 hours.  
> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Project Management & Git
- **Branching:** `main` (release), `dev` (integration), `feature/*` branches.
- **PRs:** Require review, CI checks (lint, test, typecheck, E2E).
- **Conventional Commits:** `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`
- **Commits:** *Every 30 minutes.*
- **Issue templates:** Bug/Feature/Task with acceptance criteria.

## Risks & Mitigations
- **WebRTC NAT traversal:** Use TURN (Coturn) fallback.
- **Child safety & privacy:** Minimize data, encrypt credentials, strong RBAC and audit.
- **Browser permissions friction:** Clear UI prompts; fallback help tips.
- **Performance on low-end devices:** Adaptive bitrates; lazy-load heavy components.

## Dependencies Between Specs
- `auth-spec.md` → required by **all**.
- `chat-spec.md` → prerequisite for live reactions & stream chat.
- `video-calling-spec.md` → shares signaling with `live-gameplay-spec.md`.
- `parental-oversight-spec.md` → depends on `auth-spec.md`, `profile-spec.md`.
- `admin-control-spec.md` → depends on `auth-spec.md`, `audit log` infra in backend.
- `billing-spec.md` (future) → admin panel tabs + payment provider keys.
