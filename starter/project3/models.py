from database import Base
from sqlalchemy import Column, Integer

class Todos(Base):
  __tablename__ = "todos"

  # id = Column(Integer, primary_key=True, inde)
