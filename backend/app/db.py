import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "kanban.db"

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
