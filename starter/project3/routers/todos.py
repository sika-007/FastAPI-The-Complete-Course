from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import Field, BaseModel
from db.get_db import get_db
from models import Todos
from starlette import status
from fastapi import APIRouter, Path, HTTPException, Depends
from routers.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    todo_data = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")).first()
    if todo_data is not None:
        return todo_data
    raise HTTPException(status_code=404, detail='Todo item not found')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    todo = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    todo_record = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")).first()
    if todo_record is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_record.title = todo_request.title  # type: ignore
    todo_record.description = todo_request.description  # type: ignore
    todo_record.priority = todo_request.priority  # type: ignore
    todo_record.complete = todo_request.complete  # type: ignore

    db.add(todo_record)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    todo_record = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")).first()
    if todo_record is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")).delete()
    db.commit()
