from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column
)

from app.schemas import PostSchema, UserSchema


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr 
    def __tablename__(cls):
        return f'{cls.__name__.lower()[:-5]}s'
    
    id: Mapped[int] = mapped_column(primary_key= True, index= True)


class UserModel(Base):
    username: Mapped[str] = mapped_column(unique= True)
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
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime]
    description: Mapped[str | None]
    filename: Mapped[str]


    def to_schema(self) -> PostSchema:
        return PostSchema(
            id= self.id,
            author_id= self.author_id,
            created_at= self.created_at,
            description= self.description,
            filename= self.filename
        )
