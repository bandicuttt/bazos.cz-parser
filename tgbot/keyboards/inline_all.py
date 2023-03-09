# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from tgbot.data.config import get_admins
from tgbot.services.api_sqlite import get_category_filters

def main_menu_kb(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'⚡️ Парсер', callback_data='parse'),
                (InlineKeyboardButton(text=f'🤖 Профиль', callback_data='profile_menu')))
    keyboard.add(InlineKeyboardButton(text=f'⚙️ Настройки', callback_data='settings'))
    if user_id in get_admins():
        keyboard.add(InlineKeyboardButton(text=f'🎛 Админ-панель', callback_data='admin_panel'))
    
    return keyboard

def search_profile_admin_kb(user_info):
    keyboard = InlineKeyboardMarkup()
    if user_info['status'] == 0:
        keyboard.add(InlineKeyboardButton(text=f'🔑 Выдать доступ', callback_data=f'give_access:{user_info["id"]}:1'))
    else:
        keyboard.add(InlineKeyboardButton(text=f'🔒 Ограничить доступ', callback_data=f'give_access:{user_info["id"]}:0'))
    return keyboard

def access_give():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'🥳 Начать', callback_data='back_to_main'))
    return keyboard

def profile_menu_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'◀️ Назад', callback_data='back_to_main'))
    return keyboard

def back_to_everywhere_kb(calldata):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'◀️ Назад', callback_data=calldata))
    return keyboard

def admin_panel_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'🔎 Поиск профиля', callback_data='admin_panel:search_profile'))
    keyboard.add(InlineKeyboardButton(text=f'➕ Загрузить токены', callback_data='admin_panel:add_new_tokens'))
    keyboard.add(InlineKeyboardButton(text=f'💳 Купить токены', callback_data='admin_panel:buy_new_tokens'))
    return keyboard

def category_filters_kb(user_id):
    data = {1: '🟢', 0: '🔴'}
    category_user_info = get_category_filters(id=user_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'Для детей {data.get(category_user_info["kids"])}', callback_data='edit_filters_category:kids'),
                (InlineKeyboardButton(text=f'Дом и сад {data.get(category_user_info["house_and_garden"])}', callback_data='edit_filters_category:house_and_garden')))
    keyboard.add(InlineKeyboardButton(text=f'Электроника {data.get(category_user_info["electro"])}', callback_data='edit_filters_category:electro'),
                (InlineKeyboardButton(text=f'Фотография {data.get(category_user_info["photo"])}', callback_data='edit_filters_category:photo')))
    keyboard.add(InlineKeyboardButton(text=f'Музыка {data.get(category_user_info["music"])}', callback_data='edit_filters_category:music'),
                (InlineKeyboardButton(text=f'Книги {data.get(category_user_info["books"])}', callback_data='edit_filters_category:books')))
    keyboard.add(InlineKeyboardButton(text=f'Телефоны {data.get(category_user_info["smartphones"])}', callback_data='edit_filters_category:smartphones'),
                (InlineKeyboardButton(text=f'Мода {data.get(category_user_info["clothes"])}', callback_data='edit_filters_category:clothes')))
    keyboard.add(InlineKeyboardButton(text= f'Компьютеры {data.get(category_user_info["pc"])}', callback_data='edit_filters_category:pc'),
                (InlineKeyboardButton(text=f'Спорт {data.get(category_user_info["sport"])}', callback_data='edit_filters_category:sport')))
    keyboard.add(InlineKeyboardButton(text=f'👁 Количество просмотров', callback_data='edit_filters:max_views'))
    keyboard.add(InlineKeyboardButton(text=f'🔢 Количество объявлений', callback_data='edit_filters:max_count'))
    
    
    return keyboard


def show_number_kb(category_name, idnumber, ads_id, url):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'🔎 Посмотреть номер', callback_data=f'show_seller_phone:{category_name}:{idnumber}:{ads_id}'))
    keyboard.add(InlineKeyboardButton(text=f'🔗 Объявление', url=url))
    return keyboard

def send_wa_kb(number, url):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'💌 Открыть WhatsApp', url=f'https://wa.me/420{number}'))
    keyboard.add(InlineKeyboardButton(text=f'🔗 Объявление', url=url))
    return keyboard


def hide_msg():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'🗑 Скрыть', callback_data='hide_msg'))
    return keyboard