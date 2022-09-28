import json
import inspect
import shutil
import os


class Manager:

    def __init__(self):
        self.data = self.get_directory().replace('\\', os.sep).replace('/', os.sep)
        self.path = os.getcwd()
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
        self.check_users()
        while True:
            move = input(f'{self.path}: ')
            command, *args = move.split()
            if command in self.dict_cmds.keys():
                args_func = inspect.getfullargspec(self.dict_cmds[command])[0]
                if len(args_func) - 1 == len(args):
                    self.dict_cmds[command](*args)
                else:
                    print(f'Функция {command} ждет {len(args_func) - 1} аргумент(а)')
            else:
                print('Некорректный ввод!')

    def check_users(self):
        while True:
            check_name = input('Вы зарегистрированы в системе (да/нет)? ')
            name_user = input('Введите имя пользователя: ')
            passord_user = input('Введите пароль: ')
            if check_name.lower() in 'да':
                with open('users.json', 'r+', encoding='utf-8') as file:
                    users = json.load(file)
                if name_user in users:
                    while True:
                        if users[name_user] == passord_user:
                            directory_users = os.path.join(self.path, name_user)
                            if not os.path.isdir(directory_users):
                                os.mkdir(directory_users)
                            self.path = directory_users
                            self.data = directory_users
                            print(f'Добро пожаловать! {name_user}')
                            break
                        else:
                            print('Неверный пароль! Попробуйте еще раз!')
                            passord_user = input('Введите пароль: ')
                    break
                else:
                    print('Пользователь не найден!')
            elif check_name.lower() in 'нет':
                with open('users.json', 'r', encoding='utf-8') as file:
                    users = json.load(file)
                if name_user not in users:
                    with open('users.json', 'w+', encoding='utf-8') as file:
                        users[name_user] = passord_user
                        json.dump(users, file, indent=4)
                    directory_users = os.path.join(self.path, name_user)
                    self.path = directory_users
                    self.data = directory_users
                    os.mkdir(directory_users)
                    print(f'Вы зарегистрированы! Добро пожаловать, {name_user}!')
                    break
                else:
                    print('Такой пользователь уже существует!')

    def get_directory(self):
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        return fr"{data_dict['path']}"

    def choose_directory(self):  # изменение директории
        new_path = input('Введите новую директорию: ').replace('\\', os.sep).replace('/', os.sep)
        with open('settings.json', 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
            data_dict['path'] = new_path
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, indent=4)
        self.data = fr"{new_path}"

    def create_directory(self, name_directory):  # создание папки
            directory_path = os.path.join(self.path, name_directory)
            type_file = ('txt', 'doc', 'docx', 'csv', 'xlsx', 'xls', 'zip')
            if not os.path.exists(directory_path) and '.' not in name_directory and \
                    not name_directory.endswith(type_file):
                os.mkdir(directory_path)
                print(f'Папка {name_directory} создана!')
            elif os.path.exists(directory_path):
                print(f'Папка {name_directory} уже существует!')
            else:
                print('Некорректный ввод!')

    def delete_directory(self, name_directory):  # удаление папки
        try:
            directory_path = os.path.join(self.path, name_directory)
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
                print(f'Папка {name_directory} удалена!')
            else:
                print(f'Папки {name_directory} не существует!')
        except NotADirectoryError:
            print(f'Папка не может содержать такой формат!')

    def move_directory(self, name_directory):  # перемещение между папками
        move_directory = ''
        path_directory = name_directory
        if '..' in name_directory:
            move_directory, name_directory = '..', ''
            path_directory = self.data
        elif name_directory != '..':
            path_directory = os.path.join(self.path, name_directory)

        if move_directory == '' and os.path.isdir(path_directory):
            self.path = path_directory
            print(f'Переход в директорию {name_directory} выполнен успешно!')
        elif move_directory == '..':
            path_name = self.path.split(os.sep)[:-1]
            new_path = f'{os.sep}'.join(path_name)
            if new_path.startswith(self.data):
                self.path = new_path
                print(f'Выход из директории выполнен успешно!')
            else:
                print('Выход за пределы корневой директории не возможен!')
        else:
            print('Некорректный ввод!')

    def create_file(self, name_file):  # создать файл
        file_path = os.path.join(self.path, name_file)
        if not os.path.exists(file_path) and self.file_name_check(name_file):
            file = open(file_path, 'tw', encoding='utf-8')
            file.close()
            print(f'Файл, {name_file}, создан!')
        elif os.path.exists(file_path) and self.file_name_check(name_file):
            print(f'Файл, {name_file}, уже существует!')

    def write_file(self, name_file):  # запись текста в файл
        text = input('Введите текст для записи в файл: ')
        file_path = os.path.join(self.path, name_file)
        if os.path.exists(file_path) and self.file_name_check(name_file):
            with open(file_path, 'a+', encoding='utf-8') as file:
                file.write(text)
                print(f'Информация успешно записана!')
        elif not os.path.exists(file_path):
            print(f'Файла {name_file} не существует!')

    def read_file(self, name_file):  # просмотр содержимого текстового файла
        file_path = os.path.join(self.path, name_file)
        if os.path.exists(file_path) and self.file_name_check(name_file):
            with open(file_path, 'r', encoding='utf-8') as file:
                print(file.read())
        elif not os.path.exists(file_path):
            print(f'Файла {name_file} не существует!')

    def delete_file(self, name_file):  # удаление файлов
        file_path = os.path.join(self.path, name_file)
        if os.path.exists(file_path) and os.path.exists(file_path):
            os.remove(file_path)
            print(f'Файл {name_file} удален!')
        elif not os.path.exists(file_path) or not self.file_name_check(name_file):
            print('Такого файла не существует!')

    def copy_file(self):  # копирование файла
        start_path, finish_path = self.path_check('скопировать')
        shutil.copy(fr'{start_path}', fr'{finish_path}')

    def move_file(self):  # перемещение файла
        start_path, finish_path = self.path_check('переместить')
        shutil.move(fr'{start_path}', fr'{finish_path}')

    def rename_file(self, name_file, rename_file):  # переименование файла
        old_name_file = os.path.join(self.path, name_file)
        new_name_file = os.path.join(self.path, rename_file)
        if os.path.exists(old_name_file) and self.file_name_check(name_file) and \
                old_name_file[old_name_file.find('.'):] == new_name_file[new_name_file.find('.'):]:
            os.rename(old_name_file, new_name_file)
            print(f'Файл {name_file} изменен на {rename_file}!')
        elif not os.path.exists(old_name_file) or not self.file_name_check(name_file) and \
                old_name_file[old_name_file.find('.'):] == new_name_file[new_name_file.find('.'):]:
            print(f'Файла {name_file} не существует!')
        elif os.path.exists(old_name_file) and self.file_name_check(name_file) and \
                old_name_file[old_name_file.find('.'):] != new_name_file[new_name_file.find('.'):]:
            print(f'Файл {rename_file} и {name_file} разного формата!')
        else:
            print('Некорректный ввод! Попробуйте еще раз!')

    def zip_directory(self, name_directory):  # архивация папки
        name_all_directory = os.walk(self.data)
        path_directory = ''
        name_zip = ''
        for directory in name_all_directory:
            name_zip = os.path.join(f'{directory[0]}.zip')
            if directory[0].endswith(name_directory):
                path_directory = directory[0]
                break
        if path_directory != '' and not os.path.exists(name_zip):
            shutil.make_archive(path_directory, format='zip', base_dir=name_directory)
            print(f'{name_directory} заархивирован!')
        elif os.path.exists(name_zip):
            print(f'{name_directory}.zip уже существует!')
        elif path_directory == '':
            print(f'Папки {name_directory} не существует!')

    def unzip_directory(self, name_directory):  # разархивация папки
        name_all = os.walk(self.data)
        name_directory = f'{name_directory}.zip'
        for directory in name_all:
            if name_directory in directory[2]:
                path_directory = os.path.join(directory[0], name_directory)
                shutil.unpack_archive(path_directory, format='zip', extract_dir=directory[0])
                os.remove(path_directory)
                print(f'Файл {name_directory} разархифирован!')
                break
        else:
            print(f'Архифа {name_directory} не существует!')

    def file_name_check(self, name_file):
        type_file = ('txt', 'doc', 'docx', 'csv', 'xlsx', 'xls', 'zip')
        if '.' in name_file and name_file.endswith(type_file) and \
                len(name_file[:name_file.find('.')]) > 0:
            return True
        else:
            print('Некорректное название файла')

    def path_check(self, move_file):
        current_directory = os.path.basename(self.path)
        while True:
            name_file_directory = input(f'Введите папку и файл откуда/что {move_file}: ').split()
            if len(name_file_directory) > 1:
                name_directory, name_file = name_file_directory
                path_directory = os.path.join(self.path, name_directory)
                if self.file_name_check(name_file):
                    path_file = os.path.join(path_directory, name_file)
                    if (os.path.isfile(os.path.join(path_directory, path_file)) and
                        os.path.isdir(os.path.join(self.path, name_directory))) or \
                            (name_directory == current_directory and
                             os.path.isfile(os.path.join(self.path, name_file))):
                        if current_directory == name_directory:
                            start_path = os.path.join(self.path, name_file)
                            break
                        else:
                            start_path = os.path.join(self.path, name_directory, name_file)
                            break
                elif not self.file_name_check(name_file):
                    print(f'Папки {name_directory} не существует!')
                elif os.path.isfile(self.file_name_check(name_file)) and \
                        not os.path.isdir(os.path.join(self.path, name_directory)):
                    print(f'Файла {name_file} не существует!')
                else:
                    print('Некорректный ввод!')
        while True:
            name_directory_finish = input('Введите папку куда вставить, скопированный файл: ')
            if len(name_directory_finish) > 0:
                finish_path = os.path.join(self.path, name_directory_finish)
                if os.path.isdir(finish_path):
                    break
                else:
                    print('Такой папки не существует. Попробуйте еще раз!')
        return start_path, finish_path


if __name__ == '__main__':
    manager = Manager()
    manager.menu()
