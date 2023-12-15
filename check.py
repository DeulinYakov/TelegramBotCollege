# /////////////////////////////////////////////////////////////////////////////////////////////////////
#                                        МОДУЛЬ ПРОВЕРКИ
# /////////////////////////////////////////////////////////////////////////////////////////////////////

import sqlite3
import handlers as hn


def init_user_verif_func(message):
    """Функция первоначально проверяет есть ли пользователь в базе(знаем ли мы его)"""
    info_user_to = hn.cur.execute("SELECT * FROM users WHERE id = " + str(message.chat.id)).fetchall()
    if len(info_user_to) > 0:
        return True
    else:
        return False


def check_user_group(message):
    """Функция проверяет есть ли группа у пользователя"""
    info_user_to = hn.cur.execute("SELECT * FROM users WHERE droup = " + str(message.chat.id)).fetchall()
    if len(info_user_to) > 0:
        return True
    else:
        return False
