
from ..models.user import User, UserSelectedModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager
from ...i18btn.locales.ru import RuLocale
from ...i18btn.getLang import getLocale
from sqlalchemy import select

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

    async def getSelectedModels(self): 
        selected_models = await self.session.scalar(
            select(UserSelectedModel).where(UserSelectedModel.user_id == self.user.id)
        )
        self.user.selected_models = selected_models

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
