# chat-spec.md — 1:1 & Group Text/Audio

## Overview
Real-time **1:1 and group chat** with text, audio notes, read receipts, and presence.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `ChatList` with avatars and unread badges
- `ConversationView` with `MessageBubble`
- `ChatComposer` (text, audio record button)
- Presence indicators (typing/online)

## Backend Endpoints & Events
- REST: `GET/POST /conversations`, `GET/POST /conversations/{id}/messages`
- WS `/ws/chat`: `message:new`, `message:ack`, `presence:update`

## Database Models
- `conversations`, `conversation_members`, `messages(type,text,audio)`

## Testing
- Unit WS handlers; message ordering; presence.
- E2E: send/receive across devices; group membership changes.

## Phases & Estimates
- **P1 (32h):** Text chat 1:1 + groups.  
  **Success:** Messages deliver in <1s; persisted; unread counts correct.
- **P2 (16h):** Audio notes + presence.  
  **Success:** Audio record/play; typing indicators functional.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md` for users; `integration-spec.md` for DTOs.
