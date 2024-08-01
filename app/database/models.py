from sqlalchemy import BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

# в принципе, всё то, что я храню о вас 

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
    setting: Mapped[str] = mapped_column(Text) 
    amount: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(Text)
    theme: Mapped[str] = mapped_column(Text)
    
    current_page: Mapped[int] = mapped_column(primary_key=True)
    current_theme: Mapped[str] = mapped_column(Text)
    current_max_page: Mapped[int] = mapped_column(primary_key=True)
    
    rights: Mapped[str] = mapped_column(Text)
    
class Post(Base):
    __tablename__ = 'Post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(Text)
    
class Theme(Base):
    __tablename__ = 'Themes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    
class Author(Base):
    __tablename__ = "Authors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text) 

class Post_(Base):
    __tablename__ = "Post_"
    
    channel: Mapped[str] = mapped_column(Text)
    id: Mapped[int] = mapped_column(primary_key=True)
    post_link: Mapped[str] = mapped_column(Text)
    themes: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(Text)
    
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
