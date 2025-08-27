# screenshots-spec.md — Gameplay Screenshot Sharing

## Overview
Kids upload and browse **gameplay screenshots** with captions; retro gallery with pixel frames.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `ScreenshotUploader` (drag/drop), `ScreenshotTile`, `GalleryGrid`, detail modal with comments (P2)

## Backend Endpoints
- `POST /screenshots` (multipart)
- `GET /screenshots` (list, owner or shared scope)
- `GET /screenshots/{id}`, `DELETE /screenshots/{id}`

## Database Models
- `screenshots(owner_id,url,caption,created_at)`
- (P2) `screenshot_comments`

## Testing
- File validation; EXIF stripping; pagination; permissions.

## Phases & Estimates
- **P1 (16h):** Upload + gallery list.  
  **Success:** Validated upload, preview, persisted URL.
- **P2 (16h):** Comments & moderation flags.  
  **Success:** Threaded comments; report flow writes flags.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- Media storage; `auth-spec.md` for ownership.
