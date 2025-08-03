from aiogram import F
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import inline_button_builder
from bot.buttons.reply import reply_button_builder
from dp.model import City, User

region = Router()


@region.message(F.text == __('🇺🇿 City'))
async def regions_handler(message: Message):
    cities = City.get_all()
    if not cities:
        await message.answer(_('🚫 No cities found.'))
        return

    buttons = [InlineKeyboardButton(text=city.name, callback_data=f"cities_{city.id}") for city in cities]
    markup = await inline_button_builder(buttons, size=(2, 2))
    await message.answer(text=_('🌆 Choose a city:'), reply_markup=markup)


@region.callback_query(F.data.startswith("cities_"))
async def city_selected(callback: CallbackQuery):
    city_id = int(callback.data.split("_")[1])
    users: list[User] = User.get(User.city_id, city_id, all=True)
    buttons = [InlineKeyboardButton(text=i.name, callback_data=f'user_{i.id}') for i in users]
    markup = await inline_button_builder(buttons, [2] * len(buttons))
    await callback.message.answer(text=_('✅ Chose users:'), reply_markup=markup)


@region.callback_query(F.data.startswith("user_"))
async def movie_choice(callback: CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    text = [_('👥 Send message user')]
    markup = await reply_button_builder(text)
    user: User = User.get(User.id, user_id)
    name_text = f"<code>{user.name}</code>"
    await callback.message.answer(text=f"✅ User: {name_text}", reply_markup=markup, parse_mode="HTML")
