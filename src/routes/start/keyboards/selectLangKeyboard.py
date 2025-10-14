from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_lang_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                    text = '🇺🇸 English',
                    callback_data = "changelang_en"
            ),
        ],
        [
            InlineKeyboardButton(
                    text = "🇷🇺 Русский",
                    callback_data = "changelang_ru"
            ),
        ],
        
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
