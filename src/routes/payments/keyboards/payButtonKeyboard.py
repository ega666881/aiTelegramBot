from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ....i18btn.locales.ru import RuLocale

def payKeyboard(locale: RuLocale, payUrl: str):
    buttons = [
        [
            InlineKeyboardButton(
                    text = locale.shared_texts.getSharedTexts()['pay'],
                    url = payUrl
            ),
            
        ],        
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
