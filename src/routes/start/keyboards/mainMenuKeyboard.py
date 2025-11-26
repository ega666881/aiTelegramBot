from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def mainMenuKeyboard(buttonsTexts: list):
    buttons = [
        [
            InlineKeyboardButton(text=buttonsTexts[0], callback_data='profile')
        ],
        [
            InlineKeyboardButton(text=buttonsTexts[1], callback_data='textModels'),
            InlineKeyboardButton(text=buttonsTexts[2], callback_data='profile'),
        ],
        [
            InlineKeyboardButton(text=buttonsTexts[3], callback_data='imageModels'),
            InlineKeyboardButton(text=buttonsTexts[4], callback_data='profile'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
