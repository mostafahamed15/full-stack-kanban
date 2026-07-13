# Database schema and persistence

This project uses SQLite for the MVP database. Board state is stored as JSON in a single table so the backend can read and write user board data without a complex relational schema.

## Storage location

- Database file: `backend/data/kanban.db`
- Created automatically on backend startup or when the first database operation runs.

## Schema

- Table: `boards`
  - `user_id` TEXT PRIMARY KEY
  - `board_json` TEXT NOT NULL
  - `updated_at` TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## Persistence strategy

- The `boards` table stores one row per user.
- Each board state is serialized as JSON in the `board_json` column.
- This keeps the MVP simple while allowing structured board updates later.
- The backend creates the database directory and file automatically using `ensure_db()`.

## Backend behavior

- `ensure_db()` creates `backend/data/kanban.db` and the `boards` table.
- `get_board(user_id)` returns the parsed board JSON or `null` if no row exists.
- `upsert_board(user_id, board_data)` saves the board state for the specified user.
