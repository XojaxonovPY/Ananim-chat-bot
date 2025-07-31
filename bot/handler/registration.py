from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import Router

from bot.buttons.inline import inline_button_builder
from bot.buttons.reply import reply_button_builder
from bot.states import States
from dp.model import User, City
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

register = Router()


@register.message(F.text == __('Registration'))
async def register_handler(message: Message, state: FSMContext):
    user_id = message.chat.id
    check = User.get(User.user_id, user_id)
    if check:
        await message.answer(text=_('You are already registered'))
        return
    await state.set_state(States.username)
    await message.answer(text=_("Enter username:"))


@register.message(States.username)
async def username_handler(message: Message, state: FSMContext):
    username = message.text
    text = [_('🧑 Man'), _('👩‍🦰 Women')]
    await state.update_data(username=username)
    await state.set_state(States.gender)
    markup = await reply_button_builder(text, (2,))
    await message.answer(text=_('Enter gender:'), reply_markup=markup)


@register.message(States.gender)
async def gender_handler(message: Message, state: FSMContext):
    gender = message.text
    await state.update_data(gender=gender)
    cities: list[City] = City.get_all()
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'city_{i.id}') for i in cities]
    markup = await inline_button_builder(buttons, [2] * (len(cities) // 2))
    await message.answer(text=_('Enter city:'), reply_markup=markup)


@register.callback_query(F.data.startswith('city_'))
async def city_handler(callback: CallbackQuery, state: FSMContext):
    texts = [_('◀️ Back'), _('💬 Chats')]
    city = int(callback.data.split('_')[1])
    data = await state.get_data()

    markup = await reply_button_builder(texts, (2,))
    users = {
        'user_id': callback.message.chat.id,
        'name': data.get('username'),
        'gender': data.get('gender'),
        'username': callback.message.chat.username,
        'city_id': city,
    }
    User.save(**users)
    await state.clear()
    await callback.message.answer(text=_('Data saved'), reply_markup=markup)
