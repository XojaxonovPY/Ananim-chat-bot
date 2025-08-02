from aiogram.fsm.state import StatesGroup,State
class States(StatesGroup):
    gender=State()
    username=State()
    region=State()
    chat_user=State()
    send_messages=State()
    language=State()