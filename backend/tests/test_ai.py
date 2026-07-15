import json
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


class AiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}, clear=False)
    @patch("backend.app.main.urllib.request.urlopen")
    def test_ai_test_endpoint_returns_reply(self, mock_urlopen) -> None:
        response_payload = {
            "choices": [
                {
                    "message": {
                        "content": "4",
                    }
                }
            ]
        }

        mock_response = unittest.mock.MagicMock()
        mock_response.read.return_value = json.dumps(response_payload).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        response = self.client.post("/api/ai/test", json={"prompt": "2+2"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reply"], "4")
        self.assertEqual(response.json()["model"], "openai/gpt-oss-120b")

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": ""}, clear=False)
    def test_ai_test_endpoint_requires_api_key(self) -> None:
        response = self.client.post("/api/ai/test", json={"prompt": "2+2"})

        self.assertEqual(response.status_code, 500)
        self.assertIn("OPENROUTER_API_KEY", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
