from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes= True)


class UserSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: bytes
    created_at: datetime


class UserAddSchema(Schema):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdateSchema(Schema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserShowSchema(Schema):
    id: int
    username: str
    created_at: datetime


class UserProfileSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

# ====================

class PostSchema(Schema):
    id: int
    author_id: int
    created_at: datetime
    description: str | None = None
    filename: str


class PostAddSchema(Schema):
    author_id: int
    description: str | None
    filename: str


class PostUpdateSchema(Schema):
    description: str | None = None


class PostShowSchema(Schema):
    id: int
    author_id: int
    created_at: datetime
    description: str | None
    filename: str

# ====================

class TokenSchema(Schema):
    access_token: str
    token_type: str

# ====================

class LikeSchema(Schema):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

# ====================

class CommentSchema(Schema):
    id: int
    post_id: int
    user_id: int
    text: str
    created_at: datetime
