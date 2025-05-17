from app import config
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


engine = create_engine(config.CONFIG_ENV.get("DB_URL"), connect_args={
                       "check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
