from aiogram import Router, types, F
from aiogram.filters import Command


from aiogram.fsm.context import FSMContext
from src.utils.cometApi.classifyModels import classify_model, getClassifyModels, ModelsClasses
from ....database.database import AsyncSessionLocal
from ....database.repositories.userRepo import UserRepository
from .states import TextModelStates
from src.utils.aiModels import textModels, imageModels
from .keyboards import textModelsKeyboard


router = Router()

@router.callback_query(F.data == 'textModels')
async def textModelsHandler(call: types.CallbackQuery, state: FSMContext): 
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
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        data = await state.get_data()
        messages_history = []
        if "messages_history" in data.keys():
            messages_history = data['messages_history']

        await userRepo.getUser(message.from_user.id)
        await userRepo.getSelectedModels() 
        sendedMessage = await message.answer(userRepo.locale.ai_models_locale.getWaitAnswerText())

        categoryModel = classify_model(userRepo.user.selected_models.text_models)

        if (categoryModel == ModelsClasses.TEXTS.value):
            modelResponse = await textModels.sendRequest(userRepo.user.selected_models.text_models, userRepo.user, message.text, messages_history)
        
        elif (categoryModel == ModelsClasses.IMAGES.value):
            modelResponse = await imageModels.sendRequest(userRepo.user.selected_models.text_models, userRepo.user, message.text, messages_history)

        messages_history.append({
            "role": "user",
            "content": message.text,
        })
        messages_history.append(modelResponse['answer'])
        await state.update_data({
            "messages_history": messages_history
        })
        messageText = f"{modelResponse['answerText']}"

        if 'answerPhoto' in modelResponse:
            answerPhoto = types.InputMediaPhoto(
                media=modelResponse['answerPhoto'],
                caption=modelResponse['answerPhoto']
            )
            await sendedMessage.edit_media(
                media=answerPhoto,
                
            )
        else:
            await sendedMessage.edit_text(
                text=messageText,
                parse_mode="Markdown"
            )
            

       

        