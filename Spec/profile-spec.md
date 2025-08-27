# profile-spec.md — Profiles & Game Credentials

## Overview
Kids manage **display name, avatar**, and **game credentials** (username + **encrypted password**). Parents can view.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `AvatarUpload` with crop
- `ProfileEditor` (display name, bio)
- `GameCredentialList` (add/edit/remove rows)

## Backend Endpoints
- `GET/PUT /profiles/me`
- `POST /profiles/me/avatar` (multipart)
- `POST /profiles/me/games` (create)
- `PUT /profiles/me/games/{id}` (update)
- `DELETE /profiles/me/games/{id}`

## Database Models
- `profiles(id,user_id,display_name,avatar_url,bio)`
- `game_credentials(profile_id,game_name,username,password_ciphertext,iv)`

## Security
- AES-256-GCM envelope encryption; never return plaintext.
- Parent visibility (read-only) for child credentials metadata (not passwords).

## Testing
- Upload validation (type/size), encryption/decryption paths, RBAC checks.

## Phases & Estimates
- **P1 (16h):** Profile basics (avatar, display name).  
  **Success:** Can set avatar and name; persisted.
- **P2 (12h):** Game credentials with encryption + parent visibility.  
  **Success:** Credentials stored encrypted; parents see metadata.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md` for identity; storage config from `backend-spec.md`.
