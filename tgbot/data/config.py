# - *- coding: utf- 8 - *-
import configparser

read_config = configparser.ConfigParser()
read_config.read("settings.ini")

BOT_TOKEN = read_config['settings']['token'].strip().replace(" ", "")  # Токен бота
MAX_ADS_COUNT = read_config['settings']['max_ads_count'].strip().replace(" ", "") # максимально количество обхявлений к парсингу
TOKEN_SLEEP = read_config['settings']['token_sleep'].strip().replace(" ", "") # время через которое токен снова станет активным
API_KEY = read_config['settings']['sms_activate_api_key'].strip().replace(" ", "") # токен смс активейт
API_KEY_ONLINE_SIM = read_config['settings']['online_sim_api_key'].strip().replace(" ", "") # токен смс активейт
PATH_DATABASE = "tgbot/data/database.db"  # Путь к БД
PATH_LOGS = "tgbot/data/logs.log"  # Путь к Логам
BOT_VERSION = "1.0"  # Версия бота


# Получение администраторов бота
def get_admins():
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))
    return admins