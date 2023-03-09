# - *- coding: utf- 8 - *-
import math
import random
import sqlite3
import aiosqlite

from tgbot.utils.const_functions import get_unix
from tgbot.data.config import PATH_DATABASE


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


####################################################################################################
########################################### ЗАПРОСЫ К БД ###########################################
# Добавление пользователя
def add_userx(user_id, username):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO users "
                    "(id, username) "
                    "VALUES (?, ?)",
                    [user_id, username])
        con.execute("INSERT INTO filters "
                    "(id)"
                    "VALUES (?)",
                    [user_id])
        con.execute("INSERT INTO category_filters "
                    "(id)"
                    "VALUES (?)",
                    [user_id])
        con.commit()


# Добавление объявления в базу
def add_adsx(id, url):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO ads "
                    "(id, url) "
                    "VALUES (?, ?)",
                    [id, url])
        con.commit()

# Получение объявлений
def get_adsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM ads"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Обновление объявления
def update_adsx(id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE ads SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Добавление токена
def add_tokenx(token,bid,temp=0):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO tokens "
                    "(token,bid, temp) "
                    "VALUES (?,?,?)",
                    [token,bid, temp])
        con.commit()

# Получение токена
def get_tokenx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM tokens"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Обновление статуса токена
def update_tokenx(token, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE tokens SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(token)
        con.execute(sql + "WHERE token = ?", parameters)
        con.commit()

# Получение фильтров
def get_filters(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM filters"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Удаление тествого токен
def delete_temp_token():
    pass
    # with sqlite3.connect(PATH_DATABASE) as con:
    #     con.execute('DELETE FROM tokens WHERE temp = "temp"')
    #     con.commit()

# Получение фильтров категорий
def get_category_filters(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM category_filters"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()

# Обновление фильтров
def update_filtersx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE filters SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()

# Обновление фильтров категорий
def update_category_filtersx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE category_filters SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()

# Получение всех активных токенов
def get_tokensx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM tokens"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM users"
        return con.execute(sql).fetchall()


# Редактирование пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()


# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "DELETE FROM users"
        sql, parameters = update_format_args(sql, kwargs)
        con.execute(sql, parameters)
        con.commit()
