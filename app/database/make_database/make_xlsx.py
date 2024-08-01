from telethon.sync import TelegramClient
import datetime
import pandas as pd
import re

from data import API_HASH, API_ID, input_channel

api_id = API_ID
api_hash = API_HASH
channels = [input_channel]

async def make_xlsx():
    print(f"make_xlsx")
    df = pd.DataFrame()
    # в принципе расчитано было на то, что каналов уже несколько
    for channel in channels:
        async with TelegramClient('test', api_id, api_hash) as client:
            async for message in client.iter_messages(channel, reverse=True):
                print(message)
            
                if isinstance(message.text, str):
                    # в принципе, мы тут делаем всё тот же Post_
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
                
                    data = {
                        "channel": channel,
                        "post_number": message.id,
                        "post_link": f"https://t.me/{channel}/{message.id}",
                        "hashtags": themes, # Объединяем хештеги в строку
                        "author": author
                    }
                
                    temp_df = pd.DataFrame(data, index=[1])
                    df =  df._append(temp_df)

    df.to_excel(f"data.xlsx", index=False)


