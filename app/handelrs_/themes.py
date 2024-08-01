from data import bot_token

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.keyboard.left_right import left_right
from app.keyboard.themes import themes

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router_themes = Router()

# хотелось, чтобы не было огромного количества сообщений
# а для этого, при отправлении нового, нужно удалить старое
async def delete_message(chat_id, message_id):
    bot = Bot(token=bot_token)
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    
from app.database.requests.post_ import set_Post

@router_themes.message(F.text == 'Темы')
async def theme_chose(message: Message):
    set_Post()
    await message.answer('Выбери тему', reply_markup=await themes())

@router_themes.callback_query(F.data == "to_themes")
async def theme(callback: CallbackQuery):
    
    await delete_message(callback.message.chat.id, callback.message.message_id)
    
    set_Post()
    await callback.message.answer('Выбери тему', reply_markup=await themes())

from app.database.requests.post_ import get_posts_themes, get_posts_themes_
from app.database.requests.user import set_user_page_theme, get_user_page

@router_themes.callback_query(F.data.startswith('theme_'))
async def theme(callback: CallbackQuery):
    await callback.answer("Хороший выбор")
    theme_id = callback.data.replace('theme_', '') 
    await set_user_page_theme(callback.from_user.id, theme_id)
    
    answer = "Посты по теме\n"
    all_posts = await get_posts_themes_(callback.from_user.id) 
    
    if not all_posts:
        print("Ничего не видно")
    else:    
        for post in all_posts:
            answer = answer + f"id: {post.id}, link: {post.post_link}, themes: {post.themes}, author: {post.author}\n" 
        answer = answer + f"страница: {await get_user_page(callback.from_user.id)}"  
        
        await delete_message(callback.message.chat.id, callback.message.message_id)
          
        await callback.message.answer(answer, reply_markup=left_right)

from app.database.requests.user import set_user_page, get_user_max_page
from aiogram import Bot
import asyncio

# вот тут уже работаем с листанием страниц

@router_themes.callback_query(F.data == "left")
async def left(callback: CallbackQuery):
    user_page = await get_user_page(callback.from_user.id)
    if user_page == 1:
        await set_user_page(callback.from_user.id, await get_user_max_page(callback.from_user.id))
    else:
        await set_user_page(callback.from_user.id, user_page - 1)
    
    answer = "Посты по теме\n" 
    all_posts = await get_posts_themes_(callback.from_user.id) 
    
    if not all_posts:
        print("Ничего не видно")
    else:    
        
        await delete_message(callback.message.chat.id, callback.message.message_id)
        
        for post in all_posts:
            answer = answer + f"id: {post.id}, link: {post.post_link}, themes: {post.themes}, author: {post.author}\n" 
        answer = answer + f"страница: {await get_user_page(callback.from_user.id)}"    
        await callback.message.answer(answer, reply_markup=left_right)
 
@router_themes.callback_query(F.data == "right")
async def left(callback: CallbackQuery):
    user_page = await get_user_page(callback.from_user.id)
    if user_page == await get_user_max_page(callback.from_user.id):
        await set_user_page(callback.from_user.id, 1)
    else:
        await set_user_page(callback.from_user.id, user_page + 1)
    
    answer = "Посты по теме\n"    
    all_posts = await get_posts_themes_(callback.from_user.id) 
    
    if not all_posts:
        print("Ничего не видно")
    else:  
        
        await delete_message(callback.message.chat.id, callback.message.message_id)
          
        for post in all_posts:
            answer = answer + f"id: {post.id}, link: {post.post_link}, themes: {post.themes}, author: {post.author}\n" 
        answer = answer + f"страница: {await get_user_page(callback.from_user.id)}"    
        await callback.message.answer(answer, reply_markup=left_right)
 
from app.keyboard.main_kb import main_kb 
 
@router_themes.callback_query(F.data.startswith('to_main'))
async def theme(callback: CallbackQuery):
    await delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.answer("Просто")
    await callback.message.answer("Ты опять на главной", reply_markup=await main_kb(callback.from_user.id))
