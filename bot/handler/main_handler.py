from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from bot.buttons.reply import reply_button_builder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from bot.states import States

main_router=Router()


@main_router.message(F.text==__('◀️ Back'))
@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text=[_('Registration'),_('🇷🇺 🇺🇿 🇬🇧 Language'),_('💬 My chat')]
    markup=reply_button_builder(text,(2,))
    await message.answer(_('Welcome chat bot'),reply_markup=markup)


@main_router.message(F.text == __('🇷🇺 🇺🇿 🇬🇧 Language'))
async def language_user(message: Message, state: FSMContext):
    text = ['🇺🇿 Uzbek', '🇷🇺 Russian', '🇬🇧 English', _('◀️ Back')]
    markup = reply_button_builder(text, (3, 1))
    await state.set_state(States.language)
    await message.answer(text=_('Chose language:'), reply_markup=markup)


@main_router.message(States.language)
async def language_handler(message: Message, state: FSMContext, i18n):
    map_lang = {
        '🇺🇿 Uzbek': 'uz',
        '🇷🇺 Russian': 'rus',
        '🇬🇧 English': 'en'
    }
    code = map_lang.get(message.text)
    i18n.current_locale = code
    await state.update_data(locale=code)
    if not code:
        await message.answer(_('❌ Iltimos, menyudan tilni tanlang!'))
        return
    lang = await state.get_value('locale')
    await state.clear()
    await state.update_data({'locale': lang})
    await state.update_data(locale=code)
    text = [_('Registration'), _('🇷🇺 🇺🇿 🇬🇧 Language'), _('💬 My chat')]
    markup = reply_button_builder(text, (2,))
    await message.answer(_('Welcome chat bot'), reply_markup=markup)

