from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_#, Category, Item
from sqlalchemy import select, func, cast, Integer

async def get_post(post_id):
    async with async_session() as session:
        return await session.scalar(select(Post).where(Post.id == post_id))
