from app.database.make_database.make_xlsx import make_xlsx
from app.database.make_database.convert_xlsx_to_sqlite import convert_xlsx_to_sqlite
# запустив этот файл вы создаётся базу данных (файл формата sqlite3)
# и не самым Гуманным путём, а именно - созданием xlsx таблицы, а
# затем конвертацией таковой в нужный формат, а уж потом я беру и 
# своими руками переношу в нужный файл
# (это было нужно в процессе, когда нужно было просто выкачить
# инфу с канала, но потом планировалось переделать под другие нужды, но
# пока не получилось)
async def make_xlsx_():
    await make_xlsx()
    await convert_xlsx_to_sqlite()
    
import asyncio
#asyncio.run(make_xlsx_())