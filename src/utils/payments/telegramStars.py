from aiogram import Bot, Dispatcher, Router, F
from ...i18btn.locales.ru import RuLocale
from aiogram.types import LabeledPrice
from ...routes.payments.enums import PaymentType


async def createInvoice(bot: Bot, amount: int, type: str, locale: RuLocale, buyType: PaymentType):
    prices = [
        LabeledPrice(label=f"{amount} tokens", amount=amount),
    ]
    return await bot.create_invoice_link(
        title=locale.payment_locale.getTypesPaymentsTitles()[type],
        description=locale.payment_locale.getTypesPaymentsTitles()[type],
        payload=f"{buyType}_{amount}",
        provider_token="",
        currency="XTR",
        prices=prices,
    )