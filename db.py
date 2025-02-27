from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
import os, logging

DATABASE_URL = os.environ.get("DATABASE_URL")

logging.basicConfig(level = logging.DEBUG)
logging.info("데이터베이스 : ", DATABASE_URL)

# 대충 비동기로 만들 거라는 뜻
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

database = Database(DATABASE_URL)

async def get_db() :
    async with SessionLocal() as session :
        yield session
