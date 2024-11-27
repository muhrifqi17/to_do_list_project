# app/routers/user.py

from fastapi import APIRouter, HTTPException, status, Depends, Path
from app.models.user import UserCreateModel, UserResponseModel
from app.core.security import get_password_hash
from app.db.connection import mongodb
from app.core.roles import has_roles
from app.models.user import UserUpdateModel
from app.models.pyobjectid import PyObjectId

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/register", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreateModel):
    existing_user = await mongodb.db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    user_dict = {
        "email": user.email,
        "password_hash": hashed_password,
        "roles": user.roles,
    }
    result = await mongodb.db["users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return UserResponseModel(**user_dict)


# Get current user info
@router.get("/me", response_model=UserResponseModel)
async def read_users_me(
    current_user: UserResponseModel = Depends(has_roles(["admin", "user", "manager"]))
):
    return current_user

# Get user by ID (Admin only)
@router.get("/{user_id}", response_model=UserResponseModel)
async def get_user(
    user_id: str, 
    current_user: UserResponseModel = Depends(has_roles(["admin"]))
):  
    user = await mongodb.db["users"].find_one({"_id": PyObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseModel(**user)

# update user by ID (Admin only)
@router.put("/{user_id}", response_model=UserResponseModel)
async def update_user(
    user_id: str, 
    user_update: UserUpdateModel, 
    current_user: UserResponseModel = Depends(has_roles(["admin"]))
):
    update_data = user_update.dict(exclude_unset=True)
    # self-update
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    await mongodb.db["users"].update_one({"_id": PyObjectId(user_id)}, {"$set": update_data})
    user = await mongodb.db["users"].find_one({"_id": PyObjectId(user_id)})
    return UserResponseModel(**user)


# delete user by ID (Admin only)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: UserResponseModel = Depends(has_roles(["admin"]))
):
    result = await mongodb.db["users"].delete_one({"_id": PyObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return