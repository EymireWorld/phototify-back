from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import decode_jwt
from app.database import get_session
from app.models import UserSchema
from app.users.services import get_user


Session = Annotated[AsyncSession, Depends(get_session)]
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session
) -> UserSchema:
    if credentials.scheme != 'Bearer':
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= 'Invalid authentication scheme.'
        )
    if not (data := decode_jwt(credentials.credentials)):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= 'Invalid token.'
        )
    if data['end_at'] < int(datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= 'Expired token.'
        )
    
    return await get_user(session, data['user_id'])


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
