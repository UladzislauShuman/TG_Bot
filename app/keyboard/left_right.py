from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

left_right = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='<=', callback_data='left'),
                                                    InlineKeyboardButton(text='к темам', callback_data='to_themes'),
                                                    InlineKeyboardButton(text='=>', callback_data='right')]])