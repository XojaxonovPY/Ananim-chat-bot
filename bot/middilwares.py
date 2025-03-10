from aiogram import BaseMiddleware
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dp.model import Channel, City
from bot.buttons.inline import inline_button_builder



class CustomMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.chat.id
        channels: list = await Channel.get_all(Channel.channel_id,Channel.link)

        # Obuna bo‘lmagan kanallarni topish
        not_join_channels = [
            channel for channel in channels
            if (await data.get('bot').get_chat_member(channel.chat_id, user_id)).status
               not in ["member", "creator", "admin"]
        ]
        if not not_join_channels:
            return await handler(event, data)
        markup = await inline_button_builder(not_join_channels,(1,))
        await data.get('bot').send_message(
            user_id, "Quyidagi kanallarga obuna bo‘ling:", reply_markup=markup
        )


def users_format(city: str, page: int = 1):
    users = City.get_users_by_city(city)
    if not users:
        return []
    users = users[10 * (page - 1): 10 * page]
    return users
def is_str(cols):
    res=' '.join(i for i in cols)
    return res

cities = City.get_all(City.name)
uzbekiston_viloyatlari = [city.name for city in cities]

