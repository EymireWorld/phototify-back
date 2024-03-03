from datetime import datetime, timedelta

import bcrypt
import jwt

from app.settings import JWT_TOKEN_LIFETIME_IN_MINUTES


def encode_jwt(user_id: int) -> str:
    data = {
        'user_id': user_id,
        'end_at': int((datetime.utcnow() + timedelta(minutes= JWT_TOKEN_LIFETIME_IN_MINUTES)).timestamp())
    }
    
    with open('certificates\jwt-private.pem', 'r', encoding= 'utf-8') as key_file:
        private_key = key_file.read()
        
    return jwt.encode(
        data,
        private_key,
        algorithm= 'RS256',
    )


def decode_jwt(token: str | bytes) -> dict:
    with open('certificates\jwt-public.pem', 'r', encoding= 'utf-8') as key_file:
        public_key = key_file.read()
    
    return jwt.decode(
        token,
        public_key,
        algorithms= ['RS256'],
    )


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password,
    )