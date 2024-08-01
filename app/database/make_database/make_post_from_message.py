from app.database.models import Post_
from aiogram.types import Message
import re

from data import input_channel

# для объекта Post_ из Message нужно выкачить следующее :
async def make_post_from_message(message: Message):
    if isinstance(message.text, str): 
        print("isinstance(message.text, str) == true")

        # все хештеги, которые потом деляется на Темы и Админов
        hashtags = re.findall(r"#(\w+)", message.text)  
        admin_hashtags = [hashtag for hashtag in hashtags if hashtag.startswith("admin_")]
        theme_hashtags = [theme for theme in hashtags if not theme.startswith("admin_")]
                    
        author = ""
        themes = ""
                    
        if len(admin_hashtags) >= 1:
            author = ", ".join(admin_hashtags) if admin_hashtags else ""
        else:
            author = "No author"

        if len(theme_hashtags) >= 1:
            themes = ", ".join(theme_hashtags) if theme_hashtags else ""
        else:
            themes = "No themes"
        post_ =  Post_(channel=input_channel, 
                               id=message.id, 
                              post_link=f"https://t.me/wouwouwou345/{message.id}", 
                              themes=themes,
                              author=author)     
        return post_