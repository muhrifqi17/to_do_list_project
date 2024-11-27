# app/routers/task.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from app.models.task import TaskCreateModel, TaskUpdateModel, TaskResponseModel, CommentModel
from app.models.user import UserResponseModel
from app.core.auth import get_current_user
from app.core.roles import has_roles
from app.db.connection import mongodb
from app.models.pyobjectid import PyObjectId
from bson.errors import InvalidId

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

# Create Task
@router.post("/", response_model=TaskResponseModel, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreateModel,
    current_user=Depends(get_current_user),
    _ = Depends(has_roles(["admin", "manager"]))
):
    task_dict = task.dict()
    task_dict["created_by"] = current_user.id
    task_dict["assigned_to"] = task.assigned_to or current_user.id
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    result = await mongodb.db["tasks"].insert_one(task_dict)
    task_dict["_id"] = result.inserted_id
    return TaskResponseModel(**task_dict)

# Endpoint untuk menambahkan komentar ke task
@router.post("/{task_id}/comments", response_model=TaskResponseModel)
async def add_comment(
    task_id: str,
    comment: CommentModel,
    current_user: UserResponseModel = Depends(get_current_user)
):
    try:
        task_obj_id = PyObjectId(task_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Tambahkan informasi user_id dan timestamp ke komentar
    comment.user_id = current_user.id
    comment.timestamp = datetime.utcnow()

    # Tambahkan komentar ke task
    await mongodb.db["tasks"].update_one(
        {"_id": task_obj_id},
        {"$push": {"comments": comment.dict()}}
    )

    # Dapatkan task yang diperbarui
    updated_task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    return TaskResponseModel(**updated_task)


# Read All Tasks (Accessible based on roles)
@router.get("/", response_model=List[TaskResponseModel])
async def get_tasks(
    skip: int = 0,
    limit: int = 5,
    sort_by: str = "project",
    order: int = 1,
    search: Optional[str] = None,
    current_user: UserResponseModel = Depends(get_current_user)
):
    query = {}
    if "admin" not in current_user.roles:
        query["$or"] = [
            {"assigned_to": current_user.id},
            {"created_by": current_user.id}
        ]

    # Tambahkan kondisi pencarian jika parameter 'search' diberikan
    if search:
        query["title"] = {"$regex": search, "$options": "i"}  # 'i' untuk case-insensitive

    # Validasi field sort_by
    allowed_sort_fields = ["project", "priority", "created_at", "updated_at"]
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    # Dapatkan cursor dengan sorting dan pagination
    tasks_cursor = mongodb.db["tasks"].find(query).sort(
        sort_by, order
    ).skip(skip).limit(limit)

    tasks = await tasks_cursor.to_list(length=limit)
    return [TaskResponseModel(**task) for task in tasks]

# Read Task by ID
@router.get("/{task_id}", response_model=TaskResponseModel)
async def get_task(
    task_id: str,
    current_user = Depends(get_current_user),
    _ = Depends(has_roles(["admin", "manager", "user"]))

):
    try:
        task_obj_id = PyObjectId(task_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if (
        task["assigned_to"] != current_user.id
        and task["created_by"] != current_user.id
        and "admin" not in current_user.roles
    ):
        raise HTTPException(status_code=403, detail="Not authorized")

    return TaskResponseModel(**task)

# Update Task
@router.put("/{task_id}", response_model=TaskResponseModel)
async def update_task(
    task_id: str,
    task_update: TaskUpdateModel,
    current_user=Depends(get_current_user),
    _ = Depends(has_roles(["admin", "manager", "user"]))
):
    try:
        task_obj_id = PyObjectId(task_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    await mongodb.db["tasks"].update_one(
        {"_id": task_obj_id}, {"$set": update_data}
    )
    task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    return TaskResponseModel(**task)

# Delete Task
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    _ = Depends(has_roles(["admin", "manager"]))
):
    try:
        task_obj_id = PyObjectId(task_id)
    except (InvalidId, ValueError):
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = await mongodb.db["tasks"].find_one({"_id": task_obj_id})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await mongodb.db["tasks"].delete_one({"_id": task_obj_id})
    return
