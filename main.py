# - *- coding: utf- 8 - *-
import os
import sys

import colorama
from aiogram import executor, Dispatcher
from tgbot.handlers import dp
from tgbot.utils.misc.bot_logging import bot_logger
from tgbot.middlewares import setup_middlewares
from tgbot.services.api_session import AsyncSession

colorama.init()

async def on_startup(dp: Dispatcher):
    aSession = AsyncSession()

    dp.bot['aSession'] = aSession
    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)

    bot_logger.warning("BOT WAS STARTED")
    print(colorama.Fore.LIGHTYELLOW_EX + "~~~~~ Бот запущен ~~~~~")
    print(colorama.Fore.RESET)


async def on_shutdown(dp: Dispatcher):
    aSession: AsyncSession = dp.bot['aSession']
    await aSession.close()

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()

    # if sys.platform.startswith("win"):
    #     os.system("cls")
    # else:
    #     os.system("clear")

if __name__ == "__main__":
    def start():
        try:
            setup_middlewares(dp)
            executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
        except Exception as message:
            print(message)
    start()