from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import insert, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import encode_jwt, hash_password, validate_password
from app.models import UserModel
from app.schemas import TokenSchema, UserSchema


async def sing_up_user(
    session: AsyncSession,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str
) -> UserSchema:
    values = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'hashed_password': hash_password(password),
        'created_at': datetime.utcnow()
    }
    stmt = insert(UserModel).values(**values).returning(UserModel)
    
    try:
        result = await session.execute(stmt)
    except IntegrityError:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= 'Username or email is already registered.'
        )
    else:
        await session.commit()

    if not (result := result.scalar()):
        return None
    return result.to_schema()


async def sing_in_user(
    session: AsyncSession,
    email_or_username: str,
    password: str
) -> TokenSchema:
    stmt = select(UserModel).where(or_(UserModel.email == email_or_username, UserModel.username == email_or_username))
        
    result = await session.execute(stmt)
    
    if not (result := result.scalar()):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'Invalid username or email.'
        )
    elif not validate_password(password, result.hashed_password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= 'Invalid password.'
        )
    
    return TokenSchema(
        access_token= encode_jwt(result.id),
        token_type= 'Bearer'
    )
