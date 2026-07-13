import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "kanban.db"

DEFAULT_BOARD = {
    "columns": [
        {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
        {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
        {"id": "col-progress", "title": "In Progress", "cardIds": ["card-4", "card-5"]},
        {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
        {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
    ],
    "cards": {
        "card-1": {
            "id": "card-1",
            "title": "Align roadmap themes",
            "details": "Draft quarterly themes with impact statements and metrics.",
        },
        "card-2": {
            "id": "card-2",
            "title": "Gather customer signals",
            "details": "Review support tags, sales notes, and churn feedback.",
        },
        "card-3": {
            "id": "card-3",
            "title": "Prototype analytics view",
            "details": "Sketch initial dashboard layout and key drill-downs.",
        },
        "card-4": {
            "id": "card-4",
            "title": "Refine status language",
            "details": "Standardize column labels and tone across the board.",
        },
        "card-5": {
            "id": "card-5",
            "title": "Design card layout",
            "details": "Add hierarchy and spacing for scanning dense lists.",
        },
        "card-6": {
            "id": "card-6",
            "title": "QA micro-interactions",
            "details": "Verify hover, focus, and loading states.",
        },
        "card-7": {
            "id": "card-7",
            "title": "Ship marketing page",
            "details": "Final copy approved and asset pack delivered.",
        },
        "card-8": {
            "id": "card-8",
            "title": "Close onboarding sprint",
            "details": "Document release notes and share internally.",
        },
    },
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS boards (
  user_id TEXT PRIMARY KEY,
  board_json TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def ensure_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(SCHEMA)
        connection.commit()


def get_connection() -> sqlite3.Connection:
    ensure_db()
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def get_board(user_id: str) -> Optional[Any]:
    ensure_db()
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            "SELECT board_json FROM boards WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if not row:
            return None
        return json.loads(row[0])


def get_or_create_board(user_id: str) -> Any:
    board = get_board(user_id)
    if board is not None:
        return board
    upsert_board(user_id, DEFAULT_BOARD)
    return DEFAULT_BOARD


def upsert_board(user_id: str, board_data: Any) -> None:
    ensure_db()
    board_json = json.dumps(board_data)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO boards (user_id, board_json) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET board_json = excluded.board_json, updated_at = CURRENT_TIMESTAMP",
            (user_id, board_json),
        )
        connection.commit()
