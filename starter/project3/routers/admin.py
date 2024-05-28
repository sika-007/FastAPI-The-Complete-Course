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
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed"
        )
    todo_record = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
