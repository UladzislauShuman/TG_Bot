from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_#, Category, Item
from sqlalchemy import select, func, cast, Integer


async def get_themes():
    async with async_session() as session:
        return await session.scalars(select(Theme))