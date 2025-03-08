from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.types import  InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram import Router, F
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.buttons.reply import reply_button_builder
from bot.states import States
from utils.env_data import BotConfig
from dp.model import User,Chat,Message as m
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
chat=Router()

bot=Bot(token=BotConfig.TOKEN)


@chat.message(F.text==__('💬 My chat'))
@chat.message( F.text==__('💬 Chats'))
@chat.message(F.text==__('❌ End Chat'))
@chat.message(F.text==__('◀️ Main back'))
async def chat_handler(message:Message,state:FSMContext):
    text=[_('🇺🇿 City'),_('👥 Send message user'),_('◀️ Back'),]
    inline=InlineKeyboardBuilder()
    inline.add(InlineKeyboardButton(text=_('🔎Search'),switch_inline_query_current_chat=''))
    inline= inline.as_markup()
    markup=reply_button_builder(text,(3,))
    # lang = await state.get_value('locale')
    # await state.update_data({'locale': lang})
    await message.answer(text=_('Search users'),reply_markup=inline)
    await message.answer(text=_('✅ Main menu:'),reply_markup=markup)


@chat.message(F.text==__('👥 Send message user'))
async def username_handler(message:Message,state:FSMContext):
    chat1_user=message.chat.id
    markup=reply_button_builder(['◀️ Main back'],(1,))
    await state.set_state(States.chat_user)
    await state.update_data(chat1_user=chat1_user)
    await message.answer(text=_('Enter username'),reply_markup=markup)


@chat.message(States.chat_user)
async def user_check(message: Message,state:FSMContext):
    username2=message.text
    chat2_user=User.get(User.username,username2,User.user_id)
    data=await state.get_data()
    chat1_user=data.get('chat1_user')
    text=[_("❌ End Chat")]
    markup=reply_button_builder(text,(1,))
    username1=User.get(User.user_id,chat1_user,User.username,)
    if not chat2_user:
        await message.answer(_("🚫 No such user found!"))
        return
    await state.update_data(chat2_user=chat2_user,username1=username1,username2=username2)
    await state.set_state(States.send_messages)
    id_=User.get(User.username,username1,User.id)
    chats = {
        'chat_1_id': chat1_user,
        'chat_2_id': chat2_user,
        'users_id':id_
    }
    Chat.save(chats)
    await message.answer(text=_(f'{username2} started a conversation with! Write a message now:'),reply_markup=markup)


@chat.message(States.send_messages)
async def forward_messages(message: Message, state: FSMContext):
    data = await state.get_data()
    chat1_user = data.get('chat1_user')
    chat2_user = data.get('chat2_user')
    username1=data.get('username1')
    username2=data.get('username2')
    if message.text == "❌ End Chat":
        await message.answer(_("✅ End chat!"))
        await state.clear()
        return
    if message.chat.id == chat1_user:
            await bot.send_message(chat2_user, f"👥 {username1}:")
            await bot.forward_message(chat2_user, chat1_user, message.message_id)
    elif message.chat.id == chat2_user:
            await bot.send_message(chat1_user, f"👥 {username2}:")
            await bot.forward_message(chat1_user, chat2_user, message.message_id)
    messages={
        'from_chat_id':chat1_user,
        'to_chat_id':chat2_user,
        'message_id':message.message_id,
        'text':message.text
    }
    m.save(messages)


#=============================================Search========================
@chat.inline_query()
async def inline_query(inline: InlineQuery):
    query = inline.query.lower()
    result = []
    users: list =  User.get_all(User.id,User.username)
    print(users)
    for user in users:
        if query in user.username.lower():
            i = InlineQueryResultArticle(
                id=str(f'👤{user.id}'),
                title=user.username,
                input_message_content=InputTextMessageContent(message_text=str(user.id)),
            )
            result.append(i)
    await inline.answer(result, cache_time=5, is_personal=True)

@chat.message(F.via_bot)
async def any_text(message: Message):
    user_id = int(message.text)
    await message.delete()
    await message.answer(text=User.get(User.id,user_id,User.username))


