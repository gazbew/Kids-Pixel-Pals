# frontend-spec.md — Next.js 14 + TS + Shadcn UI + Tailwind

## Architecture
- **Next.js 14 App Router** with server components for data fetching where appropriate.
- **TypeScript** strict mode; ESLint + Prettier.
- **UI:** Shadcn UI components themed via Tailwind tokens; retro theme applied app-wide.
- **State:** React Query (TanStack) for data; Context for auth/session; simple Zustand store for ephemeral UI state.
- **Realtime:** Socket.IO client for chat/stream events; native WebRTC APIs for media.
- **Routing Proposal**
  - `/` → Onboarding router; directs to login if not authed.
  - `/auth/login` → centered login + social buttons.
  - `/onboarding` → welcome → navigation guide → profile setup prompt.
  - `/profile/create` and `/profile` → photo upload + game credentials.
  - `/chats` → chat selection (people/groups).
  - `/chats/[id]` → conversation (text/audio) + **Share Live** CTA.
  - `/calls/[id]` → video calling screen.
  - `/live` → **dedicated live gameplay** stream screen.
  - `/screenshots` → gallery view & detail.
  - `/parent` → parental dashboard & child creation.
  - `/admin` → ultimate admin control.

## Theming & Styles
- Tailwind config exposes tokens:
  ```ts
  // tailwind.config excerpt
  colors: {{ retroRed: '#98002E', retroDark: '#2A0010', neonPink: '#FF2E79' }}
  ```
- Focus rings: 2px neon pink outline.
- Retro scanline background (CSS overlay) on live/call screens.

## Components (examples)
- `RetroButton`, `RetroCard`, `CenteredAuthForm`, `AvatarUpload`, `GameCredentialList`,
  `ChatList`, `ChatComposer`, `MessageBubble`, `CallControls`, `StreamViewer`, `ReactionTray`, `ScreenshotTile`,
  `ParentChildLinker`, `AdminTable`, `AuditLogTable`, `BillingTab` (future).

## Accessibility
- Minimum contrast ratio 4.5:1. ARIA labels on all inputs & toggles.
- Keyboard navigability for chat, call controls, and stream UI.

## Testing
- **Unit:** Vitest + React Testing Library.
- **E2E:** Playwright (login, onboarding, chat send/receive, live stream start/stop).
- **Accessibility:** `@axe-core/playwright` checks for core screens.

## Analytics (privacy-preserving)
- Local event log for UX metrics (e.g., call join time), shipped to backend as anonymized counters.

## Error Handling
- Toasts for transient issues, modals for blocking errors.
- Retry with backoff for network calls; offline badges.

## Phases & Estimates
- **Phase 1 (40h):** Auth screens, onboarding, profiles, chat list & conversation, screenshot gallery base.  
  **Success:** User can sign in, complete onboarding, chat, and upload a screenshot.
- **Phase 2 (60h):** Call UI, **Live Gameplay** screen, reactions, viewer list.  
  **Success:** Users can call & broadcast with stable controls and reactions.
- **Phase 3 (40h):** Parent dashboard UI, Admin panel UI, Audit log table + export.  
  **Success:** Parents/Admin can manage accounts & see logs.
- **Phase 4 (24h):** Billing tab (hidden by feature flag), polish.  
  **Success:** Billing UI renders from mock/fake endpoints when enabled.

> **Git rule:** Commit every 30 minutes with a concise, action-oriented message (Conventional Commits style).

## Dependencies
- Relies on `backend-spec.md` endpoints and Socket namespaces.
- Needs `integration-spec.md` contracts for DTOs and event names.
