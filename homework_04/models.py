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
from sqlalchemy.orm import sessionmaker, declared_attr, \
    declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy import Column, String, Integer, ForeignKey

PG_CONN_URI = os.environ.get(
    "SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"
async_engine: AsyncEngine = create_async_engine(PG_CONN_URI, echo=True)
Session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


class Base:
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)


Base = declarative_base(cls=Base)


class User(Base):
    name = Column(String(50), unique=False)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)

    posts = relationship("Post", back_populates="user")


class Post(Base):
    user_id = Column(Integer, ForeignKey("users.id"), unique=False)
    title = Column(String(100), unique=False)
    body = Column(String(500), unique=False)

    user = relationship("User", back_populates="posts")
