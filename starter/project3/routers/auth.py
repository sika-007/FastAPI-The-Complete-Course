from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from db.get_db import get_db
from typing import Annotated
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/auth", tags=["auth"])
db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = 'HS256'


class CreateUserRequest(BaseModel):
    username: str = Field()
    email: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    password: str = Field()
    phone_number: str = Field()
    role: str = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "username": "sika_007",
                "email": "nsikaktheman@gmail.com",
                "first_name": "Nsikak",
                "last_name": "Thomas",
                "password": "averystrongone1234",
                "phone_number": "+234-8167739545",
                "role": "user"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User could not be validated")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    new_user_record = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(new_user_record)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    authenticated_user = authenticate_user(
        form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username or password is incorrect")
    token = create_access_token(
        # type: ignore
        authenticated_user.username, authenticated_user.id, authenticated_user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
