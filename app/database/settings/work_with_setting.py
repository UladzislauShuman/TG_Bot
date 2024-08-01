# from app.database.models import async_session
# from app.database.models import User, Post, Theme, Post_
# from sqlalchemy import select, func, cast, Integer 

# async def set_new_setting(tg_id, setting):
#      async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             user.setting = setting
#             await session.commit()
         
# async def get_setting(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.setting 
        
            
# async def set_new_amount(tg_id, amount_str):
#      async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         int_amount = int(amount_str)
        
#         if user:
            
#             if int_amount > 10 or int_amount < 0:
#                 print("no change")
#             else:
#                 user.amount = amount_str
                
#             await session.commit()
         
# async def get_amount(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.amount
        
# from app.database.models import Author      
        
# async def set_new_authors(tg_id, author):
#      async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             user.author = author
#             await session.commit()
         
# async def get_authors_user(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.author.split(", ") 
# async def get_authors_post(post_:Post_):
#     async with async_session() as session:
#         return post_.author.split(", ")    
         
# async def get_authors_str(tg_id):
#     async with async_session() as session:
#         user = await session. scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.author
        
# async def get_all_authors():
#     async with async_session() as session:
#         return await session.scalars(select(Author)) 
        
# from app.database.models import Theme      
        
# async def set_new_themes(tg_id, theme):
#      async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             user.theme = theme
#             await session.commit()
         
# async def get_themes_user(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.theme.split(", ") 
# async def get_themes_post(post_:Post_):
#     async with async_session() as session:
#         return post_.themes.split(", ")    
         
# async def get_themes_str(tg_id):
#     async with async_session() as session:
#         user = await session. scalar(select(User).where(User.tg_id == tg_id))
#         if user:
#             return user.theme
        
# async def get_all_themes():
#     async with async_session() as session:
#         return await session.scalars(select(Theme)) 
        