# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def choose_service_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'🔹 SMS Activate', callback_data='service:smsactivate'))
    keyboard.add(InlineKeyboardButton(text=f'🔹 OnlineSIM', callback_data='service:onlinesim'))
    keyboard.add(InlineKeyboardButton(text=f'🗑 Скрыть', callback_data='hide_msg'))
    return keyboard

def buy_online_sim_kb(info):
    keyboard = InlineKeyboardMarkup()
    if int(info[0]['count']) > 0:
        keyboard.add(InlineKeyboardButton(text=f'🇩🇪 Германия', callback_data='smsactivate:49'))
    if int(info[1]['count']) > 0:
        keyboard.add(InlineKeyboardButton(text=f'🇵🇱 Польша', callback_data='smsactivate:48'))
    if int(info[2]['count']) > 0:
        keyboard.add(InlineKeyboardButton(text=f'🇨🇿 Чехия', callback_data='smsactivate:420'))
    return keyboard