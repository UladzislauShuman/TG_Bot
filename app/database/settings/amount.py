from app.database.models import async_session
from app.database.models import User, Post, Theme, Post_
from sqlalchemy import select, func, cast, Integer       
        
async def set_new_amount(tg_id, amount_str):
     async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        int_amount = int(amount_str)
        
        if user:
            
            if int_amount > 10 or int_amount < 0:
                print("no change")
            else:
                user.amount = amount_str
                
            await session.commit()
         
async def get_amount(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user.amount
        