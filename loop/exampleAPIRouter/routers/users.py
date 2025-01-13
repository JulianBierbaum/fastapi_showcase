from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routers import FastApiAuthorization
from typing import List

router = APIRouter()

class User(BaseModel):
    display_name: str
    password: str
    is_admin: bool
    microsoft_account: bool | None = None
    archived: str | None = None
    last_active: str | None = None
    is_email_verified: bool | None = None
    mobile_number: str | None = None

user_list: List[User] = []

@router.get("/get_all_users")
async def get_all_users():
    return {"users": user_list}

@router.get("/get_user/{display_name}")
async def get_user(display_name: str):
    for user in user_list:
        if user.display_name == display_name:
            return {"item": user}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/create_user", dependencies=[Depends(FastApiAuthorization.is_admin)])
async def create_user(user: User):
    user_list.append(user)
    return {"message": "User added successfully", "item": user}
