from fastapi import APIRouter, Form, UploadFile, HTTPException, status

from app.dependencies import CurrentUser, Session
from app.posts import services
from app.schemas import CommentSchema as Comment
from app.schemas import PostShowSchema as Post


router = APIRouter(
    prefix= '/posts'
)


@router.get('', tags= ['Posts'])
async def get_posts(
    session: Session,
    offset: int = 0,
    limit: int = 10
) -> list[Post]:
    return await services.get_posts(session, offset, limit)


@router.get('/{post_id}', tags= ['Posts'])
async def get_post(
    session: Session,
    post_id: int
) -> Post:
    return await services.get_post(session, post_id)


@router.post('', tags= ['Posts'])
async def add_post(
    current_user: CurrentUser,
    session: Session,
    file: UploadFile,
    description: str | None = Form(None)
) -> Post:
    return await services.add_post(session, current_user.id, file, description)


@router.put('/{post_id}', tags= ['Posts'])
async def update_post(
    current_user: CurrentUser,
    session: Session,
    post_id: int,
    description: str = Form()
) -> Post:
    return await services.update_post(session, post_id, current_user.id, description)


@router.delete('/{post_id}', tags= ['Posts'])
async def remove_post(
    current_user: CurrentUser,
    session: Session,
    post_id: int
) -> Post:
    return await services.remove_post(session, current_user.id, post_id)


@router.post('/{post_id}/likes', tags= ['Likes'])
async def add_post_like(
    current_user: CurrentUser,
    session: Session,
    post_id: int
):
    return {
        'liked': await services.add_post_like(session, post_id, current_user.id)
    }


@router.delete('/{post_id}/likes', tags= ['Likes'])
async def add_post_like(
    current_user: CurrentUser,
    session: Session,
    post_id: int
):
    return {
        'disliked': await services.remove_post_like(session, post_id, current_user.id)
    }


@router.get('/{post_id}/comments', tags= ['Comments'])
async def get_post_comments(
    session: Session,
    post_id: int,
    offset: int = 0,
    limit: int = 10
) -> list[Comment]:
    return await services.get_post_comments(session, post_id, offset, limit)


@router.get('/{post_id}/comments/{comment_id}', tags= ['Comments'])
async def get_post_comment(
    session: Session,
    post_id: int,
    comment_id: int
) -> Comment:
    return await services.get_post_comments(session, post_id, comment_id)


@router.post('/{post_id}/comments', tags= ['Comments'])
async def add_post_comment(
    current_user: CurrentUser,
    session: Session,
    post_id: int,
    text: str = Form()
) -> Comment:
    return await services.add_post_comment(session, post_id, current_user.id, text)


@router.put('/{post_id}/comments/{comment_id}', tags= ['Comments'])
async def update_post_comment(
    current_user: CurrentUser,
    session: Session,
    post_id: int,
    comment_id: int,
    text: str = Form()
) -> Comment:
    return await services.update_post_comment(session, post_id, comment_id, current_user.id, text)


@router.delete('/{post_id}/comments/{comment_id}', tags= ['Comments'])
async def remove_post_comment(
    current_user: CurrentUser,
    session: Session,
    post_id: int,
    comment_id: int
) -> Comment:
    return await services.remove_post_comment(session, post_id, comment_id, current_user.id)
