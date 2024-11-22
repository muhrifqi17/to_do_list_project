# app/tests/test_config.py

import unittest
from app.core.config import settings

class TestConfig(unittest.TestCase):

    def test_settings(self):
        self.assertIsNotNone(settings.APP_NAME)
        self.assertIsNotNone(settings.MONGODB_URI)
        self.assertIsNotNone(settings.JWT_SECRET_KEY)

if __name__ == '__main__':
    unittest.main()
