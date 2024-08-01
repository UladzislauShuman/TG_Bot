from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.models import async_session
from sqlalchemy import select
from app.database.models import User

from app.database.requests.theme import get_themes
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def themes():
    all_themes = await get_themes()
    keyboard = InlineKeyboardBuilder()
    for theme in all_themes:
        keyboard.add(InlineKeyboardButton(text=theme.name, callback_data=f"theme_{theme.name}"))
        print(f"theme_{theme.name}")
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
