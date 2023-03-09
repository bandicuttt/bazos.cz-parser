# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from tgbot.keyboards.inline_all import hide_msg, main_menu_kb
from tgbot.messages.msg import main_message

from tgbot.services.api_sqlite import get_userx
from tgbot.data.config import get_admins
from tgbot.data.loader import dp, bot


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in get_admins():
            return True
        else:
            return False

# Проверка на админа
class IsAccess(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_info = get_userx(id=call.from_user.id)
        if user_info['status'] == 1 or user_info['id'] in get_admins():
            return True
        else:
            return False

# Проверка на активность парсер статуса
class IsParse(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        user_info = get_userx(id=call.from_user.id)
        if user_info['parse_status'] == 0:
            return True
        else:
            await call.answer('😔 У вас уже запущен парсинг!',show_alert='False')
            return False