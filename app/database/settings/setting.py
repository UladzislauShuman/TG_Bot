from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_
from sqlalchemy import select, func, cast, Integer 

async def set_new_setting(tg_id, setting):
     async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.setting = setting
            await session.commit()
         
async def get_setting(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.setting 