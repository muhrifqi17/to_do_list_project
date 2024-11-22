# app/models/user.py

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Literal
from app.models.pyobjectid import PyObjectId

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password_hash: str
    roles: List[Literal["admin", "manager", "user"]] = Field(default_factory=list)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
