from datetime import datetime
from sqlalchemy import Integer, String, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .base import Base
from ...i18btn.getLang import getLocale
from ...i18btn.locales.ru import RuLocale

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lang: Mapped[str] = mapped_column(String, nullable=True, default='eng')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class UserRepository: 
    session: AsyncSession
    telegram_id: int
    user: User = None
    locale: RuLocale

    def __init__(self, session: AsyncSession,):
        self.session = session

    
    async def getUser(self, telegram_id):
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        self.user = result.scalar_one_or_none()
        if self.user:
            self.locale = getLocale(self.user.lang)

    async def createUser(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        self.user = user
        self.locale = getLocale(self.user.lang)

    async def updateUser(self):
        await self.session.commit()
        await self.session.refresh(self.user)
        self.locale = getLocale(self.user.lang)
