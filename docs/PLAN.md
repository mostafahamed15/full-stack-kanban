# High level steps for project

This document defines the 10-part MVP plan and tracks the detailed work required to ship the project. The first part is to expand the plan, create the frontend agent doc, and establish the test and acceptance criteria.

## General goals

- Ship a single-user MVP Kanban app with a user login, one board, drag/drop cards, column renaming, and AI chat.
- Use Next.js frontend, Python FastAPI backend, static asset serving, Docker packaging, SQLite storage, and OpenRouter for AI.
- Keep implementation simple, idiomatic, and minimal.
- Achieve at least 80% frontend unit test coverage.

## Part 1: Plan and audit

- [ ] Review existing frontend code, tests, and package setup.
- [ ] Create `frontend/AGENTS.md` documenting current frontend architecture and the planned frontend work.
- [ ] Expand this plan into checklist steps with clear tests and success criteria for each part.
- [ ] Confirm current repo state and surface any gaps before implementation.
- [ ] Get user approval of the updated plan before starting code work.

Success criteria:

- `docs/PLAN.md` contains a detailed task list for all 10 parts.
- `frontend/AGENTS.md` exists and documents current frontend components, state, and planned evolution.
- The plan explicitly requires 80% frontend unit coverage.

## Part 2: Scaffolding

- [x] Add backend skeleton in `backend/` with FastAPI and `uv` package management.
- [x] Create Docker files to run backend and serve static content.
- [x] Add `scripts/` start and stop scripts for Windows/macOS/Linux.
- [x] Add a backend health endpoint and a static HTML endpoint for verification.

Tests:

- Run the backend locally and verify `GET /` returns static HTML.
- Verify `GET /api/health` returns a success response.
- Confirm Docker container starts and responds to both endpoints.

Success criteria:

- Backend starts successfully and serves example static content.
- API health route works.
- Docker build and run commands exist and are documented.

## Part 3: Add in Frontend

- [x] Build the existing Next.js frontend into static assets.
- [x] Configure FastAPI to serve the built frontend from `/`.
- [x] Ensure the Kanban board page loads when the app is served from backend.
- [x] Add unit tests and integration checks for the static site build path.

Tests:

- Frontend build succeeds with `npm run build`.
- Served root page includes the Kanban board and the `Kanban Studio` heading.
- Unit tests cover board rendering and component-level behavior.

Success criteria:

- `GET /` returns the built frontend and shows the Kanban board.
- Frontend unit test coverage is tracked and moving toward 80%.

## Part 4: Add fake user sign in experience

- [x] Add a login flow with dummy credentials: `user` / `password`.
- [x] Protect the Kanban route so users must log in first.
- [x] Add logout functionality and persistent session state in the browser.
- [x] Keep the user experience simple; no real auth backend required yet.

Tests:

- Login page renders and validates credentials.
- Correct credentials allow access to the board.
- Wrong credentials stay on the login page and show an error.
- Logout returns the user to the login screen.

Success criteria:

- Unauthenticated users cannot see the Kanban board.
- Login and logout work in the browser.
- The login flow is covered by unit tests and at least one end-to-end test.

## Part 5: Database modeling

- [x] Design a SQLite schema or JSON-based schema for board data.
- [x] Store board state as JSON inside SQLite to simplify the MVP.
- [x] Add documentation in `docs/` describing the schema and persistence strategy.
- [x] Ensure the database file is created automatically when the app starts.

Tests:

- Schema definition is documented in `docs/`.
- The backend can create and open the SQLite file.
- Data read/write operations succeed on an empty database.

Success criteria:

- Database schema and approach are documented.
- The app creates the database automatically.
- Schema choice is approved before backend implementation.

## Part 6: Backend API

- [x] Implement backend routes for reading and updating the Kanban board by user.
- [x] Add endpoints for: `GET /api/board`, `POST /api/board`, `PATCH /api/board`, and health checks.
- [x] Implement user scoping support in the backend so data can be saved per dummy user.
- [x] Add backend unit tests for API behavior and persistence.

Tests:

- `GET /api/board` returns the expected board JSON for the signed-in user.
- `POST` or `PATCH` updates board state and persists it.
- Invalid payloads return appropriate errors.

Success criteria:

- Backend API supports read/write of board state.
- Backend tests cover API behavior and persistence logic.
- The database is updated when the board changes.

## Part 7: Frontend + Backend

- [x] Replace local board state with backend-backed data fetching.
- [x] Add API client utilities or hooks to fetch and mutate board state.
- [x] Sync column renaming, card creation, deletion, and drag/drop moves with the backend.
- [x] Keep the frontend responsive and fallback safely during load states.

Tests:

- [x] Board state loads from backend on page load.
- [x] User actions update the board and persist through refresh.
- [x] API request failures are handled gracefully.

Success criteria:

- [x] Frontend uses backend API for the Kanban board.
- [x] User actions persist across page reloads.
- [x] Frontend unit tests cover API integration logic.

## Part 8: AI connectivity

- [x] Add backend integration with OpenRouter using `OPENROUTER_API_KEY`.
- [x] Implement a simple AI test endpoint such as `POST /api/ai/test` or `POST /api/ai/chat`.
- [x] Verify that the backend can call OpenRouter successfully.

Tests:

- [x] AI connectivity test returns a valid response for a simple prompt like `2+2`.
- [x] The backend handles API errors cleanly.

Success criteria:

- [x] Backend can reach OpenRouter and return a valid AI response.
- [x] AI call behavior is covered by backend tests.

## Part 9: AI structured outputs

- [ ] Define structured output format for AI chat responses.
- [ ] Send the current board JSON, user question, and conversation context to the AI.
- [ ] Parse AI responses into user-facing text and optional board updates.
- [ ] Allow board updates from AI response to be returned via the backend.

Tests:

- Structured output parsing tests handle valid AI JSON responses.
- Backend applies AI-suggested board updates correctly.
- AI response payloads are validated before applying changes.

Success criteria:

- AI backend route returns both text and structured board update data.
- The AI response format is documented.
- The backend safely applies valid board updates.

## Part 10: AI chat UI

- [ ] Add a sidebar chat UI for user/AI conversation.
- [ ] Display recent chat messages, send button, and loading state.
- [ ] Allow the backend to apply AI-proposed board changes and refresh UI automatically.
- [ ] Ensure the chat UI is visually polished and simple.

Tests:

- Chat UI renders and sends messages.
- AI responses appear in chat history.
- AI-suggested board updates refresh the board.

Success criteria:

- The app has a working AI chat sidebar.
- AI messages are visible and applied to the board when needed.
- The integration is covered by frontend unit tests and at least one end-to-end flow.

## Quality checklist

- [ ] Frontend unit test coverage should target at least 80%.
- [ ] Backend tests should validate all API and persistence behavior.
- [ ] Keep the README minimal and update only as needed.
- [ ] Avoid unnecessary complexity and extra features beyond the MVP.
