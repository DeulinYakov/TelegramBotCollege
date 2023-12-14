# Импорт работы с фото
from telebot.types import InputMediaPhoto

# Подключаем MySQLite
import sqlite3

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


def init_user_verif_func(message):
    """Функция первоначально проверяет есть ли пользователь в базе(знаем ли мы его)"""
    info_user_to = cur.execute("SELECT * FROM users WHERE id = " + str(message.chat.id)).fetchall()
    if len(info_user_to) > 0:
        return True
    else:
        return False


''' count = cur.execute("""INSERT INTO users
                          (id, nickname, droup, day, nofr)
                          VALUES
                          (?, ?, '', '', 0);""", (message.chat.id, message.from_user.username))
        conn.commit()
        conn.close()'''
# написать start_handler
