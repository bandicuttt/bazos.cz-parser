# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.middlewares.exists_user import ExistsUserMiddleware


# Подключение милдварей
def setup_middlewares(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(ExistsUserMiddleware())
