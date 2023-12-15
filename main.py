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

"""Важные переменные"""
# Мой чат айди
my_chat_ID = 722555232

# Фаил расписания формата html
DATA_FILE_PATH = 'Лист1.html'
# Фаил звонков понедельник
Mcalls = 'Понедельник.png'
# Фаил звонков вторник - пятница
Bcalls = 'Вторник - Пятница.jpg'
# Фаил звонков суббота
Scalls = 'Суббота.jpg'
# Токен бота
# bot = telebot.TeleBot(k.TOKEN)

# Токен тестового бота
bot = telebot.TeleBot(k.TEST_TOKEN)


def add_startup_keyboard():
    """Функция создающая начальную клавиатуру для регистрации пользователя в системе"""


def schedule_keyboard():
    """Функция создающая клавиатуру расписания для выбора направления"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for x, y, z in fn.grouped(sets.areas, 3):
        markup.add(x, y, z)
    return markup


'''def send_message_to_user(message, text, keyboard=None):
    """Эта функцию отправит пользователю сообщение"""
    # Отправим сообщение пользователю и добавим нужную клавиатуру
    msg = bot.send_message(message.chat.id, text, reply_markup=keyboard)'''


# Переделать
def basic_keyboard():
    """Функция создающая клавиатуру расписания для выбора даты """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.calls)
    markup.add(sets.mon, sets.tue, sets.wed)
    markup.add(sets.thu, sets.fri, sets.sat)
    markup.add(sets.Ya)
    return markup


# Отправляю себе сообщение при каждом запуске
msg = bot.send_message(my_chat_ID, f'Всё исправно Босс!\nНачал работу')


# Обработчик команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Если пользователь прошел проверку, то работаем с ним. Напишем приветственное сообщение
    if not ch.init_user_verif_func(message):
        print('НЕТ')
        hn.start_handler(message, bot, keyboard=schedule_keyboard())
    else:
        hn.sending_message(message, bot, 'Укажите вашу группу', keyboard=schedule_keyboard())


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def function_ya(message):
    # Прописать try для защиты от ошибок
    if not ch.init_user_verif_func(message):
        print('НЕТ')
        hn.start_handler(message, bot, keyboard=schedule_keyboard())
    else:
        if message.text in sets.areas and not ch.check_user_group(message):
            # запоминаем группу и говорим что запомнили
            hn.group_handler(message, bot, keyboard=basic_keyboard())
        elif message.text in sets.days:
            # запоминаем дату
            hn.day_handler(message, bot)
            hn.get_schedule_handler(message, bot, DATA_FILE_PATH,
                                    keyboard=basic_keyboard())

        else:
            hn.sending_message(message, bot, 'fe', keyboard=basic_keyboard())


bot.infinity_polling()
