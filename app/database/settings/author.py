from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_
from sqlalchemy import select, func, cast, Integer 

from app.database.models import Author      
        
async def set_new_authors(tg_id, author):
     async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.author = author
            await session.commit()
         
async def get_authors_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.author.split(", ") 
async def get_authors_post(post_:Post_):
    async with async_session() as session:
        return post_.author.split(", ")    
         
async def get_authors_str(tg_id):
    async with async_session() as session:
        user = await session. scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.author
        
async def get_all_authors():
    async with async_session() as session:
        return await session.scalars(select(Author)) 