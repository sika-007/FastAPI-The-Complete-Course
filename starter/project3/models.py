from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, default=None)
    priority = Column(Integer, default=None)
    complete = Column(Boolean, default=False)
