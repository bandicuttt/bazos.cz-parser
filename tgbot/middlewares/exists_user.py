# - *- coding: utf- 8 - *-
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update

from tgbot.data.config import get_admins
from tgbot.services.api_sqlite import get_userx, add_userx, update_userx


class ExistsUserMiddleware(BaseMiddleware):
    def __init__(self):
        self.prefix = "key_prefix"
        super(ExistsUserMiddleware, self).__init__()

    async def on_process_update(self, update: Update, data: dict):
        try:
            if "message" in update:
                this_user = update.message.from_user
            elif "callback_query" in update:
                this_user = update.callback_query.from_user
            else:
                this_user = None

            if this_user is not None:
                get_prefix = self.prefix

                if 1 > 0 or this_user.id in get_admins():
                    if not this_user.is_bot:
                        get_user = get_userx(id=this_user.id)
                        user_id = this_user.id
                        user_login = this_user.username

                        if user_login is None:
                            user_login = ""

                        if get_user is None:
                            add_userx(user_id, user_login.lower())
                        else:
                            if len(user_login) >= 1:
                                if user_login.lower() != get_user['username']:
                                    update_userx(get_user['id'], username=user_login.lower())
                            else:
                                update_userx(get_user['id'], username="")
        except Exception as e:
            print(e)
