from fastapi import FastAPI
import models
from routers import auth, todos
from db.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
