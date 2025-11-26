from aiogram import Router, types, F
from aiogram.filters import Command

from src.utils.cometApi.cometApi import cometApi
from aiogram.fsm.context import FSMContext
from src.utils.cometApi.classifyModels import ModelsClasses
from ...database.database import AsyncSessionLocal
from ...database.repositories.userRepo import UserRepository
from .keyboards.selectModelKeyboard import get_paginated_keyboard
from .keyboards import selectModelKeyboard
from .imageModels import imageModels as imageModelsRouter

router = Router()
router.include_routers(
    selectModelKeyboard.router,
    imageModelsRouter.router,
    )

@router.callback_query(F.data.split(":")[0] == 'select_model')
async def selectModel(call: types.CallbackQuery, state: FSMContext, userRepo: UserRepository):
    categoryModel = call.data.split(":")[1]
    await state.update_data({
        "changeModelCategory": categoryModel
    })
    
    
    await call.message.answer(userRepo.locale.ai_models_locale.getSelectModelText(), reply_markup=get_paginated_keyboard(
        cometApi.getModelsByCategory(categoryModel),
        0,
        nav_prefix="text_page"
    ))
    await call.answer()



@router.callback_query(F.data.split(":")[0] == 'change_model')
async def onModelSelected(call: types.CallbackQuery, state: FSMContext, userRepo: UserRepository):
    selectedModel = call.data.split(":")[1]
    data = await state.get_data()
    modelCategory = data.get('changeModelCategory')
    await userRepo.getSelectedModels()
    match modelCategory:
        case ModelsClasses.TEXTS.value:
            userRepo.user.selected_models.text_models = selectedModel
        
        case ModelsClasses.AUDIO.value:
            userRepo.user.selected_models.audio_models = selectedModel

        case ModelsClasses.IMAGES.value:
            userRepo.user.selected_models.image_models = selectedModel

        case ModelsClasses.EDITIND.value:
            userRepo.user.selected_models.editing_models = selectedModel

        case ModelsClasses.EMBENDS.value:
            userRepo.user.selected_models.embends_models = selectedModel
        
        case ModelsClasses.VIDEO.value:
            userRepo.user.selected_models.video_models = selectedModel

        case ModelsClasses.OTHER.value:
            userRepo.user.selected_models.other_models = selectedModel

    await userRepo.updateUser()

    await call.message.edit_text(userRepo.locale.ai_models_locale.getChangeModalText(selectedModel), parse_mode="HTML")
