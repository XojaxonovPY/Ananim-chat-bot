from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from bot.buttons.reply import reply_button_builder
from bot.buttons.inline import inline_button_builder
from bot.states import States
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from bot.middilwares import users_format,uzbekiston_viloyatlari
region=Router()


@region.message(F.text==__('🇺🇿 City'))
@region.message(F.text==__("◀️City back"))
async def regions_handler(message:Message,state:FSMContext):
    text=uzbekiston_viloyatlari
    markup=reply_button_builder(text,(2,2,2,2,2,2,2))
    await message.answer(text=_('Chose city:'),reply_markup=markup)


@region.message(F.text.in_(uzbekiston_viloyatlari))
async def category_handler(message: Message, state: FSMContext):
    city = message.text
    page = 1
    user_names = users_format(city, page)
    await state.update_data(users=user_names)
    await state.set_state(States.users)
    buttons = [(str(i), f"choice_{i}") for i in range(1, len(user_names) + 1)]
    buttons.append((_("prev"),f"pos_{page - 1}"))
    buttons.append((_("next"), f"pos_{page + 1}"))
    markup = inline_button_builder(buttons, size=(5, 5, 2))
    markup1 = reply_button_builder([_("◀️City back"),_('◀️ Main back')], (1,))
    await message.answer(text=_("List users"), reply_markup=markup1)
    await message.answer(text="\n".join(user_names), reply_markup=markup)


@region.message(States.users,F.data.startswith('pos_'))
async def category_handler(callback:CallbackQuery, state: FSMContext):
    city = callback.message.text
    page = int(callback.data.split("_")[-1])
    user_names = users_format(city, page)
    if not user_names:
        await callback.answer(text=_('Invalid selection'))
    else:
        await state.update_data(users=user_names)
        await state.set_state(States.users)
        buttons = [(str(i), f"choice_{i}") for i in range(1, len(user_names) + 1)]
        buttons.append(("prev", f"pos_{page - 1}"))
        buttons.append(("next", f"pos_{page + 1}"))
        markup = inline_button_builder(buttons, size=(5, 5, 2))
        markup1 = reply_button_builder([_("◀️City back")], (1,))
        await callback.message.answer(text=_("List users"), reply_markup=markup1)
        await callback.message.answer(text="\n".join(user_names), reply_markup=markup)


@region.callback_query(States.users)
async def movie_choice(callback : CallbackQuery , state : FSMContext):
    pos = int(callback.data.split("_")[-1]) - 1
    text=[_('👥 Send message user'),]
    markup=reply_button_builder(text,(1,))
    data = await state.get_data()
    users = data.get('users', [])
    if pos < 0 or pos >= len(users):
        await callback.answer(_("Invalid selection"))
        return
    username = users[pos]
    await callback.message.answer(text=f"User: {username}",reply_markup=markup)



