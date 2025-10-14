from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profileKeyboard(buttonsTexts: list):
    buttons = [
        [
            InlineKeyboardButton(
                    text = buttonsTexts[0],
                    callback_data = "buy_tokens"
            ),
        ],

        
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
