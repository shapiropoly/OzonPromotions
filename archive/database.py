import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
# from config import settings

URL_DATABASE = "postgresql://localhost:5432/postgres"


sync_engine = create_engine(
    url=URL_DATABASE,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# async_engine = create_async_engine(
#     url=URL_DATABASE,
#     echo=False,
#     pool_size=5,
#     max_overflow=10,
# )


with sync_engine.connect() as conn:
    res = conn.execute(text("select 1, 2, 3 union select 4, 5, 6"))
    print(f"{res.first()=}")


# async def get_123():
#     async with async_engine.connect() as conn:
#         res = await conn.execute(text("select 1, 2, 3 union select 4, 5, 6"))
#         print(f"{res.first()=}")
#
#
# asyncio.run(get_123())