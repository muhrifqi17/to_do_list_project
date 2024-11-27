# app/models/activity.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.pyobjectid import PyObjectId
from bson import ObjectId

class ActivityCreateModel(BaseModel):
    activity_name: str
    description: Optional[str] = None
    tasks: Optional[List[PyObjectId]] = Field(default_factory=list)
    # manager_id will be set automatically to the current user's ID

class ActivityUpdateModel(BaseModel):
    tasks: Optional[List[PyObjectId]] = None
    # manager_id should not be updated through this model

class ActivityResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    activity_name: str
    description: Optional[str] = None
    tasks: List[PyObjectId] = Field(default_factory=list)
    manager_id: PyObjectId
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
