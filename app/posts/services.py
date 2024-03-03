from datetime import datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PostModel
from app.schemas import PostAddSchema, PostSchema, PostUpdateSchema


async def get_posts(
    session: AsyncSession,
    offset: int,
    limit: int
) -> list[PostSchema] | None:
    stmt = select(PostModel)

    result = await session.execute(stmt)

    if not (result := result.scalars()):
        return None
    return [row.to_schema() for row in result][offset:][:limit]


async def get_post(
    session: AsyncSession,
    post_id: int
) -> PostSchema | None:
    stmt = select(PostModel).where(PostModel.id == post_id)

    result = await session.execute(stmt)

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def add_post(session: AsyncSession, data: PostAddSchema):
    values = {
        'author_id': data.author_id,
        'created_at': datetime.utcnow(),
        'description': data.description,
        'filename': data.filename
    }
    stmt = insert(PostModel).values(**values).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit()

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def update_post(session: AsyncSession, post_id: int, data: PostUpdateSchema):
    values = data.model_dump(exclude_unset= True)
    
    if not values:
        return None
    
    stmt = update(PostModel).where(PostModel.id == post_id).values(**data.model_dump(exclude_unset= True)).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def remove_post(session: AsyncSession, post_id: int):
    stmt = delete(PostModel).where(PostModel.id == post_id).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def get_post_likes(session: AsyncSession, post_id: int):
    pass


async def add_post_like(session: AsyncSession, post_id: int, user_id: int):
    pass


async def remove_post_like(session: AsyncSession, post_id: int, user_id: int):
    pass
