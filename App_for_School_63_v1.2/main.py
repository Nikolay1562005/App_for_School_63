from kivy.app import App

from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSidebar

import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

import time

from data.app_data.settingsjson import settings_json

# Список названий дней недели
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Расписание на понедельник"]
# Название листов таблицы
sheets_of_the_table = ['смена 1', 'смена 2']
# Данные со всех листов Google таблицы
information_from_the_table = []
# Список со всеми классами в школе
all_school_classes = []
# Словарь, который по названию класса выводит положение данных в списке information_from_the_table
link_to_the_schedule = {}
# https://docs.google.com/spreadsheets/d/{{{1kBwsowjGwZTrqWYa11uaJw9G4_EQsdfe0AuytT-Bi0s}}}/edit#gid=0
SAMPLE_SPREADSHEET_ID = '1kBwsowjGwZTrqWYa11uaJw9G4_EQsdfe0AuytT-Bi0s'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Ссылка на Google таблицу
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, r'data\app_data\credentials.json')  # Ключ к роботу
# Даю полномочия роботу
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

wday = time.localtime(time.time()).tm_wday  # Получение данных о текущем дне недели


# Функция получающая данные из таблицы
def getting_values_from_a_table():
    global all_school_classes, t1
    for i in range(len(sheets_of_the_table)):  # Цикл проходящий по страницам таблицы
        try:  # Ловец ошибок (если возникнет ошибка выполнение кода не прекратится
            # Вызов google таблицы по API
            result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheets_of_the_table[i]).execute()
            # Получение данных с листа таблицы в виде списка в списке
            data_from_sheet = result.get('values', [])
        except:  # При любой ошибке выполниться эта программа
            all_school_classes.append(0)  # Забивание списка пустыми данными для отсутствия возникновения ошибки
        else:  # Если ошибок не произошло выполняется код далее
            column_table = len(data_from_sheet[0])  # Нахождение этолонного количества столбцов
            rows_table = len(data_from_sheet)  # Нахождение этолонного количества строк
            for k in range(1, rows_table):  # Цикл доводящий список со списками до матрицы
                while len(data_from_sheet[k]) < column_table:
                    # Добавление пустых ячеек для приведения всех списков в списке к одной длине
                    data_from_sheet[k].append('')
            information_from_the_table.append('')  # Добавление пустого значения
            information_from_the_table[i] = []  # Превращение пустого значения в пустой список
            information_from_the_table[i] += data_from_sheet  # Добавление в пустой список матрицы data_from_sheet
            for x in range(2, column_table):  # Цикл
                name_class = data_from_sheet[0][x]  # Заношу в переменную имя класса
                all_school_classes.append(name_class)  # Добавляю в список имя класса
                link_to_the_schedule[name_class] = []  # Создаю пустой список к ячейке с ключём - именем класса
                # Добавляю в нулевое значение положение в списке страниц таблицы
                link_to_the_schedule[name_class].append(i)
                # Добавляю в первое значение положение класса в списке столбцов таблицы
                link_to_the_schedule[name_class].append(x)
    print(all_school_classes)        
    classes_1_to_9 = []
    classes_10_and_11 = []
    for k in range(len(all_school_classes) - 1):
        name = list(str(all_school_classes[k]))
        for m in range(len(name)):
            if name[m] == ' ':
                name.pop(m)
        if len(name) > 2:
            classes_10_and_11.append(all_school_classes[k])
        else:
            classes_1_to_9.append(all_school_classes[k])
    classes_1_to_9.sort()
    classes_10_and_11.sort()
    all_school_classes = classes_1_to_9 + classes_10_and_11
    all_school_classes = all_school_classes[::-1]



getting_values_from_a_table()  # Получение данных перед загрузкой приложения

# Функция поиска нужных данных из списка с матрицами
def schedule(user_selection, day):
    t1 = time.time()
    schedule_on_day = []  # Создание списка для вывода данных
    link_to_page = link_to_the_schedule[user_selection][0]  # Получение данных о номере страницы
    # Получение положения данных класса в списке с матрицами
    link_to_number_class_in_list = link_to_the_schedule[user_selection][1]
    rows_table = len(information_from_the_table[link_to_page])  # Нахождение количества строк
    quantity_rows_for_one_day_of_the_week = int(rows_table/6)  # Получение количества строчек для одного дня недели
    if day == 0 or day == 6:  # Распознание понедельника
        # Цикл для получения данных из расписания на понедельник
        for i in range(1, quantity_rows_for_one_day_of_the_week*1):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    if day == 1:  # Распознание вторника
        # Цикл для получения данных из расписания на вторник
        for i in range(quantity_rows_for_one_day_of_the_week*1 + 1, quantity_rows_for_one_day_of_the_week * 2):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    if day == 2:  # Распознание среды
        # Цикл для получения данных из расписания на среду
        for i in range(quantity_rows_for_one_day_of_the_week*2 + 1, quantity_rows_for_one_day_of_the_week * 3):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    if day == 3:  # Распознание четверга
        # Цикл для получения данных из расписания на четверг
        for i in range(quantity_rows_for_one_day_of_the_week*3 + 1, quantity_rows_for_one_day_of_the_week * 4):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    if day == 4:  # Распознание пятницы
        # Цикл для получения данных из расписания на пятницу
        for i in range(quantity_rows_for_one_day_of_the_week*4 + 1, quantity_rows_for_one_day_of_the_week * 5):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    if day == 5:  # Распознание субботы
        # Цикл для получения данных из расписания на субботу
        for i in range(quantity_rows_for_one_day_of_the_week*5 + 1, rows_table):
            schedule_on_day.append(information_from_the_table[link_to_page][i][1])  # Занесение в список времени звонков
            # Занесение в список уроков класса
            schedule_on_day.append(information_from_the_table[link_to_page][i][link_to_number_class_in_list])
    t2 = time.time()
    print(t2 - t1)
    return schedule_on_day


class start(AnchorLayout):
    # Функция для обновления базы данных
    def update_data(self):
        information_from_the_table.clear()  # Очистка старой базы данных
        all_school_classes.clear()
        link_to_the_schedule.clear()
        getting_values_from_a_table()  # Вызов функции получения нужных данных

    def class_school(self):  # Функция вносящая данные в вылитающий список и очищает старые
        if all_school_classes[0] == 0:  # проверка на подключение к интернету
            self.ids.day_label.text = 'Нет подключения к интернету'
        else:
            self.ids.spin.values = all_school_classes  # Добавление данных о всех классах
        self.ids.spin.color = 1, 1, 1, 1  # изменение цвета текста

    def clicked(self, value):  # Функция обработчик выбранного значения
        global wday
        selection = str(value)  # Получение данных о выбранном элементе
        wday = time.localtime(time.time()).tm_wday  # Получение данных о текущем дне недели для удобства
        self.ids.day_label.text = days[wday]  # Занесение этих данных
        if selection == 'Выберите класс':
            self.ids.spin.color = 1, 0, 0, 1  # Обращение внимания на проблему
        else:
            schedule_on_day = schedule(selection, wday)
            while len(schedule_on_day) < 14:  # Доформирование списка нужной длины
                schedule_on_day.append('')
            self.ids.l_1.text = str(schedule_on_day[0])  # Далее внесение данных из списка
            self.ids.l_2.text = str(schedule_on_day[1])
            self.ids.l_3.text = str(schedule_on_day[2])
            self.ids.l_4.text = str(schedule_on_day[3])
            self.ids.l_5.text = str(schedule_on_day[4])
            self.ids.l_6.text = str(schedule_on_day[5])
            self.ids.l_7.text = str(schedule_on_day[6])
            self.ids.l_8.text = str(schedule_on_day[7])
            self.ids.l_9.text = str(schedule_on_day[8])
            self.ids.l_10.text = str(schedule_on_day[9])
            self.ids.l_11.text = str(schedule_on_day[10])
            self.ids.l_12.text = str(schedule_on_day[11])
            self.ids.l_13.text = str(schedule_on_day[12])
            self.ids.l_14.text = str(schedule_on_day[13])

    def yesterday(self):   # Функция перемещения назад по списку дней недели
        global wday
        if wday > 0:  # Исключение случая попадание в воскресенье
            wday -= 1
        else:
            wday = 5
        self.ids.day_label.text = days[wday]
        selection = self.ids.spin.text
        if selection == 'Выберите класс':
            self.ids.spin.color = 1, 0, 0, 1  # Обращение внимания на проблему
        else:
            schedule_on_day = schedule(selection, wday)
            while len(schedule_on_day) < 14:  # Доформирование списка нужной длины
                schedule_on_day.append('')
            self.ids.l_1.text = str(schedule_on_day[0])  # Далее внесение данных из списка
            self.ids.l_2.text = str(schedule_on_day[1])
            self.ids.l_3.text = str(schedule_on_day[2])
            self.ids.l_4.text = str(schedule_on_day[3])
            self.ids.l_5.text = str(schedule_on_day[4])
            self.ids.l_6.text = str(schedule_on_day[5])
            self.ids.l_7.text = str(schedule_on_day[6])
            self.ids.l_8.text = str(schedule_on_day[7])
            self.ids.l_9.text = str(schedule_on_day[8])
            self.ids.l_10.text = str(schedule_on_day[9])
            self.ids.l_11.text = str(schedule_on_day[10])
            self.ids.l_12.text = str(schedule_on_day[11])
            self.ids.l_13.text = str(schedule_on_day[12])
            self.ids.l_14.text = str(schedule_on_day[13])

    def tomorrow(self):
        global wday
        if wday > 4:  # Исключение случая попадание в воскресенье
            wday = 0
        else:
            wday += 1
        self.ids.day_label.text = days[wday]
        selection = self.ids.spin.text
        if selection == 'Выберите класс':
            self.ids.spin.color = [1, 0, 0, 1]  # Обращение внимания на проблему
        else:
            schedule_on_day = schedule(selection, wday)
            while len(schedule_on_day) < 14:  # Доформирование списка нужной длины
                schedule_on_day.append('')
            self.ids.l_1.text = str(schedule_on_day[0])  # Далее внесение данных из списка
            self.ids.l_2.text = str(schedule_on_day[1])
            self.ids.l_3.text = str(schedule_on_day[2])
            self.ids.l_4.text = str(schedule_on_day[3])
            self.ids.l_5.text = str(schedule_on_day[4])
            self.ids.l_6.text = str(schedule_on_day[5])
            self.ids.l_7.text = str(schedule_on_day[6])
            self.ids.l_8.text = str(schedule_on_day[7])
            self.ids.l_9.text = str(schedule_on_day[8])
            self.ids.l_10.text = str(schedule_on_day[9])
            self.ids.l_11.text = str(schedule_on_day[10])
            self.ids.l_12.text = str(schedule_on_day[11])
            self.ids.l_13.text = str(schedule_on_day[12])
            self.ids.l_14.text = str(schedule_on_day[13])


class MyApp(App):  # Получение данных о построении древа виджетов из .kv файла
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        self.image_source = self.config.get('example', 'pathexample')
        self.text_color = self.config.get('example', 'stringexample')
        Window.clearcolor = (0.7725, 0.53725, 0.91372, 0.68235)
        return start()  # Запуск класса

    def build_settings(self, settings):
        settings.add_json_panel('Panel Name', self.config, data=settings_json)

    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': 'Тема',
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': ''})

    def on_config_change(self, config, section,key, value):
        if key == 'pathexample':
            self.image_source = value


if __name__ == '__main__':
    MyApp().run()  # Запуск приложения