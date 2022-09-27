import json
import inspect
from os import path


class Manager:

    def __init__(self):
        # self.path_directory = path
        self.data = self.get_directory()

        self.dict_cmds = {
            'cdir': self.create_directory,
            'ddir': self.delete_directory,
            'mdir': self.move_directory,
            'cfile': self.create_file,
            'wfile': self.write_file,
            'rfile': self.read_file,
            'dfile': self.delete_file,
            'cpfile': self.copy_file,
            'mfile': self.move_file,
            'rnfile': self.rename_file,
            'zdir': self.zip_directory,
            'unzdir': self.unzip_directory
        }

    def menu(self):
        while True:
            move = input('Введите действие: ')
            command, *args = move.split()
            if command in self.dict_cmds.keys():
                args_func = inspect.getfullargspec(self.dict_cmds[command])[0]
                # print(args_func)
                if len(args_func) - 1 == len(args):
                    # print(len(args_func) - 1, args)
                    self.dict_cmds[command](*args)
                # else:
                #     print(f'Функция {command} ждет {len(args_func) - 1} аргумент(а)')

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

    def create_directory(self, path):  # создание папки
        pass

    def delete_directory(self, path):  # удаленин папки
        pass

    def move_directory(self, start_path, finish_path):  # перемещение между папками
        pass

    def create_file(self, name_file):  # создать файл
        self.file_name_check(name_file)
        file = open(name_file, 'tw', encoding='utf-8')
        file.close()
        print('Файл создан!')

    def write_file(self, name_file, text_file):  # запись текста в файл
        self.file_name_check(name_file)

    def read_file(self, path):  # просмотр содержимого текстового файла
        pass

    def delete_file(self, name_file):  # удаление файлов
        self.file_name_check(name_file)
        file_path = self.data + '\\' + name_file
        if path.exists(file_path):
            print(f'Файл {name_file} удален!')
        elif not path.exists(file_path):
            print('Такого файла не существует!')

    def copy_file(self, start_path, finish_path):  # копирование файла
        pass

    def move_file(self, start_path, finish_path):  # перемещение файла
        pass

    def rename_file(self, path, new_name):  # переименование файла
        pass

    def zip_directory(self, path):  # архивация папки
        pass

    def unzip_directory(self, path):  # разархивация папки
        pass

    def file_name_check(self, name_file):
        type_file = ('txt', 'doc', 'docx', 'csv', 'xlsx', 'xls')
        while True:
            if '.' in name_file and name_file.endswith(type_file) and len(name_file[:name_file.find('.')]) > 0:
                return True
            name_file = input('Введите корректное название файла: ')

    def __str__(self):
        return f'Путь файла {self.data}'


if __name__ == '__main__':
    manager = Manager()
    manager.menu()
