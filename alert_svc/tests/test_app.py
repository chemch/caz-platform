# alert_svc/tests/test_app.py

import unittest
import sys
import os

# Add the alert_svc directory to the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # ✅ direct import from alert_svc/main.py

class AlertServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_alerts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        print(response.get_json())