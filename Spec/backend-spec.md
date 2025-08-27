# backend-spec.md — FastAPI + PostgreSQL

## Stack
- **FastAPI** (uvicorn), **SQLAlchemy 2.0**, **PostgreSQL**, **Pydantic v2**.
- **Auth:** JWT (access 15m, refresh 7d), Argon2 password hashing, OAuth for social login.
- **Realtime:** Socket.IO via ASGI + Redis pub/sub.
- **RTC signaling:** WebSocket endpoints.
- **Media storage:** Pluggable storage (S3-compatible); local disk for dev.

## Domain Models (tables)
- `users` (id, email, role, password_hash, parent_id nullable for CHILD, approved_by_admin bool, created_at)
- `profiles` (id, user_id fk, display_name, avatar_url, bio)
- `game_credentials` (id, profile_id, game_name, username, password_ciphertext, iv, created_at)
- `conversations` (id, is_group bool, title nullable, created_by, created_at)
- `conversation_members` (conversation_id, user_id, role_in_convo)
- `messages` (id, conversation_id, sender_id, type enum[text,audio,image,system], content, media_url, created_at)
- `calls` (id, conversation_id nullable, started_by, started_at, ended_at, type enum[1v1,group], stats_json)
- `streams` (id, streamer_id, title, started_at, ended_at, status enum[started,ended])
- `screenshots` (id, owner_id, url, caption, created_at)
- `audit_logs` (id, actor_id, action, entity_type, entity_id, before_json, after_json, ip, created_at)
- `billing_plans` (id, name, price_cents, interval, active) — **future**
- `subscriptions` (id, parent_id, plan_id, status, started_at, canceled_at) — **future**
- `payments` (id, subscription_id, provider, external_id, amount_cents, status, created_at) — **future**

> **Sensitive data:** `game_credentials.password_ciphertext` uses AES-256-GCM envelope encryption.
Master key from env or KMS; per-record random IV; store only ciphertext + iv; never plaintext.

## REST Endpoints (examples)
- **Auth**
  - `POST /auth/login` — password login
  - `POST /auth/refresh`
  - `POST /auth/oauth/{provider}` — Google/Apple
  - `POST /auth/parent/register` — parent-first
  - `POST /auth/child` — parent creates child
  - `POST /auth/admin/approve` — admin approves parent
- **Profiles**
  - `GET/PUT /profiles/me`
  - `POST /profiles/me/avatar` — multipart upload
  - `POST /profiles/me/games` — add game credential (encrypted)
- **Chat**
  - `GET /conversations` — list
  - `POST /conversations` — 1:1 or group
  - `GET /conversations/{id}/messages`
  - `POST /conversations/{id}/messages` — send text/audio
- **Screenshots**
  - `GET /screenshots`
  - `POST /screenshots` — multipart upload
- **Streams**
  - `POST /streams/start` / `POST /streams/stop`
  - `GET /streams/active`
- **Admin**
  - `GET /admin/accounts` (filters)
  - `POST /admin/accounts/{id}/approve|suspend|reset-password`
  - `GET /admin/logs` (filters + CSV export)
  - `GET/PUT /admin/settings`
  - **Billing (future):** `GET/POST /admin/billing/*`

## WebSocket / Socket Namespaces
- `/ws/chat` — events: `message:new`, `message:ack`, `presence:update`
- `/ws/call` — events: `signal:offer`, `signal:answer`, `signal:ice`, `call:end`
- `/ws/stream` — events: `stream:live`, `stream:ended`, `reaction:new`, `viewer:list`

## Security & Compliance
- **Closed-circle access:** No public self-signup. Parent-first registration; admin approves parents; parents create/own child accounts.
- **RBAC:** Roles = `ADMIN`, `PARENT`, `CHILD`. Enforce at route and data layer.
- **Auth:** JWT (short-lived access, refresh tokens). Password hashing with Argon2. OAuth for social sign-in (Google/Apple).
- **PII & data protection:** Minimum necessary data. Encrypt sensitive fields at rest (PostgreSQL + app-level AES-256 envelope encryption).
- **Transport:** HTTPS everywhere. Secure cookies (httpOnly, sameSite=strict) for refresh token storage.
- **Rate limiting:** IP + user-based (e.g., 60 req/min) applied to auth & messaging endpoints.
- **Audit:** Immutable admin/parent sensitive actions written to `audit_logs` with actor, action, entity, before/after, timestamp.
- **Media safety:** File-type/size validation, AV scanning hook (stubbed in MVP), EXIF stripping.

## Testing
- **Unit:** Pydantic validation, encryption helpers, RBAC guards.
- **Integration:** Auth flow, parent creates child, admin approves, chat send/receive.
- **Load:** Stream and group call with 10–20 participants in staging.

## Phases & Estimates
- **Phase 1 (60h):** Auth, parent-child linking, profiles, chat REST + WS, screenshots REST.  
  **Success:** Complete parent-first flow; text chat; screenshot upload.
- **Phase 2 (60h):** Call signaling; live stream start/stop; reactions WS.  
  **Success:** Call and stream endpoints work with clients.
- **Phase 3 (40h):** Admin endpoints; audit logs; CSV export.  
  **Success:** Admin can manage accounts; logs recorded for all admin actions.
- **Phase 4 (24h):** Billing domain & endpoints (feature-flag OFF).  
  **Success:** CRUD for plans/subscriptions/payments behind flag.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- TURN server for reliable calls/streams.
- Object storage credentials for media.
