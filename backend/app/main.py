# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.db.connection import connect_to_mongo, close_mongo_connection

from app.routers import user, task  # Make sure 'user' is imported

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(user.router)

# app.include_router(task.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the ToDo List Application"}
