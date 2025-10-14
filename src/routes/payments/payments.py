from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from ...database.database import AsyncSessionLocal
from ...database.models.user import User, UserRepository
from .keyboards.selectPaymentMethod import selectPaymentMethodKeyboard
from .keyboards.payButtonKeyboard import payKeyboard
from .states import PaymentStates
from ...utils.payments import telegramStars
from ...utils.checkIntegerText import checkIntegerText
from .enums import PaymentType

router = Router()



@router.callback_query(F.data == 'buy_tokens')
async def buy_tokens(call: types.CallbackQuery):
    async with AsyncSessionLocal() as session: 
        userRepo = UserRepository(session)
        await userRepo.getUser(call.from_user.id)
        await call.message.answer(userRepo.locale.profile_locale.getSelectPaymentMethodText(), reply_markup= selectPaymentMethodKeyboard(userRepo.locale))



@router.callback_query(F.data.split('_')[0] == 'paymentMethod')
async def selectedPaymentMethod(call: types.CallbackQuery, state: FSMContext):
    async with AsyncSessionLocal() as session: 
        userRepo = UserRepository(session)
        await userRepo.getUser(call.from_user.id)
        
        
        paymentMethod = call.data.split('_')[1]
        await state.update_data({"paymentMethod": paymentMethod})
        await state.set_state(PaymentStates.GET_PAYMENT_AMOUNT)
        await call.message.answer(userRepo.locale.profile_locale.getBuyTokensText(1, '🌟'))


@router.message(PaymentStates.GET_PAYMENT_AMOUNT)
async def getAmountPayment(message: types.Message, state: FSMContext, bot: Bot):
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(message.from_user.id)
        amount = await checkIntegerText(message, userRepo.locale)
        if amount:
            stateData = await state.get_data()
            paymentMethod = stateData['paymentMethod']
            invoiceUrl = await telegramStars.createInvoice(
                bot, 
                amount, 
                'tokens', 
                userRepo.locale,
                PaymentType.BUY_TOKENS,
            )
            await message.answer(
                userRepo.locale.payment_locale.getPayCheckText(amount, '🌟'),
                reply_markup=payKeyboard(userRepo.locale, invoiceUrl)
            )
            await state.set_state(None)

@router.pre_checkout_query()
async def handle_pre_checkout(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def handle_successful_payment(message: types.Message):
    payment = message.successful_payment
    total_stars = payment.total_amount
    payload = payment.invoice_payload
    async with AsyncSessionLocal() as session:
        userRepo = UserRepository(session)
        await userRepo.getUser(message.from_user.id)
        buyType = payload.split('_')[0]
        buyAmount = payload.split('_')[1]

        match (buyType):
            case PaymentType.BUY_TOKENS:
               userRepo.user.tokens += int(buyAmount)
               await userRepo.updateUser()
               await message.answer(
                   userRepo.locale.payment_locale.getSuccessPaymentTokensText(int(buyAmount))
               )

        
        
