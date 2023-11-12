from telebot.types import InputMediaPhoto
edge = 'BT'
edgeNum = 51.0


def secondary_functions(message, bot, keyboard):
    """Обработчик второстепенной команды(пока только что ты можешь)"""
    msg = bot.send_message(message.chat.id, f'Пока что я могу немного, но с Вашей помощью я стану лучшим '
                                            f'ассистентом📝\n\nВы можете помочь мне стать лучше, написав моему '
                                            f'создателю. Мы будем очень рады услышать Ваше мнение и '
                                            f'предложения!\n\n@arduinoespruino', reply_markup=keyboard)


def main_func_handler(message, dict, bot, keyboard):
    """Обработчик главных функций. Пока обработаывает только функцию
    расписание."""
    # запишем состояние общения с пользователем
    if dict.get(message.chat.id, None) is None:
        dict[message.chat.id] = []
    dict[message.chat.id].append(message.text)
    # отпрвим пользователю следующее собщение
    msg = bot.send_message(message.chat.id,
                           'Выберите интересующее направление',
                           reply_markup=keyboard)


def group_handler(message, dict, bot, keyboard):
    """Обработчки групп"""
    # закинем инфу о группе в словарик
    dict[message.chat.id].append(message.text)
    # отпрвим пользователю следующее собщение
    msg = bot.send_message(message.chat.id,
                           'Выберите день недели',
                           reply_markup=keyboard)


def day_handler(message, dict, bot, keyboard):
    """Обработчк дня записанного пользователем"""

    # закинем инфу о группе в словарик
    dict[message.chat.id].append(message.text)

    # отпрвим пользователю следующее собщение
    msg = bot.send_message(message.chat.id, 'Вспоминаю расписание, это может занять несколько секунд🤔')


def get_schedule_handler(message, bot, file_path, user_data, dict, keyboard):
    """Функция возвращает готовое расписание для бота"""
    global otvet
    import pandas as pd
    from time import sleep

    data = pd.read_html(file_path, header=0, index_col=0)[0].fillna('нет')

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

    # напишем функцию которая находит расписание нужной группы
    def get_schedule(ds, grop_name, found_line_name):
        # найдем индекс столбцы с номером этой группы
        indx = ds.loc[found_line_name].tolist().index(grop_name)

        # найдем названия столбцов по найденному индексу
        columns_names = ["A", "B", "C", ds.columns[indx], ds.columns[indx + 1]]

        # вернем отфильтрованный датафрейм

        return ds.get(columns_names).loc[7.0:edgeNum]

    first_processing(data)
    example_grop = get_schedule(data, user_data[1], 5.0)
    result = example_grop.values.tolist()

    # сделаем функцию которая достанет расписание нужного дня
    def get_xz(ds, day_name):
        # найдем индекс нужного дня
        indx = example_grop["A"].to_list().index(day_name)

        # получим адреса нужных ячеек
        start = ds.index.to_list()[indx]
        end = ds.index.to_list()[indx + 5]

        return ds.loc[start: end]

    example_day = get_xz(example_grop, user_data[2])
    result = example_day.values.tolist()
    s = ''
    for day, pare, time, sub, gruop in result:
        s += f'{time}\t {sub}\t {gruop}\n'
    sleep(1)
    msg = bot.send_message(message.chat.id, f'{s} \nСпасибо за терпение!\nУдачного дня😊', reply_markup=keyboard)
    # Удаляю переменную дня
    del s


def get_mon_schedule_handler(message, bot, file_path, user_data, dict, keyboard):
    """Функция возвращает готовое расписание для бота для понедельника"""
    global otvet
    import pandas as pd
    from time import sleep
    data = pd.read_html(file_path, header=0, index_col=0)[0].fillna('нет')

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

    # напишем функцию которая находит расписание нужной группы
    def get_schedule(ds, grop_name, found_line_name):
        # найдем индекс столбцы с номером этой группы
        indx = ds.loc[found_line_name].tolist().index(grop_name)

        # найдем названия столбцов по найденному индексу
        columns_names = ["A", "B", "C", ds.columns[indx], ds.columns[indx + 1]]

        # вернем отфильтрованный датафрейм

        return ds.get(columns_names).loc[8.0:edgeNum]

    first_processing(data)
    example_grop = get_schedule(data, user_data[1], 5.0)
    result = example_grop.values.tolist()

    # сделаем функцию которая достанет расписание нужного дня
    def get_xz(ds, day_name):
        # найдем индекс нужного дня
        indx = example_grop["A"].to_list().index(day_name)

        # получим адреса нужных ячеек
        start = ds.index.to_list()[indx]
        end = ds.index.to_list()[indx + 6]

        return ds.loc[start: end]

    example_day = get_xz(example_grop, user_data[2])
    result = example_day.values.tolist()
    s = ''
    for day, pare, time, sub, gruop in result:
        s += f'{time}\t {sub}\t {gruop}\n'
    sleep(1)
    msg = bot.send_message(message.chat.id, f'{s} \nСпасибо за терпение!\nУдачного дня😊', reply_markup=keyboard)
    # Удаляю переменную дня
    del s


def calls_handler(message, bot, Mcalls, Bcalls, Scalls, keyboard):
    from time import sleep
    """Функция выдающая расписание звонков"""
    msg = bot.send_message(message.chat.id, 'Вспоминаю расписание звонков, это может занять несколько секунд🤔', reply_markup=keyboard)
    pic1 = open(Mcalls, "rb")
    pic2 = open(Bcalls, "rb")
    pic3 = open(Scalls, "rb")
    media = [InputMediaPhoto(pic1, caption='Пожалуйста, Вы можете закрепить это сообщение, для Вашего удобства.'
                                           ' Удачного дня😊'), InputMediaPhoto(pic2), InputMediaPhoto(pic3)]
    sleep(1)
    bot.send_media_group(message.chat.id, media)


def start_handler(message, dict, bot, keyboard):
    """Функция меню"""
    if dict.get(message.chat.id, None) is None:
        dict[message.chat.id] = []
    del dict[message.chat.id]
    msg = bot.send_message(message.chat.id, "Чем я могу Вам помочь?", reply_markup=keyboard)


def back_group(message, dict):
    """Обработчик замены группы"""

    # удалим последний элемент группы
    dict[message.chat.id].pop()


def back_func_handler(message, bot, keyboard):
    """Обработчик замены группы выбор групп"""
    # отпрвим пользователю следующее собщение
    msg = bot.send_message(message.chat.id,
                           'Выберите интересующее направление',
                           reply_markup=keyboard)


def back_func_day(message, bot, keyboard):
    """Обработчки групп"""
    # отпрвим пользователю следующее собщение
    msg = bot.send_message(message.chat.id,
                           'Выберите день недели',
                           reply_markup=keyboard)
