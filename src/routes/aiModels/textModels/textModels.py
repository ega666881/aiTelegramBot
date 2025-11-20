from aiogram import Router, types, F
from aiogram.filters import Command


from aiogram.fsm.context import FSMContext
from ....database.database import AsyncSessionLocal
from ....database.models.user import User, UserRepository
from .states import TextModelStates
from src.utils.aiModels import textModels
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
        sendedMessage = await message.answer(userRepo.locale.ai_models_locale.getWaitAnswerText())
        modelResponse = await textModels.sendRequest('gpt-4o', userRepo.user, message.text, messages_history)
        
        messages_history.append({
            "role": "user",
            "content": message.text,
        })
        messages_history.append(modelResponse['answer'])
        await state.update_data({
            "messages_history": messages_history
        })
        messageText = f"{modelResponse['answerText']}"

        await sendedMessage.edit_text(
            text=messageText,
            parse_mode="Markdown"
        )
        

       

        