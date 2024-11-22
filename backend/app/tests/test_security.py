# app/tests/test_security.py

import unittest
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token

class TestSecurity(unittest.TestCase):

    def test_password_hashing(self):
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed))

    def test_jwt_token(self):
        user_id = "user123"
        token = create_access_token(user_id)
        decoded_user_id = decode_access_token(token)
        self.assertEqual(user_id, decoded_user_id)

if __name__ == '__main__':
    unittest.main()
