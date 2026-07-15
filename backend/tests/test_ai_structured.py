import json
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


class AiStructuredTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=False)
    @patch("backend.app.main.urllib.request.urlopen")
    def test_ai_chat_returns_structured_reply(self, mock_urlopen) -> None:
        response_payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "message": "Added a card",
                                "board_update": {
                                    "columns": [
                                        {
                                            "id": "col-backlog",
                                            "title": "Backlog",
                                            "cardIds": ["card-1", "card-2", "card-999"],
                                        }
                                    ],
                                    "cards": {
                                        "card-999": {
                                            "id": "card-999",
                                            "title": "New card",
                                            "details": "Added by AI",
                                        }
                                    },
                                },
                            }
                        )
                    }
                }
            ]
        }

        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = json.dumps(response_payload).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        response = self.client.post(
            "/api/ai/chat",
            json={"prompt": "add a card", "user_id": "user"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Added a card")
        self.assertEqual(response.json()["applied"], True)
        self.assertEqual(response.json()["board"]["cards"]["card-999"]["title"], "New card")

    def test_ai_chat_rejects_invalid_payload(self) -> None:
        response = self.client.post(
            "/api/ai/chat",
            json={"board_update": {"bad": "value"}},
        )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
