# - *- coding: utf- 8 - *-
import asyncio
import requests
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from random import randint
import os
from bs4 import BeautifulSoup
from create_new_tokens import get_balance_online_sim, get_statistics_online_sim, send_num
from smsactivate.api import SMSActivateAPI

from tgbot.data.config import get_admins
from tgbot.data.config import PATH_LOGS, PATH_DATABASE
from tgbot.data.loader import dp
from tgbot.keyboards.inline_admin import buy_online_sim_kb, choose_service_kb
from tgbot.keyboards.inline_all import access_give, admin_panel_kb, back_to_everywhere_kb, hide_msg, search_profile_admin_kb
from tgbot.messages.msg import online_sim_msg, profile_search_message
from tgbot.services.api_sqlite import add_tokenx, get_userx, update_userx
from tgbot.utils.misc.bot_filters import IsAdmin
from tgbot.utils.parser_func import check_token, check_token_with_get_num, get_headers_for_number
from tgbot.data.config import API_KEY

sa = SMSActivateAPI(API_KEY)
sa.debug_mode = False

@dp.message_handler(IsAdmin(),text='🎛 Админ Панель', state='*')
async def admin_panel_menu(message: Message, state: FSMContext):
    await state.finish()
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text='<b>🎛 Админ Панель</b>',
        reply_markup=admin_panel_kb()
    )


@dp.callback_query_handler(IsAdmin(), text_startswith='admin_panel:', state='*')
async def admin_functions(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()
        mode = call.data.split(':')[1]
        if mode == 'search_profile':
            proxy['msg']=await call.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text='<b>✍️ | Введите ID или @юзернейм пользователя: </b>',
                reply_markup=hide_msg()
            )
            await state.set_state('search_profile')
        if mode == 'add_new_tokens':
            proxy['msg']=await call.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text='<b>✍️ | Введите токены которые хотите добавить.</b>\n<i>Можно добавить сразу несколько токенов. Вводите каждый токен с новой строки</i>\n<b>Пример:</b>\n<b>TOKEN 1\nTOKEN 2\nTOKEN 3</b>',
                reply_markup=hide_msg()
            )
            await state.set_state('add_tokens')
        if mode == 'buy_new_tokens':
            await state.finish()
            await call.bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                text='<b>💠 Выберите сервис</b>',
                reply_markup=choose_service_kb()
            )

@dp.callback_query_handler(text_startswith='service:')
async def choose_service(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        await state.finish()
        service = call.data.split(':')[1]
        if service == 'smsactivate':
            while True:
                    try:
                        balance = sa.getBalance()
                        balance = balance['balance']
                        break
                    except Exception as e:
                        await asyncio.sleep(0.1)
                        print(e)
            while True:
                try:
                    prices = sa.getPrices(service='cb', country=63)
                    print(prices)
                    price = prices['63']['cb']['cost']
                    count = prices['63']['cb']['count']
                    break
                except Exception as e:
                    await asyncio.sleep(0.1)
                    print(prices['message'])
            proxy['price'] = price
            proxy['count'] = count
            proxy['balance'] = balance
            proxy['msg']=await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f'<b>✍️ | Введите желаемое количество токенов к покупке.</b>\n<b>💰 Баланс:</b> <code>{balance}</code>\n<b>💴 Цена за 1 токен:</b> <code>{price}</code>\n<b>🔄 Количество доступных номеров:</b> <code>{count}</code>',
            reply_markup=hide_msg()
            )
            await state.set_state('buy_tokens')
        else:
            print('тут')
            try:
                while True:
                    try:
                        balance = await get_balance_online_sim()
                        break
                    except Exception as e:
                        await asyncio.sleep(0.1)
                while True:
                    try:
                        info = await get_statistics_online_sim()
                        break
                    except Exception as e:
                        await asyncio.sleep(0.1)
                proxy['msg']=await call.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=online_sim_msg(balance,info),
                reply_markup=buy_online_sim_kb(info)
                )
            except Exception as e:
                print(e)

@dp.callback_query_handler(text_startswith='smsactivate:',state='*')
async def how_many_number_func(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            await state.finish()
            await call.bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.from_user.id,
                reply_markup=hide_msg(),
                text=f'<b>✍️ | Введите желаемое количество токенов к покупке.</b>',
            )
            proxy['country_code']=call.data.split(':')[1]
            await state.set_state('buy_tokens')
        except Exception as e:
            print(e)

@dp.message_handler(state='buy_tokens')
async def buy_tokens(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            await message.delete()
            country_code = None
            try:
                country_code = proxy['country_code']
            except Exception:
                pass
            if country_code is not None:
                try:
                    for i in range(0,int(message.text)):
                        await message.bot.send_message(
                            chat_id=message.from_user.id,
                            text='<b>🕔 Начинаю покупку</b>'
                        ) 
                        token = await send_num(48)
                        await message.bot.send_message(
                            chat_id=message.from_user.id,
                            text='<b>⚠️ Куплен новый токен {}</b>'.format(token)
                        ) 
                except Exception as e:
                    print(e)
            else:
                try:
                    if int(message.text) > 0 and int(message.text) < int(proxy['count']):
                        if float(proxy['balance']) > (int(proxy['price'])*int(message.text)):
                            await state.finish()
                            for i in range(0,int(message.text)):
                                token = await send_num()
                                await message.bot.send_message(
                                    chat_id=message.from_user.id,
                                    text='<b>⚠️ Куплен новый токен {}</b>'.format(token)
                                )
                        else:
                            proxy['msg']=await message.bot.send_message(
                            message_id=proxy['msg'].message_id,
                            chat_id=message.from_user.id,
                            reply_markup=hide_msg(),
                            text=f'<b>❌ | Ошибка, введенное значение не может быть больше баланса! Попробуйте ещё раз</b>'
                        )
                    else:
                        proxy['msg']=await message.bot.send_message(
                            message_id=proxy['msg'].message_id,
                            chat_id=message.from_user.id,
                            reply_markup=hide_msg(),
                            text=f'<b>❌ | Ошибка, введенное значение не может быть меньше 0 или больше 100! Попробуйте ещё раз</b>'
                        )
                except Exception as e:
                    print(e)
                    proxy['msg']=await message.bot.send_message(
                        chat_id=message.from_user.id,
                        reply_markup=hide_msg(),
                        text='<b>❌ | Ошибка, введенное значение не является числом! Попробуйте ещё раз</b>'
                    )
    except Exception as e:
        print(e)


@dp.message_handler(state='add_tokens')
async def add_token(message: Message, state: FSMContext):
    try:
        await message.delete()
        async with state.proxy() as proxy:
            await state.finish()
            tokens = message.text.split('\n')
            good,bad = await check_token_with_get_num(tokens)
            
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=proxy['msg'].message_id,
            reply_markup=hide_msg(),
            text=f'<b>🎉 Я проверил токены и загрузил те, которые прошли проверку\n✅ Прошли проверку {good}шт.\n❌ Не прошли проверку {bad}шт</b>'
        )
    except Exception as e:
        print(e)

        
    


@dp.message_handler(IsAdmin(), state='search_profile')
async def search_profile_func(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await message.delete()
        if '@' in message.text:
            user_info = get_userx(username=message.text.split('@')[1].lower())
        else:
            user_info = get_userx(id=message.text)
        if user_info:
            await state.finish()
            await message.bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=proxy['msg'].message_id,
                reply_markup=search_profile_admin_kb(user_info),
                text=profile_search_message(user_info)
            )
        else:
            proxy['msg']=await message.bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=proxy['msg'].message_id,
                text='<b>😔 Пользователь не найден!</b>\n <i>Вомзожно вы неправильно ввели ID пользователя или пользователь ни разу не запускал бота.</i>\nПопробуйте ещё раз!',
                reply_markup=hide_msg()
            )


@dp.callback_query_handler(IsAdmin(), text_startswith='give_access:', state='*')
async def edit_user_access(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.data.split(':')[1]
    user_status = call.data.split(':')[2]
    if user_status == '1':
        await call.answer('🎉 | Пользователю успешно выданы права на использование бота', show_alert=False)
        update_userx(user_id,status=1)
        await call.bot.send_message(
            chat_id=user_id,
            text='<b>🎉 | Поздравляем! Вам был выдан доступ!</b>',
            reply_markup=access_give()
        )
    else:
        await call.bot.send_message(
            chat_id=user_id,
            text='<b>😔 | Сожалеем! Вам был закрыт доступ!</b>',
            reply_markup=None
        )
        await call.answer('🎉 | Пользователь больше не сможет использовать бота', show_alert=False)
        update_userx(user_id,status=0)

    user_info = get_userx(id=user_id)
    await call.message.delete()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        reply_markup=search_profile_admin_kb(user_info),
        text=profile_search_message(user_info)
    )

    