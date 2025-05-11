from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

engine = create_engine(os.getenv("DB_URL"), connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()