from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_#, Category, Item
from sqlalchemy import select, func, cast, Integer


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, 
                             setting='default', 
                             amount='5',
                             author="admin_Ѱsinα",
                             theme="мат",
                             current_page=0,
                             current_theme='null',
                             current_max_page=0,
                             rights="user"))
            await session.commit()

# я не придумал ничего лучше, кроме как при листании страниц (Темы, выбрали тему и теперь - листайте)
# сохранять текущую страницу внутри пользователя
async def set_user_page_theme(tg_id, theme_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.current_page = 1
            user.current_theme = theme_id
            
            query = select(Post_).where(Post_.themes.like(f'%{user.current_theme}%')).order_by(Post_.id.desc())
            result = await session.scalars(query)
            list_of_posts = result.all()
            user_amount = int(user.amount)
            page_of_posts = [list_of_posts[i:i+user_amount] for i in range(0, len(list_of_posts), user_amount)]
            
            user.current_max_page = len(page_of_posts)
            await session.commit()
            
          
async def set_user_page(tg_id, page):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.current_page = page
            await session.commit()

async def get_user_page(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.current_page
        else:
            return 0

# вот это нужно, чтобы была возможность с первой страницы
# свернуть на страницу назад, ну и в итоге попасть на последнюю страницу
async def get_user_max_page(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.current_max_page
        else:
            return 0
                          
async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User)) 
