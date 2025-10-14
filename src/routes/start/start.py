from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.database import AsyncSessionLocal
from ...database.models.user import User, UserRepository
from ...i18btn.getLang import getLocale
from .keyboards.selectLangKeyboard import select_lang_keyboard
from .keyboards.mainMenuKeyboard import mainMenuKeyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    async with AsyncSessionLocal() as session:
        
        userRepo = UserRepository(session)
        
        await userRepo.getUser(message.from_user.id)
        
        if not userRepo.user:
            await userRepo.createUser(User(
                telegram_id = message.from_user.id,
                username = message.from_user.username,
                tokens = 5,
                lang = message.from_user.language_code
            ))
        

        
        await message.answer(userRepo.locale.start_locale.getStartMessage(), reply_markup=select_lang_keyboard())


@router.callback_query(F.data.split('_')[0] == 'changelang')
async def select_lang(call: types.CallbackQuery): 
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(call.from_user.id)
        
        selected_lang = call.data.split('_')
        userRepo.user.lang = selected_lang[1]
        await userRepo.updateUser()
        
        await call.message.answer(userRepo.locale.start_locale.getMainMenuMessage(), reply_markup=mainMenuKeyboard(userRepo.locale.start_locale.getMainMenuKeyboardText()))

        