# прежде всего, спустите свои глаза на функцию main()

# requests - запросы к базе данных, причём для разных таблиц в разных файлах (для эстетики(?))
# requests.models - основные классы описаны там (Пост, Автор, Тема, Пользователь и тп)
# handlers_ - обрабатывают сообщения пользователя
# keyboard - клавиатуры под разные задачи
# setting-и различного сорта - просто отделил Настройки от всех остальных

# и надеюсь вы читаете в алфавитном порядке

# о некоторых модулях по подробнее 
import asyncio # нужно для работы с асинхронным программированием(?) 
               # (коротко -- можно делать несколько вещей одновременно)
from aiogram import Bot, Dispatcher

# об функциях, написанных мной (как эта, к примеру)
# будет +- подробно расписано там, где они реализованы
from app.database.models import  async_main

from telethon import TelegramClient, events

# тут я решил в отдельном файле сохранить необходимые данные, чтобы 
# спокойно залить на github
from data import API_ID, API_HASH, input_channel, bot_token
# в процессе просмотров гайдов вам расскажут об этом подробнее
# коротко - при работе с telegram api, чтобы это было безопастно
# ваше приложение индентифицируют и дают ему спец ключ
# по которому ваши данные шифруют
api_id = API_ID
api_hash = API_HASH 

# тут хранится название моего канала 
INPUT_CHANNEL = input_channel

from app.send_to_users.send_to_user import send_to_user
import aiohttp

# вот здесь мы создаём бота по его токену
# а токен мы получаем при создании через BotFuther 
# (бот в телеграм, который как раз и создаёт бота (пустую болванку))
bot = Bot(token=bot_token)

from app.database.make_database.make_xlsx import make_xlsx
from app.database.make_database.convert_xlsx_to_sqlite import convert_xlsx_to_sqlite

# создаём наш Клиент
# так сказать -- через него мы и подключаемся к TG_API
# ну и работаем с тем, что мы хотим 
client = TelegramClient('test', api_id, api_hash)

from app.database.make_database.make_database import make_xlsx_
from app.database.requests.post_ import set_last_post
from app.database.models import Post_
from app.database.models import async_session
from app.database.make_database.make_post_from_message import make_post_from_message

# эта библиотека и позволяет работать с базами данных (создавать таблицы, запрашивать и заносить данные и тп)
from sqlalchemy import select, update

async def run_telethon():
    # здесь Клиент фиксирует новое сообщение у конкретного чата
    # (если не указать этот параметр, то оно у меня фиксировало каждое новое сообщение на аккаунте)
    @client.on(events.NewMessage(chats=INPUT_CHANNEL))
    # по большому счёту - название никак не влияет
    async def handle_new_message(event):
        message = event.message
        # моя функция, что отправляет пользователям (по их параметрам)
        # информацию о новом посте в канале 
        await send_to_user(message=message)
        # тк пост новый, то теперь его нужно задать как последний
        await set_last_post(message=message)
    
    # фиксирует изменения в посте
    @client.on(events.MessageEdited(chats=INPUT_CHANNEL))
    async def handle_message_deleted(event):
         message = event.message
         # вот это моя функция. из Message в Post_
         post_ = await make_post_from_message(message=message)
         # для работы с базой данных, нам нужно работать в Сессии 
         # (объект, который и даёт возможность работать с базой данных)
         # он определён в models.py, если вы проглядели
         async with async_session() as session:
            # session -- это объект, что является результатом работы функции
            # что создаёт ассинхронную сессию
            
            # запрос на изменение базы данных с условиями выбора
            stmt = update(Post_).where(Post_.id == post_.id).values(
                channel=post_.channel,
                id=post_.id,
                post_link=post_.post_link,
                themes=post_.themes,
                author=post_.author
            )
            await session.execute(stmt)
            await session.commit()
            print(f"измененена в базе данных")
    
    # фиксирует удаление поста               
    @client.on(events.MessageDeleted(chats=INPUT_CHANNEL))
    async def handle_message_deleted(event):
        message_id = event.deleted_id
        print(f"в процессе удаления: {message_id}")
        
        async with async_session() as session:
            # вытягиев Один Post_ из базы данных по определённому условию
            # scalar(запрос)
            post_ = await session.scalar(select(Post_).where(Post_.id == message_id))
            if post_:
                print(f"it was deleted")
                await session.delete(post_)
                await session.commit()
                    
    
    async with client:
        await client.start()
        await client.run_until_disconnected()

from app.handelrs_.settings import router_settings
from app.handelrs_.themes import router_themes 
from app.handelrs_.commands import router_commands
from app.handelrs_.admin import router_admin
from app.handelrs_.last_post import router_last_post
async def run_aiogram():
    dp = Dispatcher() # обрабатывает сообщения, что приходят боту от пользователя 
    # но - диспетчер может иметь роутеры, которые сами занимаются этим
    # (помогли структурировать код)
    dp.include_router(router_settings)
    dp.include_router(router_themes)
    dp.include_router(router_commands)
    dp.include_router(router_admin)
    dp.include_router(router_last_post)
    async with bot:
        print("Aiogram bot started")
        await dp.start_polling(bot)

# а теперь по подробнее
async def main():
    # функция для создания таблиц в базе данных, реализация которой 
    # расположена в models.py
    await async_main()  
    
    
    await asyncio.gather( # позволяет запустить несколько независимых задач параллельно
                          # тем самым задача не ждёт завершения другой задачи
        # для работы с телеграм я использовал две библиотеки
        # telethon - я использовал для получения данных из канала, чатов, изменений данных в них и тп
        run_telethon(),
        # aiogram - я использовал для для самого бота
        run_aiogram(),
        # теперь можно возвращаться обратно
    )
    
if __name__ == '__main__':
    try:
        asyncio.run(main()) 
        print("Aiogram bot started")
    except KeyboardInterrupt:
        print("Aiogram bot stopped")
        
