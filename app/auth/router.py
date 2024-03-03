from fastapi import APIRouter, Form
from pydantic import EmailStr

from app.auth import services
from app.dependencies import CurrentUser, Session
from app.schemas import TokenSchema, UserProfileSchema, UserShowSchema


router = APIRouter(
    prefix= '/auth',
    tags= ['Auth']
)


@router.post('/sign_up')
async def sing_up(
    session: Session,
    username: str = Form(),
    first_name: str = Form(),
    last_name: str = Form(),
    email: EmailStr = Form(),
    password: str = Form()
) -> UserShowSchema:
    return await services.sing_up_user(session, username, first_name, last_name, email, password)


@router.post('/sign_in')
async def sing_in(
    session: Session,
    email_or_username: str = Form(),
    password: str = Form()
) -> TokenSchema:
    return await services.sing_in_user(session, email_or_username, password)


@router.get('/me')
async def profile(current_user: CurrentUser) -> UserProfileSchema:
    return current_user
