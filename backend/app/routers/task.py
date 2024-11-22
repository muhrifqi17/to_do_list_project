# app/routers/task.py

from fastapi import APIRouter, HTTPException, Depends
from app.models.task import TaskModel
from app.db.connection import mongodb
from app.models.pyobjectid import PyObjectId

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post("/", response_model=TaskModel)
async def create_task(task: TaskModel):
    task_dict = task.dict(by_alias=True)
    result = await mongodb.db["tasks"].insert_one(task_dict)
    task.id = result.inserted_id
    return task
