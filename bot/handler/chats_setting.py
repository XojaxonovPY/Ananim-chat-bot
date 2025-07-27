from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from bot.buttons.inline import inline_button_builder
from dp.model import User

chat_settings = Router()


@chat_settings.message(Command('delete'))
async def delete_user(message: Message, state: FSMContext):
    query = User.get(User.id, message.from_user.id)
    if not query:
        await message.answer(text='You are not allowed to do that')

    text = [
        InlineKeyboardButton(text=_('✅Yes'), callback_data='yes'),
        InlineKeyboardButton(text=_('❌NO'), callback_data='no')
    ]
    markup = inline_button_builder(text)
    await message.answer(text=_('Do you delete your chat?'), reply_markup=markup)


@chat_settings.callback_query(F.data == 'yes')
async def user_deleted(callback: CallbackQuery):
    user_id = callback.from_user.id
    User.delete(User.user_id, user_id)
    await callback.message.answer(text=_('✅ Chat is deleted'))


@chat_settings.callback_query(F.data == 'no')
async def user_not_deleted(callback: CallbackQuery):
    await callback.message.answer(text=_('✅ Thanks for staying on our channel!'))


@chat_settings.message(Command('my_own'))
async def get_user(message: Message):
    user_id = message.from_user.id
    user:User = User.get(User.user_id,user_id)
    information=f'Name: {user.name}\nGender: {user.gender}\nCity: {user.city.name}'
    if user:
        await message.answer(text=information)
    else:
        await message.answer(text=_('No information'))
        return
    await message.answer(text=_('Datas fetched'))
