from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.utils.cometApi.classifyModels import ModelsClasses


def mainKeyboard(buttonsTexts: list):
    buttons = [
        [
            InlineKeyboardButton(text=buttonsTexts[0], callback_data=f'select_model:{ModelsClasses.TEXTS.value}')
        ],
        [
            InlineKeyboardButton(text=buttonsTexts[1], callback_data='back_main'),
        ],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
