import os
from datetime import datetime
from hashlib import sha256

import aiofiles
from fastapi import UploadFile
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommentModel, PostModel
from app.schemas import CommentSchema, PostSchema
from app.files.services import add_file


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


async def add_post(
    session: AsyncSession,
    user_id: int,
    file: UploadFile,
    description: str | None
):
    values = {
        'user_id': user_id,
        'created_at': datetime.utcnow(),
        'description': description,
        'likes': [],
        'filename': await add_file(file)
    }
    stmt = insert(PostModel).values(**values).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit()

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def update_post(
    session: AsyncSession,
    user_id: int,
    post_id: int,
    description: str
):
    stmt = update(PostModel).where(PostModel.id == post_id, PostModel.user_id == user_id).values(description= description).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def remove_post(
    session: AsyncSession,
    user_id: int,
    post_id: int
):
    stmt = delete(PostModel).where(PostModel.id == post_id, PostModel.user_id == user_id).returning(PostModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def add_post_like(
    session: AsyncSession,
    post_id: int,
    user_id: int
) -> bool:
    if not (post := await get_post(session, post_id)):
        return False
    if user_id in post.likes:
        return False
    
    post.likes.append(user_id)
    
    stmt = update(PostModel).where(PostModel.id == post_id).values(likes= post.likes)
    
    await session.execute(stmt)
    await session.commit()
    
    return True


async def remove_post_like(
    session: AsyncSession,
    post_id: int,
    user_id: int
) -> bool:
    if not (post := await get_post(session, post_id)):
        return False
    if user_id not in post.likes:
        return False
    
    post.likes.remove(user_id)
    
    stmt = update(PostModel).where(PostModel.id == post_id).values(likes= post.likes)
    
    await session.execute(stmt)
    await session.commit()
    
    return True


async def get_post_comments(
    session: AsyncSession,
    post_id: int,
    offset: int,
    limit: int
) -> list[CommentSchema] | None:
    stmt = select(CommentModel).where(CommentModel.post_id == post_id)

    result = await session.execute(stmt)

    if not (result := result.scalars()):
        return None
    return [row.to_schema() for row in result][offset:][:limit]


async def get_post_comment(
    session: AsyncSession,
    post_id: int,
    comment_id: int
) -> CommentSchema | None:
    stmt = select(CommentModel).where(CommentModel.post_id == post_id, CommentModel.id == comment_id)

    result = await session.execute(stmt)

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def add_post_comment(
    session: AsyncSession,
    post_id: int,
    user_id: int,
    text: str
) -> CommentSchema:
    values = {
        'post_id': post_id,
        'user_id': user_id,
        'text': text,
        'created_at': datetime.utcnow()
    }
    stmt = insert(CommentModel).values(**values).returning(CommentModel)

    result = await session.execute(stmt)
    await session.commit()

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def update_post_comment(
    session: AsyncSession,
    post_id: int,
    comment_id: int,
    user_id: int,
    text: str
) -> CommentSchema | None:
    stmt = update(CommentModel).where(CommentModel.post_id == post_id, CommentModel.id == comment_id, CommentModel.user_id == user_id).values(text= text).returning(CommentModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def remove_post_comment(
    session: AsyncSession,
    post_id: int,
    comment_id: int,
    user_id: int
) -> CommentSchema | None:
    stmt = delete(CommentModel).where(CommentModel.post_id == post_id, CommentModel.id == comment_id, CommentModel.user_id == user_id).returning(CommentModel)

    result = await session.execute(stmt)
    await session.commit() 

    if not (result := result.scalar()):
        return None
    return result.to_schema()
