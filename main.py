# Библиотеки
import telebot
from telebot import *
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InputMediaPhoto
#import html5lib
import sets
import funcs as fn
import handlers as hn
from time import sleep


my_chat_ID = 722555232
# Типо он ассинхроный
MEMORY = {}
# Фаил расписания формата html /home/pip/Desktop/bot
DATA_FILE_PATH = '/home/pip/Desktop/bot/Лист1.html'
# Фаил звонков понедельник
Mcalls = '/home/pip/Desktop/bot/Понедельник.jpg'
# Фаил звонков вторник - пятница
Bcalls = '/home/pip/Desktop/bot/Вторник - Пятница.jpg'
# Фаил звонков суббота
Scalls = '/home/pip/Desktop/bot/Суббота.jpg'
# Токен бота
bot = telebot.TeleBot('TOKEN')


# Токен тестового бота
#bot = telebot.TeleBot('755635624:AAH5Af2ZNRtDf2wKOm5bF1mWXLzIl4slRx8')


# Функции
def add_startup_keyboard():
    """Функция создающая начальную клавиатуру для выбора функций бота"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.schedule)
    markup.add(sets.calls)
    markup.add(sets.Ya)
    return markup


def startup_keyboard():
    """Функция создающая начальную клавиатуру для выбора функций бота"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.menu)
    return markup


def back_day_keyboard():
    """Функция создающая начальную клавиатуру для выбора функций бота"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.back_day)
    markup.add(sets.menu)
    return markup


def schedule_keyboard():
    """Функция создающая клавиатуру расписания для выбора направления"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for x, y, z in fn.grouped(sets.areas, 3):
        markup.add(x, y, z)
    markup.add(sets.menu)
    return markup


def data_keyboard():
    """Функция создающая клавиатуру расписания для выбора даты sets.mon,"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(sets.back)
    markup.add(sets.tue, sets.wed)
    markup.add(sets.thu, sets.fri, sets.sat)
    markup.add(sets.menu)
    return markup


def send_message_to_user(message, text, keyboard=None):
    """Эта функцию отправит пользователю сообщение"""
    # Отправим сообщение пользователю и добавим нужную клавиатуру
    msg = bot.send_message(message.chat.id, text, reply_markup=keyboard)


# Отправляю себе сообщение при каждом запуске
msg = bot.send_message(my_chat_ID, f'Босс, я перезагрузился.\nНачал работу')


# Обработчик команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Если пользователь прошел проверку, то работаем с ним. Напишем приветственное сообщение
    hn.start_handler(message, MEMORY, bot, keyboard=add_startup_keyboard())


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def function_ya(message):
    try:
        if message.text in sets.main_functions:
            # запуск обработчика основынх функций бота
            hn.main_func_handler(message, MEMORY, bot, keyboard=schedule_keyboard())
        elif message.text in sets.Ya:
            # запуск обработчика второстепенных функций
            hn.secondary_functions(message, bot, keyboard=startup_keyboard())
        elif message.text in sets.areas and MEMORY[message.chat.id][0] == sets.schedule:
            # обработчик групп
            hn.group_handler(message, MEMORY, bot, keyboard=data_keyboard())
        elif message.text in sets.days and MEMORY[message.chat.id][1] in sets.areas:
            # обработчик дней вторник - суббота и обработчик выдачи результата
            hn.day_handler(message, MEMORY, bot, keyboard=back_day_keyboard())
            hn.get_schedule_handler(message, bot, DATA_FILE_PATH, MEMORY[message.chat.id], MEMORY,
                                    keyboard=back_day_keyboard())
        elif message.text in sets.mon and MEMORY[message.chat.id][1] in sets.areas:
            # обработчик понедельника и обработчик выдачи результата
            hn.day_handler(message, MEMORY, bot, keyboard=back_day_keyboard())
            hn.get_mon_schedule_handler(message, bot, DATA_FILE_PATH, MEMORY[message.chat.id], MEMORY,
                                        keyboard=back_day_keyboard())
        elif message.text in sets.calls:
            # обработчик второстепенной функции звонков
            hn.calls_handler(message, bot, Mcalls, Bcalls, Scalls, keyboard=startup_keyboard())
        elif message.text in sets.menu:
            # Функция меню
            hn.start_handler(message, MEMORY, bot, keyboard=add_startup_keyboard())
        elif message.text in sets.back and MEMORY[message.chat.id][0] == sets.schedule:
            # Замена группы
            hn.back_group(message, MEMORY)
            hn.back_func_handler(message, bot, keyboard=schedule_keyboard())
        elif message.text in sets.back_day and MEMORY[message.chat.id][1] in sets.areas:
            # Замена дня
            hn.back_group(message, MEMORY)
            hn.back_func_day(message, bot, keyboard=data_keyboard())
        else:
            # пользователь пишет парашу, шлем его
            pass
    except:
        send_message_to_user(message, f'Упс😓... Что-то пошло не так, давайте попробуем заново', startup_keyboard())


bot.infinity_polling()
