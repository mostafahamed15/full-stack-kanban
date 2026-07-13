import json
import sqlite3
import unittest

from backend.app.db import DB_PATH, ensure_db, get_board, upsert_board


class DatabaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        if DB_PATH.exists():
            DB_PATH.unlink()
        ensure_db()

    def tearDown(self) -> None:
        if DB_PATH.exists():
            DB_PATH.unlink()

    def test_database_file_and_schema_created(self) -> None:
        self.assertTrue(DB_PATH.exists())

        with sqlite3.connect(DB_PATH) as connection:
            row = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='boards'"
            ).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "boards")

    def test_board_read_and_write_operations(self) -> None:
        sample_board = {
            "columns": [],
            "cards": {},
        }

        self.assertIsNone(get_board("user"))
        upsert_board("user", sample_board)
        self.assertEqual(get_board("user"), sample_board)

        updated_board = {"columns": [{"id": "col-backlog", "title": "Backlog", "cardIds": []}], "cards": {}}
        upsert_board("user", updated_board)
        self.assertEqual(get_board("user"), updated_board)


if __name__ == "__main__":
    unittest.main()
