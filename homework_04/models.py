"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os
import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, noload, declared_attr, declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey


class Base:
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)


Base = declarative_base(cls=Base)

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://username:passwd!@localhost/postgres"
async_engine: AsyncEngine = create_async_engine(PG_CONN_URI, echo=True)
Session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    # __tablename__ = 'users_list'

    name = Column(String(50), unique=False)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)

    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"username={self.username}, "
            f"email={self.email})"
        )


class Post(Base):
    # __tablename__ = 'posts_list'

    user_id = Column(Integer, ForeignKey("users.id"), unique=False)
    title = Column(String(100), unique=False)
    body = Column(String(500), unique=False)

    user = relationship("User", back_populates="posts")

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"user_id={self.user_id}, "
            f"title={self.title}, "
            f"body={self.body})"
        )
