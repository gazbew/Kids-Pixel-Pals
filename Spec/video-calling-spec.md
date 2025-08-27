# video-calling-spec.md — WebRTC Calls + Screen Share

## Overview
**One-on-one and group** video calls with **screen sharing** during calls. Retro pixel frames.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `CallView` grid, `CallControls` (mute, cam, share, leave)
- Device picker modal; permission prompts

## Backend & Signaling
- WS `/ws/call`: `signal:offer|answer|ice`, `call:end`
- TURN server (Coturn) configured for NAT traversal

## Database Models
- `calls(id, type, started_by, started_at, ended_at, stats_json)`

## Testing
- Simulated group call with 3–6 peers; bandwidth checks; screen share toggle.

## Phases & Estimates
- **P1 (32h):** 1:1 calls.  
  **Success:** Stable P2P incl. poor network fallback via TURN.
- **P2 (32h):** Group calls.  
  **Success:** 4–6 participants, adaptive layout.
- **P3 (16h):** Screen share toggle + UI polish.  
  **Success:** Share works across OS/browsers; quick re-negotiation.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md`, `integration-spec.md`, TURN infra from `backend-spec.md`.
