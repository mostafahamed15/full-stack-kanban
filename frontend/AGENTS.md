# Frontend AGENTS.md

## Purpose

This document describes the existing frontend architecture and the planned work for the Kanban MVP frontend in `frontend/`.

## Current frontend state

- App root: `src/app/page.tsx` renders `KanbanBoard`.
- Main board component: `src/components/KanbanBoard.tsx` manages board state locally.
- Column component: `src/components/KanbanColumn.tsx` renders a board column, supports renaming, drag-and-drop targets, and adding cards.
- Card component: `src/components/KanbanCard.tsx` renders an individual draggable card with delete support.
- New card form: `src/components/NewCardForm.tsx` handles card creation in a simple inline form.
- Card preview: `src/components/KanbanCardPreview.tsx` shows the dragged card in the `DragOverlay`.
- Data model: `src/lib/kanban.ts` defines `Card`, `Column`, `BoardData`, initial sample data, and utility functions (`moveCard`, `createId`).

## What is implemented today

- Full local board state in React state.
- Drag and drop using `@dnd-kit/core` and `@dnd-kit/sortable`.
- Column title editing via controlled inputs.
- Add card flow and remove card flow.
- Empty column placeholder when no cards exist.
- Basic component-level unit tests in `src/test/setup.ts` and `src/components/KanbanBoard.test.tsx`.
- Core logic tests for `moveCard` in `src/lib/kanban.test.ts`.
- End-to-end tests in `frontend/tests/kanban.spec.ts`.

## Current limitations

- No backend integration: board data is not persisted.
- No login/auth flow.
- No AI features or chat UI.
- State is fully local and resets on refresh.
- Coverage is currently unmeasured but needs to be >= 80%.

## Tooling and test strategy

- Unit testing: `vitest` with `@testing-library/react` and a JSDOM environment.
- E2E testing: Playwright.
- Coverage: `@vitest/coverage-v8`.
- Current scripts in `package.json` include `test`, `test:unit`, `test:e2e`, and `test:all`.

## Planned frontend work

### Part 2 / Part 3

- Ensure the frontend can build successfully and be served as static files by the backend.
- Validate that `npm run build` produces a working production artifact.
- Confirm the backend can serve the built app at `/`.

### Part 4

- Add a login page or modal on first load.
- Add lightweight route protection to prevent access to the board before login.
- Keep credentials hardcoded to `user` / `password`.

### Part 7

- Replace local board state with API-backed state fetched from the backend.
- Add a client module for `GET /api/board` and `PATCH /api/board`.
- Keep board interactions responsive and persist updates.

### Part 10

- Add an AI chat sidebar UI in the app shell.
- Send chat messages to the backend AI route and render responses.
- Apply AI-proposed board updates when the backend returns structured output.

## Frontend test coverage goals

- Target at least 80% unit coverage across components and library utilities.
- Add tests for:
  - board rendering and user interaction flows,
  - column renaming,
  - card add/delete,
  - drag/drop state transitions,
  - API integration points once backend is added,
  - login flow and protected board access.

## Notes for implementation

- Use the existing `src/lib/kanban.ts` model as the starting point for board state.
- Keep components small and focused; avoid adding unnecessary abstractions.
- Add new frontend files only as needed for API client, auth state, and chat UI.
- Preserve the current visual language and structure where possible.
