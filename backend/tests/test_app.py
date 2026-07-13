import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_root_serves_frontend(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Kanban Studio", response.text)

    def test_hello_endpoint(self):
        response = self.client.get("/api/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "hello from backend"})


if __name__ == "__main__":
    unittest.main()
