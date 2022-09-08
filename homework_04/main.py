"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio
from loguru import logger
from models import async_engine, Base, Session, User, Post
from jsonplaceholder_requests import fetch_posts_data, fetch_users_data


async def create_tables():
    async with async_engine.begin() as conn:
        logger.info("todo: drop all")
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("todo: create all")
        await conn.run_sync(Base.metadata.create_all)


async def fetch_users_posts_from_api():
    # users_data: List[dict]
    # posts_data: List[dict]
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )
    return users_data, posts_data


async def create_user(session, iduser: int, name: str, username: str, email: str) -> User:
    user = User(id=iduser, name=name, username=username, email=email)
    session.add(user)
    logger.info("user create", user)

    # await session.commit()
    # logger.info("user saved", user)

    # not necessary!! if expire_on_commit=False
    # await session.refresh(user)
    # logger.info("user refreshed", user)

    return user


async def create_post(session, user_id: int, title: str, body: str) -> User:
    post = Post(user_id=user_id, title=title, body=body)
    session.add(post)
    logger.info("post create", post)

    # await session.commit()
    # logger.info("post saved", post)

    # not necessary!! if expire_on_commit=False
    # await session.refresh(post)
    # logger.info("user refreshed", post)

    return post


async def async_main():
    pass


async def main():
    await create_tables()
    users_data, posts_data = await fetch_users_posts_from_api()
    # logger.info(type(users_data))
    # logger.info(posts_data)
    async with Session() as session:
        for user_profile in users_data:
            await create_user(
                session,
                user_profile.get("id"),
                user_profile.get("name"),
                user_profile.get("username"),
                user_profile.get("email")
            )
        for post_profile in posts_data:
            await create_post(
                session,
                post_profile.get("userId"),
                post_profile.get("title"),
                post_profile.get("body")
            )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
