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
async def imageModelsHandler(call: types.CallbackQuery, userRepo: UserRepository, state: FSMContext):
    await state.set_state(None)
    await call.message.edit_text(
        userRepo.locale.image_models_locale.getHelloMessage(), 
        reply_markup=selectImageModelKeyboard.mainMenuKeyboard(userRepo.locale.image_models_locale.getMainButtons())
        )

@router.callback_query(F.data == 'select_mj')
async def selectMjModel(call: types.CallbackQuery, state: FSMContext, userRepo: UserRepository):
    await state.set_state(ImageModelStates.GET_MJ_PROMT_MESSAGE)
    senderMessage = call.message.answer
    if not call.message.photo:
        senderMessage = call.message.edit_text

    await senderMessage(
            userRepo.locale.image_models_locale.getMjPromtMessage(),
            reply_markup=backKeyboard.backKeyboard(userRepo.locale.image_models_locale.getMainButtons()[2], 'imageModels')
        )

@router.callback_query(F.data == 'select_gem')
async def selectGemModel(call: types.CallbackQuery, state: FSMContext, userRepo: UserRepository):
    await state.set_state(ImageModelStates.GET_GEMENI_PROMT_MESSAGE)
    senderMessage = call.message.answer
    if not call.message.photo:
        senderMessage = call.message.edit_text

    await senderMessage(
        userRepo.locale.image_models_locale.getGemeniPromtMessage(),
        reply_markup=backKeyboard.backKeyboard(userRepo.locale.image_models_locale.getMainButtons()[2], 'imageModels')
    )

@router.message(ImageModelStates.GET_GEMENI_PROMT_MESSAGE)
async def getGemeniPromt(message: types.Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(message.from_user.id)
        await state.set_state(None)
        sendedMessage = await message.answer(
            userRepo.locale.ai_models_locale.getWaitAnswerText()
        )
        photo = await imageModels.sendGemeniRequest(userRepo.user, message.text)
        answerPhoto = types.InputMediaPhoto(
                media=photo,
            )

        await sendedMessage.edit_media(
            media=answerPhoto,
            reply_markup=backKeyboard.backKeyboard(userRepo.locale.image_models_locale.getMjAnswerButtons()[0], 'select_gem')
        )

@router.message(ImageModelStates.GET_MJ_PROMT_MESSAGE)
async def getMjPromt(message: types.Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(message.from_user.id)
        await imageModels.sendMjRequest('mj_turbo_blend', userRepo.user, message.text)
        await message.answer(userRepo.locale.image_models_locale.getMjSendReqMessage())
        await state.set_state(None)