# app/models/task.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime
from app.models.pyobjectid import PyObjectId

class CommentModel(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )

class TaskModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]
    status: Literal["Pending", "In Progress", "Completed"]
    created_by: PyObjectId
    assigned_to: PyObjectId
    comments: List[CommentModel] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
