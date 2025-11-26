from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from src.database.repositories.userRepo import UserRepository
import src.utils.aiModels
from src.database.database import AsyncSessionLocal
from .keyboards import selectImageModelKeyboard
from .states import ImageModelStates
from src.sharedKeyboards import backKeyboard
from src.utils.aiModels import imageModels

router = Router()


@router.callback_query(F.data == 'imageModels')
async def imageModelsHandler(call: types.CallbackQuery, userRepo: UserRepository):
    await call.message.edit_text(
        userRepo.locale.image_models_locale.getHelloMessage(), 
        reply_markup=selectImageModelKeyboard.mainMenuKeyboard(userRepo.locale.image_models_locale.getMainButtons())
        )

@router.callback_query(F.data == 'select_mj')
async def selectMjModel(call: types.CallbackQuery, state: FSMContext, userRepo: UserRepository):
    await state.set_state(ImageModelStates.GET_MJ_PROMT_MESSAGE)
    await call.message.edit_text(
        userRepo.locale.image_models_locale.getMjPromtMessage(),
        reply_markup=backKeyboard.backKeyboard(userRepo.locale.image_models_locale.getMainButtons()[1], 'imageModels')
        )
    
@router.message(ImageModelStates.GET_MJ_PROMT_MESSAGE)
async def getMjPromt(message: types.Message):
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(message.from_user.id)
        await imageModels.sendMjRequest('mj_turbo_blend', userRepo.user, message.text)
        await message.answer(userRepo.locale.image_models_locale.getMjSendReqMessage())