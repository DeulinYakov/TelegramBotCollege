# /////////////////////////////////////////////////////////////////////////////////////////////////////
#                                    МОДУЛЬ ОСНОВНЫХ ФУНКЦИЙ
# /////////////////////////////////////////////////////////////////////////////////////////////////////

# Импорт работы с фото
from telebot.types import InputMediaPhoto

# Подключаем MySQLite
import sqlite3

import sets

"""База данных"""
# Подключение к базе данных 'dbase.db', если её нет она создастся автоматически
conn = sqlite3.connect('base.db', check_same_thread=False)
# Создаём курсор
cur = conn.cursor()
print("Подключен к SQLite")
# cur.execute('''CREATE TABLE users (id TEXT, nickname TEXT, droup TEXT, day TEXT, nofr INTEGER)''')
# id = message.chat.id
# nickname = ник в тг
# grop = группа
# day = день
# nofr = кол-во обращений

# cur.close()
# print('////base close////')

edge = 'BT'
edgeNum = 51.0


def start_handler(message, bot, keyboard):
    """Функция добавляет юзера в базу и предлагает выбрать группу"""
    cur.execute("""INSERT INTO users
                          (id, nickname, droup, day, nofr)
                          VALUES
                          (?, ?, '', '', 0);""", (message.chat.id, message.from_user.username))
    conn.commit()
    # отправим пользователю следующее сообщение
    msg = bot.send_message(message.chat.id,
                           'Я новый крутой привет Выберите интересующее направление',
                           reply_markup=keyboard)


def sending_message(message, bot, text, keyboard):
    """Эта функцию отправит пользователю сообщение"""
    # Отправим сообщение пользователю и добавим нужную клавиатуру
    msg = bot.send_message(message.chat.id, text, reply_markup=keyboard)


def group_handler(message, bot, keyboard):
    """Обработчки групп"""
    # закинем инфу о группе в базу
    cur.execute('UPDATE users SET  droup = ? WHERE id = ?', (message.text, message.chat.id))
    conn.commit()
    # отправим пользователю следующее сообщение
    msg = bot.send_message(message.chat.id,
                           'Выберите день недели',
                           reply_markup=keyboard)


def day_handler(message, bot, file_path, keyboard):
    """Обработчки дней недели"""
    # закинем инфу о группе в базу
    cur.execute('UPDATE users SET  day = ? WHERE id = ?', (message.text, message.chat.id))
    conn.commit()
    # Проверяем день недели, если понедельник показываем больше строк
    if message.text == sets.mon:
        pass
    else:
        pass
