from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import Field, BaseModel
from db.get_db import get_db
from models import Todos
from starlette import status
from fastapi import APIRouter, Path, HTTPException, Depends
from routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") is not "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(Todos).all()
