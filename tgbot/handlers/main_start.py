# - *- coding: utf- 8 - *-
import os
import random
from captcha.image import ImageCaptcha

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from tgbot.data.loader import dp
from tgbot.keyboards.inline_all import main_menu_kb
from tgbot.keyboards.reply_all import main_menu_kb_reply
from tgbot.messages.msg import main_message
from tgbot.services.api_sqlite import get_userx, update_userx
from tgbot.data.config import get_admins


@dp.message_handler(text='/start')
async def main_start_func(message: Message, state: FSMContext):
    user_info = get_userx(id=message.from_user.id)
    await state.finish()
    if user_info['status'] == 1 or message.from_user.id in get_admins():
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=main_message(message),
            reply_markup=main_menu_kb_reply(message.from_user.id),
        )
    else:
         pass