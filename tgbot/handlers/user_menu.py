# - *- coding: utf- 8 - *-
import asyncio
import os
import random
import requests
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from tgbot.data.config import MAX_ADS_COUNT, TOKEN_SLEEP

from tgbot.data.loader import dp
from tgbot.keyboards.reply_all import back_to_main_reply, main_menu_kb_reply, stop_parse
from tgbot.keyboards.inline_all import back_to_everywhere_kb, category_filters_kb, hide_msg, main_menu_kb, profile_menu_kb, send_wa_kb, show_number_kb
from tgbot.messages.msg import main_message, parser_message, profile_message, settings_message
from tgbot.services.api_sqlite import add_adsx, get_adsx, get_category_filters, get_filters, get_userx, update_category_filtersx, update_filtersx, update_tokenx, update_userx
from tgbot.utils.misc.bot_filters import IsAccess, IsParse
from tgbot.utils.parser_func import check_ads_count, check_views, get_ads_list, get_headers_for_number, get_seller_link
from bs4 import BeautifulSoup

@dp.callback_query_handler(text='hide_msg', state='*')
async def delete_my_msg(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.delete()

@dp.callback_query_handler(IsAccess(),text='back_to_main', state='*')
async def back_to_main_menu_func(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=main_message(call),
        reply_markup=main_menu_kb_reply(call.from_user.id),
    )


@dp.message_handler(IsAccess(),text='🎩 Профиль', state='*')
async def profile_menu(message: Message, state: FSMContext):
    await state.finish()
    try:
        await message.bot.send_message(
            text=profile_message(message),
            chat_id=message.from_user.id,
            reply_markup=None
        )
    except Exception as e:
        print(e)


@dp.message_handler(IsAccess(), text='⚒ Настройки', state='*')
async def set_filters(message: Message, state: FSMContext):
    await state.finish()
    await message.bot.send_message(
        chat_id=message.from_user.id,
        text=settings_message(message),
        reply_markup=category_filters_kb(message.from_user.id)
    )


@dp.callback_query_handler(IsAccess(), text_startswith='edit_filters_category:', state='*')
async def edit_filters(call: CallbackQuery, state: FSMContext):
    await state.finish()
    mode = call.data.split(':')[1]

    category_user_info = get_category_filters(id=call.from_user.id)
    data = {1: 0, 0: 1}

    if mode == 'kids':
        update_category_filtersx(call.from_user.id,kids=data.get(category_user_info[mode]))
    if mode == 'house_and_garden':
        update_category_filtersx(call.from_user.id,house_and_garden=data.get(category_user_info[mode]))
    if mode == 'electro':
        update_category_filtersx(call.from_user.id,electro=data.get(category_user_info[mode]))
    if mode == 'photo':
        update_category_filtersx(call.from_user.id,photo=data.get(category_user_info[mode]))
    if mode == 'music':
        update_category_filtersx(call.from_user.id,music=data.get(category_user_info[mode]))
    if mode == 'books':
        update_category_filtersx(call.from_user.id,books=data.get(category_user_info[mode]))
    if mode == 'smartphones':
        update_category_filtersx(call.from_user.id,smartphones=data.get(category_user_info[mode]))
    if mode == 'clothes':
        update_category_filtersx(call.from_user.id,clothes=data.get(category_user_info[mode]))
    if mode == 'pc':
        update_category_filtersx(call.from_user.id,pc=data.get(category_user_info[mode]))
    if mode == 'sport':
        update_category_filtersx(call.from_user.id,sport=data.get(category_user_info[mode]))

    await call.bot.edit_message_text(
    message_id=call.message.message_id,
    chat_id=call.from_user.id,
    text=settings_message(call),
    reply_markup=category_filters_kb(call.from_user.id)
    )

@dp.callback_query_handler(IsAccess(), text_startswith='edit_filters:',state='*')
async def edit_filters(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as proxy:
        mode = call.data.split(':')[1]

        if mode == 'max_views':
            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Введите новый аргумент для фильтра "Максимальное число просмотров":</b>',
                reply_markup=hide_msg()
            )
            await state.set_state('set_new_max_views')
        if mode == 'max_count':
            proxy['msg']=await call.bot.send_message(
                chat_id=call.from_user.id,
                text='<b>✍️ | Введите новый аргумент для фильтра "Максимальное число объявлений":</b>',
                reply_markup=hide_msg()
            )
            await state.set_state('set_new_max_count')


@dp.message_handler(IsAccess(),state='set_new_max_count')
async def set_max_count(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await message.delete()
        try:
            if int(message.text) < 100000 and int(message.text) > 0:
                await state.finish()
                
                update_filtersx(message.from_user.id, max_count=message.text)
                await message.bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=proxy['msg'].message_id,
                    text='<b>🎉 | Данные успешно обновлены!</b>',
                    reply_markup=hide_msg()
                )
                await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text=settings_message(message),
                    reply_markup=category_filters_kb(message.from_user.id)
                )
            else:
                await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>❌ | Возникла ошибка!\nВведенный текст не может быть больше 100,000 или меньше 1.\nПопробуйте ещё раз!</b>',
                reply_markup=hide_msg()
            )   
        except Exception as e:
            await message.bot.send_message(
                chat_id=message.from_user.id,
                text='<b>❌ | Возникла ошибка!\nВведенный текст не является цифрой.\nПопробуйте ещё раз!</b>',
                reply_markup=hide_msg()
            )

@dp.message_handler(IsAccess(),state='set_new_max_views')
async def set_max_count(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            await message.delete()
            if int(message.text) < 100000 and int(message.text) > 0:
                await state.finish()

                update_filtersx(message.from_user.id, max_views=message.text)
                await message.bot.edit_message_text(
                    chat_id=message.from_user.id,
                    message_id=proxy['msg'].message_id,
                    text='<b>🎉 | Данные успешно обновлены!</b>',
                    reply_markup=hide_msg()
                )
                await message.bot.send_message(
                    chat_id=message.from_user.id,
                    text=settings_message(message),
                    reply_markup=category_filters_kb(message.from_user.id)
                )
            else:
                proxy['msg']=await message.bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=proxy['msg'].message_id,
                text='<b>❌ | Возникла ошибка!\nВведенный текст не может быть больше 100,000 или меньше 1.\nПопробуйте ещё раз!</b>',
                reply_markup=hide_msg()
            )
        except Exception as e:
            print(e)
            proxy['msg']=await message.bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=proxy['msg'].message_id,
                text='<b>❌ | Возникла ошибка!\nВведенный текст не является цифрой.\nПопробуйте ещё раз!</b>',
                reply_markup=hide_msg()
            )

@dp.message_handler(text='❌ Остановить парсинг', state='*')
async def stop_parse_func(message: Message, state: FSMContext):
    await message.delete()
    update_userx(message.from_user.id, parse_status=0)
    msg=await message.answer(
        text='🎉 Парсинг успешно остановлен!',
        reply_markup=ReplyKeyboardRemove()
    )
    await msg.delete()


@dp.message_handler(IsAccess(),IsParse(),text='🔎 Поиск объявлений 🔍',state='*')
async def get_count(message: Message, state: FSMContext):
    try:
        async with state.proxy() as proxy:
            await state.finish()

            category_filters = get_category_filters(id=message.from_user.id)
            active_categories = [cat for cat in category_filters if category_filters[cat] == 1]
            if str(active_categories) != '[]':
                proxy['msg']=await message.bot.send_message(
                    chat_id=message.from_user.id,
                    reply_markup=hide_msg(),
                    text='<b>✍️ | Введите число объявлений к парсингу</b>'
                )
                await state.set_state('get_ads_count')
            else:
                await message.answer('😔 К сожалению вы не выбрали ни одной категории!')
    except Exception as e:
        print(e)

@dp.callback_query_handler(IsAccess(),text_startswith='show_seller_phone:', state='*')
async def show_num(call: CallbackQuery, state: FSMContext):
    try:
        category_name = call.data.split(':')[1]
        idnumber = call.data.split(':')[2]
        ads_id = call.data.split(':')[3]
        url = get_adsx(id=ads_id)['url']
        await asyncio.sleep(0.1)
        number = await get_seller_number(category_name, idnumber, ads_id)
        caption = await edit_caption(str((call.message.caption)),number)
        # if number == None:
        #     await call.bot.edit_message_caption(
        #     message_id=call.message.message_id,
        #     chat_id=call.from_user.id,
        #     reply_markup=send_wa_kb(number,url),
        #     caption=caption
        #     )
        # else:
        #     await call.answer('😔 Закончились токены, попробуйте позже')
        if number:
            await call.bot.edit_message_caption(
            message_id=call.message.message_id,
            chat_id=call.from_user.id,
            reply_markup=send_wa_kb(number,url),
            caption=caption
            )
        else:
            await call.bot.send_message(
                chat_id=call.from_user.id,
                text='😔 Закончились токены, попробуйте позже',
                reply_markup=hide_msg()
            )
            await call.answer('😔 Закончились токены, попробуйте позже')
    except Exception as e:
        print(e)

@dp.message_handler(state='get_ads_count')
async def start_parsing(message: Message, state: FSMContext):
    async with state.proxy() as proxy:
        await proxy['msg'].delete()
        await message.delete()
        try:
            if int(message.text) < int(MAX_ADS_COUNT) and int(message.text) > 0:
                await state.finish()
                update_userx(message.from_user.id, parse_status=1)
                start_parse=await message.answer(
                    reply_markup=stop_parse(),
                    text='<b>⏱ Начинаю парсинг...</b>'
                )
                await main(int(message.text),message.from_user.id,message)
                proxy['msg']=await message.bot.send_message(
                    chat_id=message.from_user.id,
                    reply_markup=main_menu_kb_reply(message.from_user.id),
                    text='<b>🎉 | Парсинг окончен!</b>'
                )
                update_userx(message.from_user.id, parse_status=0)
            else:
                proxy['msg']=await message.bot.send_message(
                    message_id=proxy['msg'].message_id,
                    chat_id=message.from_user.id,
                    reply_markup=hide_msg(),
                    text=f'<b>❌ | Ошибка, введенное значение не может быть меньше 0 или больше {MAX_ADS_COUNT}! Попробуйте ещё раз</b>'
                )
        except Exception as e:
            print(e)
            proxy['msg']=await message.bot.send_message(
                chat_id=message.from_user.id,
                reply_markup=hide_msg(),
                text='<b>❌ | Ошибка, введенное значение не является числом! Попробуйте ещё раз</b>'
            )

async def edit_caption(caption,number):
    caption = caption.replace('📞 Телефон: Скрыт',f'<b>📞 Телефон:</b> <code>+420{number}</code>').replace('🔷 Объявление','<b>🔷 Объявление</b>') \
        .replace('🏷 Название', '<b>🏷 Название</b>').replace('💸 Цена:','<b>💸 Цена:</b>').replace('📅 Дата создания:','<b>📅 Дата создания:</b>') \
            .replace('🔝 ТОП: ','<b>🔝 ТОП: </b>').replace('👁 Просмотры:','<b>👁 Просмотры:</b>').replace('📊 Объявления продавца:','<b>📊 Объявления продавца:</b>')
    ads_name = ((caption.split('🏷 Название</b>: ')[1]).split('<b>📞 Телефон:')[0]).replace('\n','')
    caption = caption.replace(f'<b>🏷 Название</b>: {ads_name}', f'<b>🏷 Название</b>: <code>{ads_name}</code>')
    return caption


async def token_sleep_func(token):
    await asyncio.sleep(int(TOKEN_SLEEP))
    update_tokenx(token,active=1)

async def get_seller_number(category_name, idnumber, ads_id):
    while True:
            link, headers, token = get_headers_for_number(category_name)
            if link:
                params = {
                    'idi': ads_id,
                    'idphone': idnumber
                }
                try:
                    html_data = requests.get(url=link, headers=headers, params=params).text
                    soup = BeautifulSoup(html_data, 'lxml')
                    number = soup.find('a',href=True).get_text()
                    if number != 'max tel, zkuste za chvíli':
                        return number 
                    update_tokenx(token,active=0)
                    asyncio.create_task(token_sleep_func(token))
                except Exception as e:
                    update_tokenx(token,active=0)
                    asyncio.create_task(token_sleep_func(token))
            else:
                return None

async def main(ads_count, user_id, message):
    try:
        page = -20
        ads_give = 0
        fitlers_train = 0
        parse_status = get_userx(id=user_id)['parse_status']
        while ads_give < ads_count and parse_status==1:
            page +=20
            ads_list,category_name = await get_ads_list(page, user_id)
            await asyncio.sleep(0.1)
            for ads in ads_list:
                parse_status = get_userx(id=user_id)['parse_status']
                while ads_give < ads_count and parse_status==1:
                    is_ads_uniq = get_adsx(id=ads['ads_id'])
                    if is_ads_uniq:
                        break
                    else:
                        user_filters = get_filters(id=user_id)
                        if check_views(user_filters['max_views'],ads['views']):
                            seller_ads_count,idphone = await get_seller_link(ads['url'], category_name, ads['ads_id'])
                            await asyncio.sleep(0.1)
                            ads['seller_ads_count'] = seller_ads_count
                            if check_ads_count(user_filters['max_count'], seller_ads_count):
                                ads_give+=1
                                fitlers_train=0
                                photo_path = f'tgbot/files/{random.randint(1,200000)}.jpg'
                                ads_name = ads['ads_name']
                                price = ads['price']
                                date = ads['date']
                                top = ads['top']
                                views = ads['views']
                                seller_count = ads['seller_ads_count']
                                url = ads['url']
                                add_adsx(id=ads['ads_id'], url=ads['url'])
                                print('спарсил')
                                with open(photo_path, 'wb') as out:
                                    out.write(requests.get(ads['photo']).content)
                                with open(photo_path, 'rb') as photo:
                                    await message.bot.send_photo(
                                        chat_id = user_id,
                                        caption=parser_message(ads_name,price,date,top,views,seller_count,url),
                                        photo=photo,
                                        reply_markup=show_number_kb(category_name,idphone,ads['ads_id'],ads['url']),
                                    )
                                os.remove(photo_path)
                                
                            else:
                                fitlers_train+=1
                                if fitlers_train == 1000:
                                    await message.bot.send_message(
                                        chat_id = user_id,
                                        hide_msg=hide_msg(),
                                        text = '⚠️ Бот пропустил более 1000 объявлений, но ни одно не прошло проверку фильтров. Возможно Вам стоит изменить настройки фильтров'
                                    )
                                # print('фильтр')
                                break
                        else:
                            fitlers_train+=1
                            if fitlers_train == 1000:
                                    await message.bot.send_message(
                                        chat_id = user_id,
                                        text = '⚠️ Бот пропустил более 1000 объявлений, но ни одно не прошло проверку фильтров. Возможно Вам стоит изменить настройки фильтров',
                                        reply_markup=hide_msg()
                                    )
                            # print('фильтр')
                            break
    except Exception as e:
        print(e)