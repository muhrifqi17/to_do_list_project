# app/core/utils.py

from bson.objectid import ObjectId
from typing import Any

def is_valid_object_id(id_str: str) -> bool:
    return ObjectId.is_valid(id_str)

def get_object_id(id_str: str) -> ObjectId:
    return ObjectId(id_str)
