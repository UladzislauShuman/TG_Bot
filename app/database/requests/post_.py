from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_#, Category, Item
from sqlalchemy import select, func, cast, Integer

from app.database.make_database.make_xlsx import make_xlsx
from app.database.make_database.convert_xlsx_to_sqlite import convert_xlsx_to_sqlite

# думаю названия функций говорят сами за себя
# может только разве уж что разные подробности реализации вас волнуют
# хотя, много важных начальных штук есть в main.py, да и 
# в принципе некоторые вещи делались буквально по аналогиичны друг другу

async def set_Post():
    async with async_session() as session:
        # await make_xlsx()
        # await convert_xslx_to_sqlite()
        return await session.scalars(select(Post_))
    

#слишком затратно
async def get_last_post():
    async with async_session() as session:
        query = select(Post_).order_by(Post_.id.desc()).limit(1)
        result = await session.scalar(query)
        return result


from aiogram.types import Message
from telethon import TelegramClient, events
import re
from app.database.models import Post_
from data import API_HASH, API_ID, input_channel
api_id = API_ID
api_hash = API_HASH
channels = [input_channel]

async def set_last_post(message: Message):
    # здесь должна быть функция make_post_from_message
    print(f"message: {message}")
    if isinstance(message.text, str): 
        print("isinstance(message.text, str) == true")
        # Извлечение хештегов из текста поста
        hashtags = re.findall(r"#(\w+)", message.text)  
        admin_hashtags = [hashtag for hashtag in hashtags if hashtag.startswith("admin_")]
        theme_hashtags = [theme for theme in hashtags if not theme.startswith("admin_")]
                    
        author = ""
        themes = ""
                    
        if len(admin_hashtags) >= 1:
            author = ", ".join(admin_hashtags) if admin_hashtags else ""
        else:
            author = "No author"

        if len(theme_hashtags) >= 1:
            themes = ", ".join(theme_hashtags) if theme_hashtags else ""
        else:
            themes = "No themes"
            
        async with async_session() as session:
            print("add new post")
            session.add(Post_(channel="wouwouwou345", 
                              id=message.id, 
                              post_link=f"https://t.me/wouwouwou345/{message.id}", 
                              themes=themes,
                              author=author))        
            await session.commit()


async def get_posts_themes(tg_id, theme_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        query = select(Post_).where(
            Post_.themes.like(f'%{theme_id}%')
        ).order_by(Post_.id.desc()).limit(cast(user.amount, Integer))
        result = await session.scalars(query)
        return result.all()
    
async def get_posts_themes_(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        query = select(Post_).where(Post_.themes.like(f'%{user.current_theme}%')).order_by(Post_.id.desc())
        result = await session.scalars(query)
        list_of_posts = result.all()
        user_amount = int(user.amount)
        page_of_posts = [list_of_posts[i:i+user_amount] for i in range(0, len(list_of_posts), user_amount)]
        return page_of_posts[user.current_page - 1]
        
