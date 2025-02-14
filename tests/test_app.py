import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_status_code(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_response_json(self):
        response = self.app.get("/")
        self.assertTrue(response.is_json)  # ❌ This will fail because app.py returns text, not JSON

if __name__ == "__main__":
    unittest.main()
