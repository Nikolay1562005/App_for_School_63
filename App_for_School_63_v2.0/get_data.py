import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

from datetime import datetime
from re import sub
import json
from pprint import pprint

def get_data(
        link_to_table=r'https://docs.google.com/spreadsheets/d/1kBwsowjGwZTrqWYa11uaJw9G4_EQsdfe0AuytT-Bi0s/edit#gid=0',
        names_pages=['смена 1', 'смена 2']):
    if r'https://docs.google.com/spreadsheets/' in link_to_table:
        account = connecting_to_google_service_account()
        data = getting_values_from_table(account, names_pages, link_to_table)
        return data
    else:
        return {'error': 'Не корректная ссылка на таблицу'}


def connecting_to_google_service_account(file_credentials_of_account=r'data\app_data\credentials.json'):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, file_credentials_of_account)  # Ключ к боту
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Ссылка на сервис
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    return service


def getting_values_from_table(service, names_pages, link_to_table):
    place_table_on_server = sub(r'https://docs.google.com/spreadsheets/./', '', link_to_table)  # удаление лишних частей
    SAMPLE_SPREADSHEET_ID = sub(r'/(.*)', '', place_table_on_server)  # удаление лишних частей
    data_from_pages = []
    data_and_time = str(datetime.now()).split('.')[0]  # %Y-%m-%d %H:%M:%S
    for i in range(len(names_pages)):
        try:
            result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=names_pages[i]).execute()
            data_from_sheet = result.get('values', [])
        except:
            pass
        else:
            len_column_table = len(data_from_sheet[0])  # Нахождение этолонного количества столбцов
            len_rows_table = len(data_from_sheet)  # Нахождение этолонного количества строк
            for k in range(1, len_rows_table):  # Цикл доводящий список со списками до матрицы
                while len(data_from_sheet[k]) < len_column_table:
                    # Добавление пустых ячеек для приведения всех списков в списке к одной длине
                    data_from_sheet[k].append('')

            data_from_pages.append(data_from_sheet)

    dictionary_of_groups_schedules = formation_of_groups(data_from_pages)
    groups_schedules = sorted_groups(dictionary_of_groups_schedules)
    return {
        'datetime': data_and_time,
        'schedule_classes': groups_schedules
    }


def formation_of_groups(data):
    groups = {}

    for page in data:
        names_groups = [name.strip() for name in page[0][2:]]
        groups |= {name: [[] for _ in range(6)] for name in names_groups}
        count_of_lessons = round(len(page) / 6)
        for number_wday in range(6):
            for day in range(number_wday * count_of_lessons + 1, (number_wday + 1) * count_of_lessons):
                lesson_time = page[day][1].strip()
                for number_group, lesson in enumerate(page[day][2:]):
                    if lesson != '':
                        groups[names_groups[number_group]][number_wday].append([lesson_time, lesson.strip()])
    return groups


def sorted_groups(data):
    all_names_groups = list(data.items())
    all_names_groups.sort()
    all_names_groups.sort(key=lambda iter: len(iter[0]))
    return dict(all_names_groups[::-1])


if __name__ == '__main__':
    pprint(get_data())