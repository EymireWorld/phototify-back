from datetime import datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PostModel
from app.schemas import PostAddSchema, PostSchema


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


async def add_post(session: AsyncSession, data: PostAddSchema, user_id: int):
    values = {
        'user_id': user_id,
        'created_at': datetime.utcnow(),
        'description': data.description,
        'likes': [],
        'filename': data.filename
    }
    stmt = insert(PostModel).values(**values).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit()

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def update_post(session: AsyncSession, user_id: int, post_id: int, description: str):
    stmt = update(PostModel).where(PostModel.id == post_id, PostModel.user_id == user_id).values(description= description).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def remove_post(session: AsyncSession, user_id: int, post_id: int):
    stmt = delete(PostModel).where(PostModel.id == post_id, PostModel.user_id == user_id).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def add_post_like(session: AsyncSession, post_id: int, user_id: int) -> bool:
    if not (post := await get_post(session, post_id)):
        return False
    if user_id in post.likes:
        return False
    
    post.likes.append(user_id)
    
    stmt = update(PostModel).where(PostModel.id == post_id).values(likes= post.likes)
    
    await session.execute(stmt)
    await session.commit()
    
    return True


async def remove_post_like(session: AsyncSession, post_id: int, user_id: int) -> bool:
    if not (post := await get_post(session, post_id)):
        return False
    if user_id not in post.likes:
        return False
    
    post.likes.remove(user_id)
    
    stmt = update(PostModel).where(PostModel.id == post_id).values(likes= post.likes)
    
    await session.execute(stmt)
    await session.commit()
    
    return True
