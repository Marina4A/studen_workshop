import json


class Manager:
    def __init__(self):
        # self.path_directory = path
        self.data = self.get_directory()

    def menu(self):
        while True:
            move = input('Введите действие: ')

    def get_directory(self):
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return fr"{data_dict['path']}"

    def choose_directory(self):
        new_path = input('Введите новую директорию: ')
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        data_dict['path'] = new_path
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, indent=4)
        self.data = fr"{new_path}"

    def __str__(self):
        return f'Путь файла {self.data}'


if __name__ == '__main__':
    manager = Manager()
    print(manager)
    manager.choose_directory()
    print(manager)
