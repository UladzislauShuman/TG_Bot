#from app.handelrs import router

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
#import app.database.requests as rq

router_settings = Router()

class States(StatesGroup):
    setting = State()
    amount = State()
    com_settings = State()
    authors = State()
    themes = State()
    
    
from app.database.models import async_session
from app.database.models import User


from app.database.settings.setting import get_setting, set_new_setting

@router_settings.message(Command('settings'))
async def cmd_setting(message: Message, state: FSMContext):
    await message.answer(f'ваша настройка: {await get_setting(message.from_user.id)}')
    await message.answer('напиши новую настройку')
    await state.set_state(States.com_settings)
@router_settings.message(States.com_settings)
async def new_setting(message: Message, state: FSMContext):
    await set_new_setting(message.from_user.id, message.text)
    await message.answer(f'ваша новая настройка!!!: {await get_setting(message.from_user.id)}')
    await state.clear()
  
from app.keyboard.serttings_keyboard import settings  
        
@router_settings.message(Command('settings1'))
async def cmd_setting(message: Message):
    await message.answer(f'Выбери параметр, который будем менять', reply_markup=await settings())

from app.database.settings.setting import get_setting, set_new_setting

@router_settings.callback_query(F.data == "setting")
async def setting(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f"Вы выбрали Настройка")
    await callback.message.answer(f'ваша Настройка: {await get_setting(callback.from_user.id)}')
    await callback.message.answer('напиши новую Настройку')  
    await state.set_state(States.setting)
    await callback.answer(f'Вы написали Настройку')
@router_settings.message(States.setting)
async def new_setting(message: Message, state: FSMContext):
    await set_new_setting(message.from_user.id, message.text)
    await message.answer(f'ваша новая Настройка: {await get_setting(message.from_user.id)}')
    await state.clear()

from app.database.settings.amount import get_amount, set_new_amount

@router_settings.callback_query(F.data == "amount")
async def amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f"Вы выбрали Количество")
    await callback.message.answer(f'ваше Количество: {await get_amount(callback.from_user.id)}')
    await callback.message.answer('напиши новое Количество')
    await state.set_state(States.amount)
    await callback.answer(f"Вы написали Количество")
@router_settings.message(States.amount)
async def new_amount(message: Message, state: FSMContext):        
    await set_new_amount(message.from_user.id, message.text)
    await message.answer(f'ваше новое Количество: {await get_amount(message.from_user.id)}')
    await state.clear()
    

from app.database.settings.author import get_all_authors, get_authors_post, get_authors_str, get_authors_user
from app.database.settings.author import set_new_authors
from app.keyboard.serttings_keyboard import authors_list

@router_settings.callback_query(F.data == "authors")
async def authors(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f"Вы выбрали Авторы")
    await callback.message.answer(f'ваши Авторы: {await get_authors_str(callback.from_user.id)}')
    await callback.message.answer('напиши новых Авторов', reply_markup=await authors_list())  
    await state.set_state(States.authors)
    await callback.answer(f'Вы написали Авторов')

@router_settings.callback_query(F.data.startswith('author_'))
async def author(callback: CallbackQuery):
    user_authors = await get_authors_user(callback.from_user.id)
    author_id = callback.data.replace('author_','')
    if author_id in user_authors:
        user_authors.remove(author_id)
        await callback.answer(f"Вы отписались от {author_id}")
    else:
        user_authors.append(author_id)
        await callback.answer(f"Вы подписались на {author_id}")
    await set_new_authors(callback.from_user.id, ", ".join(user_authors))   
    await callback.message.answer(f'ваши новые Авторы: {await get_authors_str(callback.from_user.id)}')

from app.database.settings.themes import get_all_themes, get_themes_post, get_themes_str, get_themes_user
from app.database.settings.themes import set_new_themes
from app.keyboard.serttings_keyboard import themes_list

@router_settings.callback_query(F.data == "themes")
async def themes(callback: CallbackQuery, state: FSMContext):
    await callback.answer(f"Вы выбрали Темы")
    await callback.message.answer(f'ваши Темы: {await get_themes_str(callback.from_user.id)}')
    await callback.message.answer('напиши новые Темы', reply_markup=await themes_list())  
    await state.set_state(States.themes)
    await callback.answer(f'Вы написали Темы')
 
@router_settings.callback_query(F.data.startswith('theme-'))
async def author(callback: CallbackQuery):
    user_themes = await get_themes_user(callback.from_user.id)
    theme_id = callback.data.replace('theme-','')
    if theme_id in user_themes:
        user_themes.remove(theme_id)
        await callback.answer(f"Вы отписались от {theme_id}")
    else:
        user_themes.append(theme_id)
        await callback.answer(f"Вы подписались на {theme_id}")
    await set_new_themes(callback.from_user.id, ", ".join(user_themes))   
    await callback.message.answer(f'ваши новые Темы: {await get_themes_str(callback.from_user.id)}') 
 
from app.keyboard.serttings_keyboard import settings

@router_settings.callback_query(F.data.startswith('to_settings'))
async def to_settings(callback: CallbackQuery):
    await callback.answer("Просто")
    await callback.message.answer("Ты опять выбираешь настройки", reply_markup=await settings())