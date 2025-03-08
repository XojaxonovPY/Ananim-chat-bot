from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from bot.handler.registration import uzbekiston_viloyatlari
from bot.buttons.inline import inline_button_builder
from bot.buttons.reply import reply_button_builder
from bot.states import States
from dp.model import User
from aiogram.utils.i18n import gettext as _
from bot.middilwares import is_str
chat_settings=Router()

@chat_settings.message(Command('delete'))
async  def delete_user(message:Message,state:FSMContext):
    user_id=message.chat.id
    await state.update_data(user_id=user_id)
    text=[(_('✅Yes'),'yes'),(_('❌NO'),'no')]
    markup=inline_button_builder(text,(1,1))
    await message.answer(text=_('Do you delete your chat?'),reply_markup=markup)

@chat_settings.callback_query(F.data=='yes')
async def user_deleted(callback:CallbackQuery,state:FSMContext):
    data=await state.get_data()
    user_id=data.get('user_id')
    check=User.check_user(user_id)
    if check:
        User.dlt(user_id)
    else:
        await callback.message.answer(text=_('Your not register!'))
        return
    await state.clear()
    await callback.message.answer(text=_('✅ Chat is deleted'))

@chat_settings.callback_query(F.data=='no')
async def user_not_deleted(callback:CallbackQuery):
    await callback.message.answer(text=_('✅ Thanks for staying on our channel!'))


@chat_settings.message(Command('update'))
async def update_user(message:Message,state:FSMContext):
    user_id=message.chat.id
    text=['username','password','gender','city']
    markup=reply_button_builder(text,(2,2))
    await state.set_state(States.column_name)
    await state.update_data(user_id=user_id)
    await message.answer(text=_('Which one you want to change?'),reply_markup=markup)

@chat_settings.message(States.column_name)
async def user_update(message:Message,state:FSMContext):
    column1=message.text
    markup=None
    if column1 == 'gender':
        text = [_('🧑 Man'), _('👩‍🦰 Women')]
        markup=reply_button_builder(text,(2,))
    elif column1 == 'city':
        text = uzbekiston_viloyatlari
        markup = reply_button_builder(text, (2, 2, 2, 2, 2, 2))
    await state.update_data(column1=column1)
    await state.set_state(States.new_column)
    if markup:
        await message.answer(text=_('Enter new value'), reply_markup=markup)
    else:
        await message.answer(text=_('Enter new value'))

@chat_settings.message(States.new_column)
async def change_column(message:Message,state:FSMContext):
    column2=message.text
    await state.update_data(column2=column2)
    data=await state.get_data()
    user_id=data.get('user_id')
    column_name=data.get('column1')
    new_column=data.get('column2')
    check=User.check_user(user_id)
    if check:
        User.ups(user_id, **{column_name: new_column})
    else:
        await message.answer(text=_('Your not register!'))
    await message.answer(text=_(f'{column_name} changed ✅'))

@chat_settings.message(Command('my_own'))
async def get_user(message:Message):
    user_id=message.chat.id
    print(user_id)
    check=User.check_user(user_id)
    user = is_str(User.get(User.user_id, user_id, User.username, User.gender))
    if check:
        await message.answer(text=user)
    else:
        await message.answer(text=_('No information'))
        return
    await message.answer(text=_('Datas fetched'))




