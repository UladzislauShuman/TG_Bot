from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.models import async_session
from sqlalchemy import select
from app.database.models import User

async def main_kb(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='Последний пост')],
                                     [KeyboardButton(text='Темы')],
                                     [KeyboardButton(text='/start'), KeyboardButton(text='/help'), KeyboardButton(text='/settings')],
                                     [KeyboardButton(text='/settings1')]],
                           resize_keyboard=True,
                           input_field_placeholder='Что ты выберешь?')
        
        if user.rights == "admin":
            keyboard.keyboard.append([KeyboardButton(text='Для админов', callback_data='admin')])
        return keyboard
