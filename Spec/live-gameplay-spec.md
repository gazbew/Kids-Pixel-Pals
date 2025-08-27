# live-gameplay-spec.md — Dedicated Live Gameplay Streaming

## Overview
A **separate screen** for live gameplay broadcasting with **viewer chat, reactions, and viewer list**.
Conversation screen includes a **Share Live** button to navigate here.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `LiveStreamPage` with central video canvas (scanline overlay)
- `ReactionTray` (pixel emojis), `LiveChatSidebar`, `ViewerList`
- `StreamerPanel` controls: start/stop, mic/cam, share screen, **Take Screenshot**

## Backend Endpoints & Events
- `POST /streams/start` → returns `stream_id`
- `POST /streams/stop`
- WS `/ws/stream`: `stream:live`, `stream:ended`, `reaction:new`, `viewer:list`

## Database Models
- `streams(streamer_id,title,started_at,ended_at,status)`

## Testing
- Stream start/stop across 10 viewers; reactions; chat throughput.
- Screenshot action posts to screenshots service.

## Phases & Estimates
- **P1 (40h):** Stream core + viewer join/leave.  
  **Success:** 720p @ 30fps baseline; 10 viewers stable.
- **P2 (24h):** Reactions + chat sidebar + screenshot hook.  
  **Success:** Reactions overlay; screenshot saved to gallery.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `chat-spec.md` (for chat components), `screenshots-spec.md`, TURN infra.
