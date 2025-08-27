# onboarding-spec.md — First-Time Tutorial Flow

## Overview
Three-step tutorial: **Welcome** → **Navigation Guide** → **Profile Setup Prompt**.

**UI Reference:** Copy `specs/ui-reference/design.png` exactly. Dark red (`#7A001C` ~ `#98002E`) + neon pink (`#FF2E79`),
pixel-art accents, high contrast, retro scanline overlays where applicable. Rounded 8px radii, 2px neon outlines on focus.

## Frontend Components
- `OnboardingStepper`, animated pixel transitions
- Store `onboarding_complete` flag in profile/user

## Backend
- `PUT /profiles/me` sets `onboarding_complete=true` when done

## Testing
- First login shows flow; subsequent logins skip; manual reset available for tests.

## Phases & Estimates
- **P1 (12h):** Static flow + gating.  
  **Success:** New users guided through 3 screens.
- **P2 (8h):** Instrumentation (time spent, drop-off).  
  **Success:** Events visible in backend counters.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- `auth-spec.md`, `profile-spec.md` for profile completion.
