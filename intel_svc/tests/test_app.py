import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

class IntelServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_detections(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())