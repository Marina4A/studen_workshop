import json
import inspect
import os
import os


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
            'unzdir': self.unzip_directory,
            'chdir': self.choose_directory
        }

    def menu(self):
        while True:
            move = input('Введите действие: ')
            command, *args = move.split()
            if command in self.dict_cmds.keys():
                args_func = inspect.getfullargspec(self.dict_cmds[command])[0]
                if len(args_func) - 1 == len(args):
                    self.dict_cmds[command](*args)
                else:
                    print(f'Функция {command} ждет {len(args_func) - 1} аргумент(а)')

    def get_directory(self):
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return fr"{data_dict['path']}"

    def choose_directory(self):  # изменение директории
        new_path = input('Введите новую директорию: ')
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        data_dict['path'] = new_path
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, indent=4)
        self.data = fr"{new_path}"

    def create_directory(self, name_directory):  # создание папки
        directory_path = os.path.join(self.data, name_directory)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            print(f'Папка {name_directory} создана!')
        else:
            print(f'Папка {name_directory} уже существует!')

    def delete_directory(self, name_directory):  # удаление папки
        directory_path = os.path.join(self.data, name_directory)
        if os.path.exists(directory_path):
            os.rmdir(directory_path)
            print(f'Папка {name_directory} удалена!')
        else:
            print(f'Папки {name_directory} не существует!')

    def move_directory(self, start_path, finish_path):  # перемещение между папками
        pass

    def create_file(self, name_file):  # создать файл
        file_path = os.path.join(self.data, name_file)
        if not os.path.exists(file_path) and self.file_name_check(name_file):
            file = open(name_file, 'tw', encoding='utf-8')
            file.close()
            print(f'Файл, {name_file}, создан!')
        elif os.path.exists(file_path) and self.file_name_check(name_file):
            print(f'Файл, {name_file}, уже существует!')

    def write_file(self, name_file, text_file):  # запись текста в файл
        file_path = os.path.join(self.data, name_file)
        if os.path.exists(file_path) and self.file_name_check(name_file):
            with open(name_file, 'a+', encoding='utf-8') as file:
                file.write(text_file)
        elif not os.path.exists(file_path):
            print(f'Файла {name_file} не существует!')

    def read_file(self, name_file):  # просмотр содержимого текстового файла
        file_path = os.path.join(self.data, name_file)
        if os.path.exists(file_path) and self.file_name_check(name_file):
            with open(name_file, 'r', encoding='utf-8') as file:
                print(file.read())
        elif not os.path.exists(file_path):
            print(f'Файла {name_file} не существует!')

    def delete_file(self, name_file):  # удаление файлов
        file_path = os.path.join(self.data, name_file)
        if os.path.exists(file_path) and self.file_name_check(name_file):
            os.remove(file_path)
            print(f'Файл {name_file} удален!')
        elif not os.path.exists(file_path) or not self.file_name_check(name_file):
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
        if '.' in name_file and name_file.endswith(type_file) and \
                len(name_file[:name_file.find('.')]) > 0:
            return True
        else:
            print('Некорректное название файла')

    def __str__(self):
        return f'Путь файла {self.data}'


if __name__ == '__main__':
    manager = Manager()
    manager.menu()
