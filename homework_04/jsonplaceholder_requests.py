"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""
import aiohttp

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: aiohttp.ClientSession, url: str) -> list:
    async with session.get(url) as response:
        data = await response.json()
        return data


async def fetch_users_data() -> list:
    async with aiohttp.ClientSession() as session:
        data = await fetch_json(session, USERS_DATA_URL)
        return data


async def fetch_posts_data() -> list:
    async with aiohttp.ClientSession() as session:
        data = await fetch_json(session, POSTS_DATA_URL)
        return data
