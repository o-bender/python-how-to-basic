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
from models import create_tables, Session, User, Post
from jsonplaceholder_requests import fetch_posts_data, fetch_users_data


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

    return user


async def create_post(session, user_id: int, title: str, body: str) -> Post:
    post = Post(user_id=user_id, title=title, body=body)
    session.add(post)

    return post


async def async_main():
    pass


async def main():
    await create_tables()
    users_data, posts_data = await fetch_users_posts_from_api()
    async with Session() as session:
        async with session.begin():
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


if __name__ == "__main__":
    asyncio.run(main())
