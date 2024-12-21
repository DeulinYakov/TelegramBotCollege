"""Импорты"""
# Библиотеки для работы с ботом
import telebot
from telebot import *
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InputMediaPhoto

# Подключаем локальные модули
import sets
import funcs as fn
import handlers as hn
import check as ch
import key as k

# Подключаем MySQLite
import sqlite3

"""Важные переменные"""
# Мой чат айди
my_chat_ID = 722555232

# Фаил расписания формата html
DATA_FILE_PATH = 'Лист1.html'
# Фаил звонков понедельник
Mcalls = './images/Понедельник.jpg'
# Фаил звонков вторник - пятница
Bcalls = './images/Вторник - Пятница.jpg'

# Токен бота
# bot = telebot.TeleBot(k.TOKEN)

# Токен тестового бота
bot = telebot.TeleBot(k.TEST_TOKEN)


def schedule_keyboard():
    """Функция создающая клавиатуру расписания для выбора направления"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for x, y, z in fn.grouped(sets.areas, 3):
        markup.add(x, y, z)
    return markup


def basic_keyboard():
    """Функция создающая клавиатуру расписания для выбора даты """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.calls)
    markup.add(sets.mon, sets.tue, sets.wed)
    markup.add(sets.thu, sets.fri, sets.sat)
    markup.add(sets.Ya)
    markup.add(sets.fix)
    return markup


# Отправляю себе сообщение при каждом запуске
msg = bot.send_message(my_chat_ID, f'Всё исправно Босс!\nНачал работу')


# Обработчик команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Если пользователь прошел проверку, то работаем с ним. Напишем приветственное сообщение
    if not ch.init_user_verif_func(message):
        hn.start_handler(message, bot, keyboard=schedule_keyboard())
    else:
        hn.sending_message(message, bot, 'Укажите вашу группу', keyboard=schedule_keyboard())


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def function_ya(message):
    # Прописать try для защиты от ошибок
    try:
        if not ch.init_user_verif_func(message):
            # Обработчик новых юзеров
            hn.start_handler(message, bot, keyboard=schedule_keyboard())
        else:
            if message.text in sets.areas:
                # обработчик групп
                hn.group_handler(message, bot, keyboard=basic_keyboard())
            elif message.text in sets.days:
                # обработчик дня и обработчик выдачи результата
                hn.day_handler(message, bot)
                hn.get_schedule_handler(message, bot, DATA_FILE_PATH)
                hn.number_requests(message)
                hn.sending_message(message, bot, 'Выберите день или раздел, который вас интересует.😉',
                                   keyboard=basic_keyboard())

            elif message.text in sets.Ya:
                # обработчик замены группы
                hn.sending_message(message, bot, 'Ожидаю указание новой группы🤔', keyboard=schedule_keyboard())
            elif message.text in sets.calls:
                # обработчик второстепенной функции звонков
                hn.calls_handler(message, bot, Mcalls, Bcalls, keyboard1=basic_keyboard())
                hn.number_requests(message)
                hn.sending_message(message, bot, 'Выберите день или раздел, который вас интересует.😉',
                                   keyboard=basic_keyboard())
            elif message.text in sets.fix:
                # временная функция
                hn.fix_handler(message, bot, keyboard=basic_keyboard())
            else:
                hn.sending_message(message, bot, 'Выберите день или раздел, который вас интересует.😉',
                                   keyboard=basic_keyboard())
    except:
        hn.sending_message(message, bot, f'Упс😓... Что-то пошло не так, давайте попробуем заново',
                           keyboard=basic_keyboard())


'''# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    message = call.message
    if call.data == 'fix':
        bot.pin_chat_message(chat_id=message.chat.id, message_id=hn.to_pin[0].message_id)
'''


def get_chat_ids_from_db():
    """Извлекает все chat.id из базы данных."""
    connection = sqlite3.connect("basetest.db")
    cursor = connection.cursor()

    # Предполагается, что таблица называется `users` и имеет столбец `id`
    cursor.execute("SELECT id FROM users")
    chat_ids = [row[0] for row in cursor.fetchall()]

    connection.close()
    return chat_ids


if __name__ == "__main__":
    chat_ids = get_chat_ids_from_db()
    print("Полученные chat IDs:", chat_ids)

    for chat_id in chat_ids:
        try:
            video_path = "IMG_6813.MP4"  # Укажите путь к вашему видео файлу
            with open(video_path, "rb") as video:
                bot.send_video(chat_id, video, caption="Привет")
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {chat_id}: {e}")
bot.infinity_polling()
