from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_
from sqlalchemy import select, func, cast, Integer      
        
async def set_new_themes(tg_id, theme):
     async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.theme = theme
            await session.commit()
         
async def get_themes_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.theme.split(", ") 
async def get_themes_post(post_:Post_):
    async with async_session() as session:
        return post_.themes.split(", ")    
         
async def get_themes_str(tg_id):
    async with async_session() as session:
        user = await session. scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.theme
        
async def get_all_themes():
    async with async_session() as session:
        return await session.scalars(select(Theme)) 