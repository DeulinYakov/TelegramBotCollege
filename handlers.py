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

edge = 'BP'
edgeNum = 50.0


def start_handler(message, bot, keyboard):
    """Функция добавляет юзера в базу и предлагает выбрать группу"""
    cur.execute("""INSERT INTO users
                          (id, nickname, droup, day, nofr)
                          VALUES
                          (?, ?, '', '', 0);""", (message.chat.id, message.from_user.username))
    conn.commit()
    # отправим пользователю следующее сообщение
    msg = bot.send_message(message.chat.id,
                           f'Приветствую!\nЯ обновленный Принтюша 2.0!🥳\n'
                           'Теперь я стал гораздо более удобным и быстрым. \n'
                           'Мои обновления позволяют мне показывать расписание без задержек и запоминать вас!🤯\n'
                           'На данный момент я нахожусь в тестовом режиме, полная версия выйдет после нового года\n'
                           'Просто напомните мне, из какой вы группы, чтобы начать.\n'
                           'Не переживайте, группу можно будет сменить в любой момент, в разделе "Сменить группу"😊',
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
                           'Выберите день или раздел, который вас интересует.😉\n',
                           reply_markup=keyboard)


def day_handler(message, bot):
    """Обработчки дней недели"""
    # закинем инфу о группе в базу
    cur.execute('UPDATE users SET  day = ? WHERE id = ?', (message.text, message.chat.id))
    conn.commit()


def get_schedule_handler(message, bot, file_path):
    """Функция возвращает готовое расписание для бота"""
    global otvet
    import pandas as pd

    data = pd.read_html(file_path, encoding='utf-8', header=0, index_col=0)[0].fillna('нет')
    # отправим пользователю следующее сообщение
    msg = bot.send_message(message.chat.id, 'Вспоминаю расписание, это может занять несколько секунд🤔')

    def first_processing(data):
        """Функция первичной обработки файла с расписанием"""
        # удаляем промежутчную ненужную строку
        data = data.drop("Unnamed: 2", axis=1)
        # удаляем первые 3 ненужные строки
        data = data.drop([1.0, 2.0, 3.0, 4.0])
        # удаляем посдедние ненужные столбцы после столбца BI
        all_colums = list(data.columns.values)
        last_index = all_colums.index(edge)
        bad_colums = all_colums[last_index + 1:]
        data = data.drop(bad_colums, axis=1)

    # напишем функцию, которая находит расписание нужной группы
    def get_schedule(ds, grop_name, found_line_name):
        # Проверим не понедельник ли сегодня
        global concl
        if message.text == sets.mon:
            edgeCon = 8.0
            concl = 7
        else:
            edgeCon = 7.0
            concl = 5

        # найдем индекс столбцы с номером этой группы
        indx = ds.loc[found_line_name].tolist().index(grop_name)

        # найдем названия столбцов по найденному индексу
        columns_names = ["A", "B", "C", ds.columns[indx], ds.columns[indx + 1]]

        # вернем отфильтрованный датафрейм

        return ds.get(columns_names).loc[edgeCon:edgeNum]

    # Найдём дату и группу
    cur.execute("SELECT droup, day FROM users WHERE id = ?", (message.chat.id,))
    user_data = cur.fetchone()

    first_processing(data)
    example_grop = get_schedule(data, user_data[0], 5.0)
    result = example_grop.values.tolist()

    # сделаем функцию, которая достанет расписание нужного дня
    def get_xz(ds, day_name):
        # найдем индекс нужного дня
        indx = example_grop["A"].to_list().index(day_name)

        # получим адреса нужных ячеек
        start = ds.index.to_list()[indx]
        end = ds.index.to_list()[indx + concl]

        return ds.loc[start: end]

    example_day = get_xz(example_grop, user_data[1])
    result = example_day.values.tolist()
    s = f'Расписание на {user_data[1]}\nДля группы {user_data[0]}:\n\n'
    for day, pare, time, sub, gruop in result:
        s += f'{time}\t {sub}\t {gruop}\n'

    bot.delete_message(message.chat.id, msg.id)
    msg = bot.send_message(message.chat.id, f'{s} \nСпасибо за терпение!\nУдачного дня😊')
    # Удаляю переменную дня
    del s


def calls_handler(message, bot, Mcalls, Bcalls, Scalls, keyboard1):
    """Функция выдающая расписание звонков"""
    msg = bot.send_message(message.chat.id, 'Вспоминаю расписание звонков, это может занять несколько секунд🤔',
                           reply_markup=keyboard1)
    bot.delete_message(message.chat.id, msg.id)

    pic1 = open(Mcalls, "rb")
    pic2 = open(Bcalls, "rb")
    pic3 = open(Scalls, "rb")
    media = [InputMediaPhoto(pic1), InputMediaPhoto(pic2), InputMediaPhoto(pic3)]
    to_pin = bot.send_media_group(message.chat.id, media)
    msg = bot.send_message(message.chat.id, f'Пожалуйста! Закрепил для вашего удобства\nУдачного дня😊',
                           reply_markup=keyboard1)
    bot.pin_chat_message(chat_id=message.chat.id, message_id=to_pin[0].message_id)


def number_requests(message):
    """Функция подсчёта обращений"""
    # Берём nofr
    cur.execute("SELECT nofr FROM users WHERE id = ?", (message.chat.id,))
    nofr = cur.fetchone()
    nofr = nofr[0]
    cur.execute("UPDATE users SET nofr = ? WHERE id = ?", (nofr + 1, message.chat.id))
    conn.commit()


def fix_handler(message, bot, keyboard):
    """Функция для отправки сообщений"""
    msg = bot.send_message(message.chat.id, f'Появилась ошибка или предложение?\nСделайте меня лучше, опишите её, моему'
                                            f' создателю @arduinoespruino', reply_markup=keyboard)
