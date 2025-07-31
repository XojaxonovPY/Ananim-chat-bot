from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def inline_button_builder(text: list, size=(1,), one_time=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(*text)
    ikb.adjust(*size)
    ikb = ikb.as_markup()
    return ikb
