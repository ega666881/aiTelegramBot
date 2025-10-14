from aiogram.fsm.state import StatesGroup, State

class PaymentStates(StatesGroup):
    GET_PAYMENT_AMOUNT = State()
