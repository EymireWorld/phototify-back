from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME


engine = create_async_engine(
    f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
session_fabric = async_sessionmaker(
    engine,
    autoflush= False,
    autocommit= False,
    expire_on_commit= False
)


async def get_session():
    session = session_fabric()
    
    try:
        yield session
    finally:
        await session.close()
