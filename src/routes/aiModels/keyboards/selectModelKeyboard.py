from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from src.utils.cometApi.cometApi import cometApi

def get_paginated_keyboard(items, page=0, per_page=8, nav_prefix="page"):
    total = len(items)
    total_pages = (total + per_page - 1) // per_page
    start = page * per_page
    end = min(start + per_page, total)

    buttons = [
        [types.InlineKeyboardButton(text=item, callback_data=f"change_model:{item}")]
        for item in items[start:end]
    ]

    nav = []
    if page > 0:
        nav.append(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{nav_prefix}:{page - 1}"))

    if page < total_pages - 1:
        nav.append(types.InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"{nav_prefix}:{page + 1}"))

    if nav:
        buttons.append(nav)

    buttons.append(
        [
            types.InlineKeyboardButton(text="Отмена", callback_data=f"textModels")
        ]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


router = Router()

@router.callback_query(
    F.data.startswith("text_page:")
)
async def handle_pagination(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":", 1)[1])
    data = await state.get_data()
    models = cometApi.getModelsByCategory(data['changeModelCategory'])


    keyboard = get_paginated_keyboard(
        items=models,
        page=page,
        nav_prefix="text_page"
    )
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()
