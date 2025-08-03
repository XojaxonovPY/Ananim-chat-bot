from aiogram import F, BaseMiddleware
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram import Router

from bot.buttons.inline import inline_button_builder
from bot.buttons.reply import reply_button_builder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from bot.states import States
from dp.model import Channel

main_router = Router()


@main_router.message(F.text == __('◀️ Main back'))
@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = [_('📋 Registration'), _('🇷🇺 🇺🇿 🇬🇧 Language'), _('💬 My chat')]
    markup = await reply_button_builder(text, (2,))
    await message.answer(_('✅ Welcome chat bot'), reply_markup=markup)


@main_router.message(F.text == __('🇷🇺 🇺🇿 🇬🇧 Language'))
async def language_user(message: Message, state: FSMContext):
    text = ['🇺🇿 Uzbek', '🇷🇺 Russian', '🇬🇧 English', _('◀️ Back')]
    markup = await reply_button_builder(text, (3, 1))
    await state.set_state(States.language)
    await message.answer(text=_('✅ Chose language:'), reply_markup=markup)


@main_router.message(States.language)
async def language_handler(message: Message, state: FSMContext, i18n):
    map_lang = {
        '🇺🇿 Uzbek': 'uz',
        '🇷🇺 Russian': 'ru',
        '🇬🇧 English': 'en'
    }
    code = map_lang.get(message.text)
    i18n.current_locale = code
    await state.update_data(locale=code)
    lang = await state.get_value('locale')
    await state.clear()
    await state.update_data({'locale': lang})
    await state.update_data(locale=code)
    text = [_('📋 Registration'), _('🇷🇺 🇺🇿 🇬🇧 Language'), _('💬 My chat')]
    markup = await reply_button_builder(text, (2,))
    await message.answer(_('✅ Welcome chat bot'), reply_markup=markup)


# ==============================================subscribe_chanells=============
class CustomMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.chat.id
        channels: list[Channel] = Channel.get_all()
        not_join_channels = []
        if channels:
            for channel in channels:
                response = await data.get('bot').get_chat_member(channel.channel_id, user_id)
                if not response.status in ["member", "creator", 'admin']:
                    not_join_channels.append(channel)
        if not_join_channels:
            buttons = [InlineKeyboardButton(text=channel.name, url=channel.link) for channel in not_join_channels]
            markup = await inline_button_builder(buttons)
            await data.get('bot').send_message(user_id, _("✅ Quydagi kannalarga obuna bo'l"), reply_markup=markup)
        else:
            return await handler(event, data)
