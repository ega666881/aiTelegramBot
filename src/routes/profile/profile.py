from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import AsyncSessionLocal
from ...database.models.user import User, UserRepository
from .keyboards.profileKeyboard import profileKeyboard



router = Router()




@router.callback_query(F.data == 'profile')
async def profileMenu(call: types.CallbackQuery):
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(call.from_user.id)
        await call.message.answer(
                userRepo.locale.profile_locale.getProfileMenuText(userRepo.user.tokens),
                reply_markup=profileKeyboard(buttonsTexts=userRepo.locale.profile_locale.getProfileKeyboardText())
            )