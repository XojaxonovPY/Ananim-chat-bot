from aiogram import BaseMiddleware
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dp.model import Channel, City
from bot.buttons.inline import inline_button_builder


class CustomMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.chat.id
        channels:list = await Channel.get_all(Channel.channel_id)
        not_join_channels = []
        for channel in channels:
            response = await data.get('bot').get_chat_member(channel.channel_id , user_id)
            if not response.status in ["member", "creator" , 'admin']:
                not_join_channels.append(channel)
        if not_join_channels:
            pass
            data["not_join_channels"] = not_join_channels



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

