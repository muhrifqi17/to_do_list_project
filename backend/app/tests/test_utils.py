# app/tests/test_utils.py

import unittest
from app.core.utils import is_valid_object_id, get_object_id
from bson.objectid import ObjectId

class TestUtils(unittest.TestCase):

    def test_object_id_validation(self):
        valid_id = "507f1f77bcf86cd799439011"
        invalid_id = "invalidobjectid"

        self.assertTrue(is_valid_object_id(valid_id))
        self.assertFalse(is_valid_object_id(invalid_id))

    def test_get_object_id(self):
        id_str = "507f1f77bcf86cd799439011"
        obj_id = get_object_id(id_str)
        self.assertIsInstance(obj_id, ObjectId)
        self.assertEqual(str(obj_id), id_str)

if __name__ == '__main__':
    unittest.main()
