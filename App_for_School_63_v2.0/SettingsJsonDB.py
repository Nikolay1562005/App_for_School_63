import json
from get_data import get_data


class SettingsJsonDB:
    def __init__(self, sours_on_file):
        self.sours_on_file = sours_on_file
        with open(self.sours_on_file, 'r') as file:
            data = json.load(file)

        self.create_attributes(data)

        # self.datetime = datetime.strptime(data.get('datetime'), '%Y-%m-%d %H:%M:%S')

    def create_attributes(self, data):
        for name, value in data.items():
            setattr(self, name, value)

    def to_json(self):
        with open(self.sours_on_file, 'w') as file:
            json.dump(vars(self), file, indent=4)

    def update_from_table(self):
        data_from_table = get_data()
        if data_from_table.get('error') == None:
            for name, value in data_from_table.items():
                setattr(self, name, value)

            return self.schedule_classes
        else:
            pass


if __name__ == '__main__':
    settings = SettingsJsonDB("settings.json")
    setattr(settings, 'days', ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
    # settings.update_from_table()
    print(vars(settings).keys())
    settings.to_json()