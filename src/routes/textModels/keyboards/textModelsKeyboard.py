from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def mainKeyboard(buttonsTexts: list):
    buttons = [
        [
            InlineKeyboardButton(text=buttonsTexts[0], callback_data='select_model')
        ],
        [
            InlineKeyboardButton(text=buttonsTexts[1], callback_data='back_main'),
        ],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
