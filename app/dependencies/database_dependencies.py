from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app import config

DBSessionDep = Annotated[AsyncSession, Depends(config.get_db_session)]
