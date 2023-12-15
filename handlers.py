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
    # отправим пользователю следующее сообщение
    msg = bot.send_message(message.chat.id, 'Вспоминаю расписание, это может занять несколько секунд🤔')


def get_schedule_handler(message, bot, file_path, keyboard):
    """Функция возвращает готовое расписание для бота"""
    global otvet
    import pandas as pd
    from time import sleep

    data = pd.read_html(file_path, encoding='utf-8', header=0, index_col=0)[0].fillna('нет')

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
        # найдем индекс столбцы с номером этой группы
        indx = ds.loc[found_line_name].tolist().index(grop_name)

        # найдем названия столбцов по найденному индексу
        columns_names = ["A", "B", "C", ds.columns[indx], ds.columns[indx + 1]]

        # вернем отфильтрованный датафрейм

        return ds.get(columns_names).loc[7.0:edgeNum]
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
        end = ds.index.to_list()[indx + 5]

        return ds.loc[start: end]

    example_day = get_xz(example_grop, user_data[1])
    result = example_day.values.tolist()
    s = f'Расписание на {user_data[1]}\nДля группы {user_data[0]}:\n\n'
    for day, pare, time, sub, gruop in result:
        s += f'{time}\t {sub}\t {gruop}\n'
    sleep(1)
    msg = bot.send_message(message.chat.id, f'{s} \nСпасибо за терпение!\nУдачного дня😊', reply_markup=keyboard)
    # Удаляю переменную дня
    del s
