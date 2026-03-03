from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
# Connecting fastapi to postgresql database -> Just want to change the url
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
engine = create_engine(SQLALCHEMY_DATABASE_URL) # In postgresql, no need gor connect_args,remove it

sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

