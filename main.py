import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.handler import *
from bot.handler.main_handler import CustomMiddleware
from utils.env_data import BotConfig

TOKEN = BotConfig.TOKEN


# engine = create_engine("postgresql+psycopg2://postgres:1@db:5432/postgres")

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Starting bot."),
        BotCommand(command="/delete", description="Delete user"),
        BotCommand(command="/my_own", description="About user")
    ]
    await bot.set_my_commands(commands=commands)


async def main() -> None:
    i18n = I18n(path='locales', default_locale='en', domain='messages')
    dp.update.middleware(FSMI18nMiddleware(i18n))
    dp.message.outer_middleware(CustomMiddleware())
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    # metadata.create_all(engine)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
