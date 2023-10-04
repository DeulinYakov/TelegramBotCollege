import gspread
# Указываем путь к JSON
gc = gspread.service_account(filename='printcollegebot-8db2a7ff0a19.json')
#Открываем тестовую таблицу
sh = gc.open("Копия Расписание занятий с 02.10 по 07.10.2023г.xlsx")

#Выводим значение ячейки A1
print(sh.sheet1.get('A1'))
