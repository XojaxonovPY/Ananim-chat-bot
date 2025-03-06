from bot.handler.main_handler import main_router
from bot.handler.registration import register
from bot.handler.city import region
from bot.handler.chats import chat
from bot.handler.chats_setting import chat_settings
from bot.dispatcher import dp
dp.include_routers(
    *[main_router,register,region,chat,chat_settings]
)