from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'  ------> Sqlite
# ------> Postgres
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:nsikak123*@localhost/TodoApplicationDatabase"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:nsikak123*@127.0.0.1:3306/todoapplicationdatabase"  # ------> MySQL

# connect_args={"check_same_thread": False} ------> Sqlite (arg for create_engine ONLY FOR SQLITE)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
