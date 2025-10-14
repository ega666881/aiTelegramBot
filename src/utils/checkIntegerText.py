from aiogram import types
from ..i18btn.locales.ru import RuLocale

async def checkIntegerText(message: types.Message, locale: RuLocale) -> int | None:
    locales = locale.payment_locale.getErrorsAmountTexts()
    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer(locales[0])
            return None
        
        return amount
    
    except (ValueError, TypeError):
        await message.answer(locales[1])
        return None