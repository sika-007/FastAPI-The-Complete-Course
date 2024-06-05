from fastapi import FastAPI
from app.routers import auth, admin, todos, users
from app.models import Base
from app.db.database import engine

app = FastAPI(title="Todos Application")

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
