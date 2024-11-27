# app/models/task.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime
from bson import ObjectId
from app.models.pyobjectid import PyObjectId

class CommentModel(BaseModel):
    user_id: PyObjectId
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TaskCreateModel(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]
    status: Literal["Pending", "In Progress", "Completed"] = "Pending"
    assigned_to: Optional[PyObjectId] = None

class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["High", "Medium", "Low"]] = None
    status: Optional[Literal["Pending", "In Progress", "Completed"]] = None
    assigned_to: Optional[PyObjectId] = None

class TaskResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    priority: Literal["High", "Medium", "Low"]
    status: Literal["Pending", "In Progress", "Completed"]
    created_by: PyObjectId
    assigned_to: PyObjectId
    comments: List[CommentModel] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str},
    )
