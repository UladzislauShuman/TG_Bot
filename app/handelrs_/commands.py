# отдельно обрабатываю команды

from data import bot_token

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.keyboard.main_kb import main_kb

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router_commands = Router()

from app.database.requests.user import set_user

@router_commands.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Lol', reply_markup=await main_kb(message.from_user.id))
    
@router_commands.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('push on help')
