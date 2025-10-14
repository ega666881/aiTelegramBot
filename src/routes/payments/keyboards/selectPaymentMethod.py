from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ....i18btn.locales.ru import RuLocale

def selectPaymentMethodKeyboard(locale: RuLocale):
    buttons = [
        [
            InlineKeyboardButton(
                    text = 'Telegram stars 🌟',
                    callback_data = "paymentMethod_tgstars"
            ),
            
        ],
        [
            InlineKeyboardButton(
                    text = locale.shared_texts.getSharedTexts()['cancel'],
                    callback_data = "cancel_payment"
            ),
        ]

        
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
