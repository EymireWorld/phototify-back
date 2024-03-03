from fastapi import APIRouter

from app.dependencies import Session, CurrentUser
from app.posts import services
from app.schemas import PostAddSchema as PostAdd
from app.schemas import PostShowSchema as Post
from app.schemas import PostUpdateSchema as PostUpdate


router = APIRouter(
    prefix= '/posts',
    tags= ['Posts']
)


@router.get('')
async def get_posts(
    session: Session,
    offset: int = 0,
    limit: int = 10
) -> list[Post] | None:
    return await services.get_posts(session, offset, limit)


@router.get('/{post_id}')
async def get_post(
    session: Session,
    post_id: int
) -> Post | None:
    return await services.get_post(session, post_id)


@router.post('')
async def add_post(
    session: Session,
    data: PostAdd
) -> Post | None:
    return await services.add_post(session, data)


@router.put('/{post_id}')
async def update_post(
    session: Session,
    post_id: int,
    data: PostUpdate
) -> Post | None:
    return await services.update_post(session, post_id, data)


@router.delete('/{post_id}')
async def remove_post(session: Session, post_id: int):
    return await services.remove_post(session, post_id)


@router.get('/{post_id}/likes')
async def get_post_likes(session: Session, post_id: int):
    return await services.get_post_likes(session, post_id)


@router.post('/{post_id}/like')
async def add_post_like(current_user: CurrentUser, session: Session, post_id: int):
    return await services.add_post_like(session, post_id, current_user.id)


@router.delete('/{post_id}/like')
async def add_post_like(current_user: CurrentUser, session: Session, post_id: int):
    return await services.remove_post_like(session, post_id, current_user.id)
