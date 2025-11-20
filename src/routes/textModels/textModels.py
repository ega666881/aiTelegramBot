from aiogram import Router, types, F
from aiogram.filters import Command
import aiogram.fsm.context
from sqlalchemy import select

from aiogram.fsm.context import FSMContext
from ...database.database import AsyncSessionLocal
from ...database.models.user import User, UserRepository
from .states import TextModelStates
from .keyboards import textModelsKeyboard

router = Router()

@router.callback_query(F.data == 'textModels')
async def textModels(call: types.CallbackQuery, state: FSMContext): 
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(call.from_user.id)
        await state.set_state(TextModelStates.GET_PROMT_MESSAGE)
        await call.message.edit_text(
            userRepo.locale.text_models_locale.getHelloMessage(),
            reply_markup=textModelsKeyboard.mainKeyboard(userRepo.locale.text_models_locale.getMainButtons())
        )

@router.message(TextModelStates.GET_PROMT_MESSAGE)
async def getPromt(message: types.Message, state: FSMContext):
    pass
        
       

        