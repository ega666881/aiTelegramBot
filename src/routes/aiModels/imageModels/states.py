from aiogram.fsm.state import StatesGroup, State

class ImageModelStates(StatesGroup):
    GET_MJ_PROMT_MESSAGE = State()
    GET_GEMENI_PROMT_MESSAGE = State()
