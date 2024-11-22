# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserModel
from app.core.security import get_password_hash
from app.db.connection import mongodb

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/register", response_model=UserModel)
async def register_user(user: UserModel):
    # Check if the email already exists
    existing_user = await mongodb.db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user.password_hash = get_password_hash(user.password_hash)
    user_dict = user.dict(by_alias=True)
    result = await mongodb.db["users"].insert_one(user_dict)
    user.id = result.inserted_id
    return user
