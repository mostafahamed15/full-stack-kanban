import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class ApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_board_returns_default_board(self) -> None:
        response = self.client.get("/api/board")
        self.assertEqual(response.status_code, 200)
        self.assertIn("columns", response.json())
        self.assertIn("cards", response.json())

    def test_patch_board_updates_board(self) -> None:
        board_payload = {
            "columns": [
                {"id": "col-backlog", "title": "Backlog", "cardIds": []}
            ],
            "cards": {},
        }

        response = self.client.patch("/api/board", json=board_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), board_payload)

        read_response = self.client.get("/api/board")
        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(read_response.json(), board_payload)


if __name__ == "__main__":
    unittest.main()
