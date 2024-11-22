# app/models/activity.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.models.pyobjectid import PyObjectId

class ActivityModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    activity_name: str
    description: Optional[str] = None
    tasks: List[PyObjectId] = Field(default_factory=list)
    manager_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
