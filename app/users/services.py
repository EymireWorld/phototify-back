from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserModel
from app.schemas import UserSchema


async def get_users(
    session: AsyncSession,
    offset: int,
    limit: int
) -> list[UserSchema] | None:
    stmt = select(UserModel)

    result = await session.execute(stmt)

    if not (result := result.scalars()):
        return None
    return [row.to_schema() for row in result][offset:][:limit]


async def get_user(
    session: AsyncSession,
    user_id: int
) -> UserSchema | None:
    stmt = select(UserModel).where(UserModel.id == user_id)

    result = await session.execute(stmt)

    if not (result := result.scalar()):
        return None
    return result.to_schema()
