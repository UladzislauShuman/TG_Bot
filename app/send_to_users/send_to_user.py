from data import bot_token

from app.database.requests.user import get_users
from aiogram import Bot
from aiogram.types import Message

from app.database.models import Post_
from app.database.make_database.make_post_from_message import make_post_from_message

from app.database.settings.author import get_authors_post, get_authors_user
from app.database.settings.themes import get_themes_post, get_themes_user

async def send_to_user(message: Message):
    post_ = await make_post_from_message(message=message)
    bot = Bot(token=bot_token)
    all_users = await get_users()
    for user in all_users:
        user_authors = await get_authors_user(user.tg_id)
        post_authors = await get_authors_post(post_)
        
        user_themes = await get_themes_user(user.tg_id)
        post_themes = await get_themes_post(post_)
        
        all_user_tags = user_themes + user_authors
        all_post_tags = post_themes + post_authors
        
        if any(item in all_post_tags for item in all_user_tags):
            await bot.send_message(user.tg_id, f"Новый пост от {post_.author}\nПо теме(ам) {post_.themes}")        