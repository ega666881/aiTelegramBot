from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def mainMenuKeyboard(buttonsTexts: list):
    buttons = [
        [
            InlineKeyboardButton(text=buttonsTexts[0], callback_data='select_mj')
        ],
        [
            InlineKeyboardButton(text=buttonsTexts[1], callback_data='back_main'),

        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
