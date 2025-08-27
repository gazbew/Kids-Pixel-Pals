# integration-spec.md — Frontend/Backend Contracts

## Auth & Session
- **Login flow:** Parent → Admin Approval → Parent creates Child → Child logs in.
- **Tokens:** Access in memory, Refresh in httpOnly cookie. `/auth/refresh` rotates tokens.
- **DTOs:** 
  ```json
  {"user": {"id":"u_123","role":"PARENT","email":"p@example.com"}, "access":"<jwt>", "expires_in":900}
  ```

## Profiles
- `GET /profiles/me` → returns profile + game credential metadata (no plaintext passwords).
- `POST /profiles/me/games`  
  Request:
  ```json
  {"game_name":"Minecraft","username":"kiddo","password_plain":"<client-encrypted optional>"}
  ```
  Server encrypts at rest and never returns plaintext.

## Chat
- **Create 1:1:** `POST /conversations` with `member_ids` [kid_a, kid_b]
- **Send message:** `POST /conversations/{id}/messages` {"type":"text","content":"hello"}
- **WS `/ws/chat`**
  - `message:new` → broadcast to members
  - `presence:update` → online/typing

## Video & Streaming
- **WS `/ws/call`** for signaling (`offer`, `answer`, `ice`)
- **POST /streams/start`** returns `stream_id`; clients join `/ws/stream`
- **Reactions:** `reaction:new` payload {"emoji":":fire:","user_id":"u_123"}

## Screenshots
- **Upload:** `POST /screenshots` multipart: (file, caption). Returns canonical URL.

## Error Model
```json
{"error": {"code":"FORBIDDEN","message":"Insufficient role"}}
```

## Versioning
- `Accept: application/vnd.app.v1+json`
- Contract changes gated by feature flags.

## Phases & Estimates
- **Phase 1 (16h):** Define DTOs, OpenAPI docs, mock server.  
  **Success:** Frontend devs can build against mocks.
- **Phase 2 (8h):** Wire sockets; finalize error model.  
  **Success:** E2E chat & stream flows pass.
- **Phase 3 (8h):** Harden & document versioning/flags.  
  **Success:** Backwards-compatible schema notes published.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `backend-spec.md` for final routes.
- `frontend-spec.md` for client-side consumption patterns.
