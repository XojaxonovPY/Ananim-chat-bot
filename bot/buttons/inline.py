from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
def inline_button_builder(text:list, size,one_time=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=text, callback_data=data) for text, data in text])
    ikb.adjust(*size)
    ikb = ikb.as_markup()
    return ikb