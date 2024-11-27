# app/models/user.py

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Literal, Optional
from app.models.pyobjectid import PyObjectId
from bson import ObjectId

class UserCreateModel(BaseModel):
    email: EmailStr
    password: str  # Plain password input
    # for developing remove "admin"
    roles: List[Literal["admin", "manager", "user"]] = Field(default_factory=list)

class UserResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    email: EmailStr
    roles: List[Literal["admin", "manager", "user"]]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class UserUpdateModel(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roles: Optional[List[Literal["manager", "user"]]] = None