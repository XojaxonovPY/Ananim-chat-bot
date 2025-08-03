from aiogram import Bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import inline_button_builder
from bot.buttons.reply import reply_button_builder
from bot.states import States
from dp.model import User, Chat, Message as M
from utils.env_data import BotConfig

chat = Router()

bot = Bot(token=BotConfig.TOKEN)


@chat.message(F.text.in_([__('💬 My chat'), __('💬 Chats'), __('◀️ Back'), __('✅ Chat ended.')]))
async def chat_handler(message: Message, state: FSMContext):
    query = User.get(User.user_id, message.chat.id)
    if not query:
        markup = await reply_button_builder(['Registration'])
        await message.answer(text=_('Register first'), reply_markup=markup)
        return

    buttons = [InlineKeyboardButton(text=_('🔎 Search'), switch_inline_query_current_chat='')]
    markup_inline = await inline_button_builder(buttons)
    markup_reply = await reply_button_builder([_('🇺🇿 City'), _('👥 Send message user'), _('◀️ Main back')], (3,))

    await message.answer(text=_('Search users:'), reply_markup=markup_inline)
    await message.answer(text=_('✅ Main menu:'), reply_markup=markup_reply)


@chat.message(F.text == __('👥 Send message user'))
async def username_handler(message: Message, state: FSMContext):
    markup = await reply_button_builder([_('◀️ Main back')], (1,))
    await state.set_state(States.chat_user)
    await message.answer(text=_('✅ Enter username:'), reply_markup=markup)


@chat.message(States.chat_user)
async def user_check(message: Message, state: FSMContext):
    chat1_id = message.chat.id
    username2 = message.text.strip()

    user1: User = User.get(User.user_id, chat1_id)
    user2: User = User.get(User.name, username2)

    if not user2:
        await message.answer(_("🚫 No such user found!"))
        return

    await state.update_data(
        chat1_id=user1.user_id,
        chat2_id=user2.user_id,
        nickname1=user1.name,
        nickname2=user2.name
    )
    await state.set_state(States.send_messages)

    Chat.save(
        chat_1_id=user1.user_id,
        chat_2_id=user2.user_id,
        users_id=user1.id
    )

    markup = await reply_button_builder([_("❌ End Chat")], (1,))
    await message.answer(
        text=_("✅ Chat started! Now send your messages."),
        reply_markup=markup
    )


@chat.message(States.send_messages)
async def forward_messages(message: Message, state: FSMContext):
    data = await state.get_data()
    chat1_id = data.get('chat1_id')
    chat2_id = data.get('chat2_id')
    nickname1 = data.get('nickname1')
    nickname2 = data.get('nickname2')
    markup = await reply_button_builder([_('✅ Chat ended.')])
    if message.text == _("❌ End Chat"):
        await message.answer(text=_('✅ Conversation ended'), reply_markup=markup)
        await state.clear()
        return
    if message.chat.id == chat1_id:
        await bot.send_message(chat2_id, f"🧑‍💬 {nickname1}:\n{message.text}")
        await bot.forward_message(chat2_id, chat1_id, message.message_id)
    elif message.chat.id == chat2_id:
        await bot.send_message(chat1_id, f"🧑‍💬 {nickname2}:\n{message.text}")
        await bot.forward_message(chat1_id, chat2_id, message.message_id)
    M.save(
        from_chat_id=message.chat.id,
        to_chat_id=chat2_id if message.chat.id == chat1_id else chat1_id,
        message_id=message.message_id,
        text=message.text
    )


# =============================================Search========================
@chat.inline_query()
async def inline_query(inline: InlineQuery):
    query = inline.query.lower()
    result = []
    users: list = User.get_all()
    print(users)
    for user in users:
        if query in user.name.lower():
            i = InlineQueryResultArticle(
                id=str(f'👤{user.id}'),
                title=user.name,
                description=user.city.name,
                input_message_content=InputTextMessageContent(message_text=str(user.id)),
            )
            result.append(i)
    await inline.answer(result, cache_time=5, is_personal=True)


@chat.message(F.via_bot)
async def any_text(message: Message):
    user_id = int(message.text)
    await message.delete()
    user: User = User.get(User.id, user_id)
    await message.answer(text=user.name)
