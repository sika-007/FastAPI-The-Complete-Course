from fastapi import APIRouter, Depends, HTTPException, Path
from db.get_db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from starlette import status
from models import Users
from pydantic import BaseModel, Field
from routers.auth import bcrypt_context


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(prefix="/users", tags=["users"])


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=3, max_length=17)
    new_password: str = Field(min_length=3, max_length=17)


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthenticated")
    user_record = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user = {
        "id": user_record.id,
        "email": user_record.email,
        "username": user_record.username,
        "first_name": user_record.first_name,
        "last_name": user_record.last_name,
        "is_active": user_record.is_active,
        "role": user_record.role,
        "phone_number": user_record.phone_number
    }
    return db_user


@router.put("/user/phone", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthenticated")
    user_record = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_record.phone_number = phone_number  # type: ignore
    db.add(user_record)
    db.commit()


@router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, request: PasswordChangeRequest):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    user_record = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User record not found")
    # type: ignore
    if not bcrypt_context.verify(request.current_password, user_record.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You provided a wrong password")
    user_record.hashed_password = bcrypt_context.hash(  # type: ignore
        request.new_password)
    db.add(user_record)
    db.commit()
