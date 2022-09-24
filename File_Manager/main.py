import json
import inspect


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
                if len(args_func) - 1 == len(args):
                    self.dict_cmds[command](*args)
                else:
                    print(f'Функция {command} ждет {len(args_func) - 1} аргумент(а)')

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

    def create_directory(self, path):
        pass

    def delete_directory(self, path):
        pass

    def move_directory(self, start_path, finish_path):
        pass

    def create_file(self, path):
        pass

    def write_file(self, path, text):
        pass

    def read_file(self, path):
        pass

    def delete_file(self, path):
        pass

    def copy_file(self, start_path, finish_path):
        pass

    def move_file(self, start_path, finish_path):
        pass

    def rename_file(self, path, new_name):
        pass

    def zip_directory(self, path):
        pass

    def unzip_directory(self, path):
        pass

    def __str__(self):
        return f'Путь файла {self.data}'


if __name__ == '__main__':
    manager = Manager()
    manager.menu()
