import pandas as pd
import sqlite3
import asyncio

async def convert_xlsx_to_sqlite():
    print(f"convert_xlsx_to_sqlite")
    # Чтение XLSX файла
    df = pd.read_excel("data.xlsx")

    # Создание базы данных
    conn = sqlite3.connect("inf_about_posts.db")

    # Создание таблицы
    df.to_sql("post_information", conn, if_exists="replace", index=False)

    # Закрытие соединения
    conn.close()
