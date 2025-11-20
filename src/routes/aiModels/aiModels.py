from aiogram import Router, types, F
from aiogram.filters import Command

from src.utils.cometApi.cometApi import cometApi
from aiogram.fsm.context import FSMContext
from ...database.database import AsyncSessionLocal
from ...database.models.user import User, UserRepository
from .keyboards.selectModelKeyboard import get_paginated_keyboard

from .keyboards import selectModelKeyboard

router = Router()
router.include_router(selectModelKeyboard.router)

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
    await call.message.edit_text(userRepo.locale.ai_models_locale.getChangeModalText(selectedModel), parse_mode="HTML")