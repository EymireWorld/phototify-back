from fastapi import APIRouter

from app.dependencies import Session
from app.schemas import UserShowSchema as User
from app.users import services


router = APIRouter(
    prefix= '/users',
    tags= ['Users']
)


@router.get('')
async def get_users(
    session: Session,
    offset: int = 0,
    limit: int = 10
) -> list[User] | None:
    return await services.get_users(session, offset, limit)


@router.get('/{user_id}')
async def get_user(
    session: Session,
    user_id: int
) -> User | None:
    return await services.get_user(session, user_id)
