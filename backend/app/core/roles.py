from fastapi import Depends, HTTPException
from app.core.auth import get_current_user
from typing import List

def has_roles(required_roles: List[str]):
    async def role_checker(current_user=Depends(get_current_user)):
        if not any(role in current_user.roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Not authorized")
        return current_user # Return the current user
    return role_checker