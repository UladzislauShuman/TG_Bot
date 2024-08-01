from data import bot_token

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


router_last_post = Router()

from app.database.requests.post_ import get_last_post

@router_last_post.message(F.text == 'Последний пост')
async def post(message: Message):
    post_item = await get_last_post()
    await message.answer(f"ссылка: {post_item.post_link}")