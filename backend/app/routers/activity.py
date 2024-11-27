# app/routers/activity.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from app.models.activity import (
    ActivityCreateModel,
    ActivityUpdateModel,
    ActivityResponseModel,
)
from app.core.auth import get_current_user
from app.core.roles import has_roles
from app.db.connection import mongodb
from app.models.pyobjectid import PyObjectId
from bson.errors import InvalidId
from app.models.user import UserResponseModel

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)

# Create Activity
@router.post(
    "/",
    response_model=ActivityResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_activity(
    activity: ActivityCreateModel,
    current_user: UserResponseModel = Depends(has_roles(["manager", "admin"])),
):
    activity_dict = activity.dict()
    activity_dict["manager_id"] = current_user.id
    activity_dict["created_at"] = datetime.utcnow()
    activity_dict["updated_at"] = datetime.utcnow()
    result = await mongodb.db["activities"].insert_one(activity_dict)
    activity_dict["_id"] = result.inserted_id
    return ActivityResponseModel(**activity_dict)

# Get All Activities
@router.get("/", response_model=List[ActivityResponseModel])
async def get_activities(current_user: UserResponseModel = Depends(get_current_user)):
    query = {}
    if "admin" not in current_user.roles:
        query["manager_id"] = current_user.id
    activities_cursor = mongodb.db["activities"].find(query)
    activities = await activities_cursor.to_list(length=100)
    return [ActivityResponseModel(**activity) for activity in activities]

# Get Activity by ID
@router.get("/{activity_id}", response_model=ActivityResponseModel)
async def get_activity(
    activity_id: str,
    current_user: UserResponseModel = Depends(get_current_user),
):
    try:
        activity_obj_id = PyObjectId(activity_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid activity ID")

    activity = await mongodb.db["activities"].find_one({"_id": activity_obj_id})
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if (
        activity["manager_id"] != current_user.id
        and "admin" not in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Not authorized")

    return ActivityResponseModel(**activity)

# Update Activity
@router.put("/{activity_id}", response_model=ActivityResponseModel)
async def update_activity(
    activity_id: str,
    activity_update: ActivityUpdateModel,
    current_user: UserResponseModel = Depends(has_roles(["manager", "admin"])),
):
    try:
        activity_obj_id = PyObjectId(activity_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid activity ID")

    activity = await mongodb.db["activities"].find_one({"_id": activity_obj_id})
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity["manager_id"] != current_user.id and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = activity_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    await mongodb.db["activities"].update_one(
        {"_id": activity_obj_id}, {"$set": update_data}
    )
    updated_activity = await mongodb.db["activities"].find_one({"_id": activity_obj_id})
    return ActivityResponseModel(**updated_activity)

# Delete Activity
@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: str,
    current_user: UserResponseModel = Depends(has_roles(["manager", "admin"])),
):
    try:
        activity_obj_id = PyObjectId(activity_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid activity ID")

    activity = await mongodb.db["activities"].find_one({"_id": activity_obj_id})
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity["manager_id"] != current_user.id and "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")

    await mongodb.db["activities"].delete_one({"_id": activity_obj_id})
    return
