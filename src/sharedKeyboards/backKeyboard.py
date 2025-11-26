from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def backKeyboard(buttonText: str, backUrl: str):
    print(buttonText, backUrl)
    buttons = [
        [
            InlineKeyboardButton(text=buttonText, callback_data=backUrl),

        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
