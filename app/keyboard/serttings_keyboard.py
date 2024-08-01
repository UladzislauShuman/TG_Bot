from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.settings.settings import settings_

async def settings():
    all_settings = list(settings_.keys())
    keyboard = InlineKeyboardBuilder()
    for setting in all_settings:
        keyboard.add(InlineKeyboardButton(text=setting, callback_data=f"{settings_[setting]}"))
        print(f"{settings_[setting]}")
    return keyboard.adjust(2).as_markup()

from app.database.settings.author import get_all_authors

async def authors_list():
    all_authors = await get_all_authors()
    keyboard = InlineKeyboardBuilder()
    for author in all_authors:
        keyboard.add(InlineKeyboardButton(text=author.name, callback_data=f"author_{author.name}"))
        print(f"author_{author.name}")
    keyboard.add(InlineKeyboardButton(text='Вернуться к настройкам', callback_data='to_settings'))
    return keyboard.adjust(2).as_markup()

from app.database.requests.theme import get_themes

async def themes_list():
    all_themes = await get_themes()
    keyboard = InlineKeyboardBuilder()
    for theme in all_themes:
        keyboard.add(InlineKeyboardButton(text=theme.name, callback_data=f"theme-{theme.name}"))
        print(f"theme-{theme.name}")
    keyboard.add(InlineKeyboardButton(text='Вернуться к настройкам', callback_data='to_settings'))
    return keyboard.adjust(2).as_markup()


