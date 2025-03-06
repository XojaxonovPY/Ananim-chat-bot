from aiogram import BaseMiddleware
from aiogram.types import Message
from dp.model import Channel, City


class CustomMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.chat.id
        channels:list = await Channel.get_all(Channel.channel_id)
        not_join_channels = []
        for channel in channels:
            response = await data.get('bot').get_chat_member(channel.channel_id , user_id)
            if not response.status in ["member", "creator" , 'admin']:
                not_join_channels.append(channel)
        data["not_join_channels"] = not_join_channels
        return await handler(event, data)


def users_format(city: str, page: int = 1):
    users = City.get_users_by_city(city)
    if not users:
        return []
    users = users[10 * (page - 1): 10 * page]
    return users


def is_number(text:str):
    res=0
    for i in text:
        if i.isdigit():
            res=i
    return res



uzbekistan_viloyatlari = [
    "1) Toshkent shahar",
    "2) Buxoro viloyati",
    "3) Andijon viloyati",
    "4) Farg‘ona viloyati",
    "5) Jizzax viloyati",
    "6) Xorazm viloyati",
    "7) Navoiy viloyati",
    "8) Namangan viloyati",
    "9) Samarqand viloyati",
    "10) Sirdaryo viloyati",
    "11) Surxondaryo viloyati",
    "12) Toshkent viloyati",
    "13) Qashqadaryo viloyati",
    "14) Qoraqalpog‘iston Respublikasi"
]


uzbekistan_viloyatlari2 = [
        "Toshkent shahar",
        "Buxoro viloyati",
        "Andijon viloyati",
        "Farg‘ona viloyati",
        "Jizzax viloyati",
        "Xorazm viloyati",
        "Navoiy viloyati",
        "Namangan viloyati",
        "Samarqand viloyati",
        "Sirdaryo viloyati",
        "Surxondaryo viloyati",
        "Toshkent viloyati",
        "Qashqadaryo viloyati",
        "Qoraqalpog‘iston Respublikasi"
    ]

