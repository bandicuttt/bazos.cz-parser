from tgbot.services.api_sqlite import get_filters


def main_message(message):
    return(
 f'''
 <b>
💠 Добро пожаловать, @{message.from_user.username}
➖➖➖➖➖➖➖➖➖➖➖➖
<i>Мы всегда рады Вам</i>
 </b>
 '''       
    )


def profile_message(message):
    return(
f'''
<b>🧳 Профиль пользователя</b>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>🆔 ID Пользователя:</b> <code>{message.from_user.id}</code>
<b>🏷 Юзернейм Пользователя: @{message.from_user.username}</b>
<b>🔐 Доступ:</b> <code>Активный</code>

<i>Приятного пользования</i>
'''
    )

def settings_message(message):
    filters_info = get_filters(id=message.from_user.id)
    return(
f'''
<b>⚙️ Настройки фильтров</b>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>👁 Количество просмотров: </b><code>{filters_info['max_views']}</code>
<b>🔢 Количество объявлений: </b><code>{filters_info['max_count']}</code>
'''

    )

def profile_search_message(user_info):
    data = {1:'Активный',0:'Отсутствует'}

    return(
f'''
<b>🧳 Профиль пользователя</b>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>🆔 ID Пользователя:</b> <code>{user_info['id']}</code>
<b>🏷 Юзернейм Пользователя: @{user_info['username']}</b>
<b>🔐 Доступ:</b> <code>{data.get(user_info['status'])}</code>

<i>Приятного пользования</i>
'''
    )


def parser_message(ads_name,price,date,top,views,seller_count,url):
    data = {True: '✅', False: '❌'}
    return(
f'''
<b>🏷 Название:</b> <code>{ads_name}</code>
<b>📞 Телефон:</b> Скрыт
<b>💸 Цена:</b> {price} Kč
<b>📅 Дата создания:</b> {date}
<b>🔝 ТОП: {data.get(top)}</b>
<b>👁 Просмотры:</b> {views}
<b>📊 Объявления продавца:</b> {seller_count}
'''
    )

def online_sim_msg(balance,info):
    return(
    f'''
<b>✍️ | Выберите страну.</b>
<b>💰 Баланс:</b> <code>{balance}</code>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>🇩🇪 Германия</b>
<b>🔄 Количество доступных токенов: {info[0]['count']}</b>
<b>💴 Цена за 1 токен: {info[0]['price']}</b>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>🇵🇱 Польша</b>
<b>🔄 Количество доступных токенов: {info[1]['count']}</b>
<b>💴 Цена за 1 токен: {info[1]['price']}</b>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>🇨🇿 Чехия</b>
<b>🔄 Количество доступных токенов: {info[2]['count']}</b>
<b>💴 Цена за 1 токен: {info[2]['price']}</b>
➖➖➖➖➖➖➖➖➖➖➖➖
    '''
    )