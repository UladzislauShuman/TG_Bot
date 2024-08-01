# для админов
from data import bot_token

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboard as kb

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
#import app.database.requests as rq

router_admin = Router()

@router_admin.message(F.text == 'Для админов')
async def theme_chose(message: Message):
    await message.answer('В разработке')