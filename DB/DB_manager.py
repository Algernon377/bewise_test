import asyncio
import os
from dotenv import load_dotenv


from sqlalchemy import select

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from DB.models.base_model import Base
from DB.models.models_list import all_table_dict

load_dotenv()
PG_HOST = os.getenv('POSTGRESQL_HOST')
PG_USER = os.getenv('POSTGRESQL_USER')
PG_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
PG_DB_NAME = os.getenv('POSTGRESQL_DB_NAME')
PG_PORT = os.getenv('POSTGRESQL_PORT')

PG_URL_FOR_ENGINE = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

engine = create_async_engine(PG_URL_FOR_ENGINE, echo=True, future=True)
async_session_maker = async_sessionmaker(
                                        engine,
                                        expire_on_commit=False,
                                        class_=AsyncSession,
                                        )

