from datetime import datetime

from sqlalchemy import ARRAY as Array
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column
)

from app.schemas import CommentSchema, PostSchema, UserSchema


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr 
    def __tablename__(cls):
        return f'{cls.__name__.lower()[:-5]}s'
    
    id: Mapped[int] = mapped_column(primary_key= True, index= True)


class UserModel(Base):
    username: Mapped[str] = mapped_column(unique= True, index= True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique= True)
    hashed_password: Mapped[bytes]
    created_at: Mapped[datetime]


    def to_schema(self) -> UserSchema:
        return UserSchema(
            id= self.id,
            username= self.username,
            first_name= self.first_name,
            last_name= self.last_name,
            email= self.email,
            hashed_password= self.hashed_password,
            created_at= self.created_at
        )


class PostModel(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    description: Mapped[str | None]
    filename: Mapped[str]
    likes: Mapped[list[int]] = mapped_column(Array(Integer))
    created_at: Mapped[datetime]


    def to_schema(self) -> PostSchema:
        return PostSchema(
            id= self.id,
            user_id= self.user_id,
            created_at= self.created_at,
            description= self.description,
            likes= self.likes,
            filename= self.filename
        )


class CommentModel(Base):
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), index= True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index= True)
    text: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime]
    edited_at: Mapped[datetime | None]


    def to_schema(self) -> CommentSchema:
        return CommentSchema(
            id= self.id,
            post_id= self.post_id,
            user_id= self.user_id,
            text= self.text,
            created_at= self.created_at
        )
