from fastapi import APIRouter, Depends, HTTPException
from db.get_db import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from starlette import status
from models import Users


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(prefix="/users", tags=["/users"])


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
        "role": user_record.role
    }
    return db_user
