import socket
import hashlib
import json
import pickle
from threading import Thread
import logging

from validation import free_port, port_validation

logging.basicConfig(format='%(asctime)s {%(level_name)s %(func_name)s: %(nessage)s}',
                    handlers=[logging.FileHandler('log/server.log', encoding='utf-8'), logging.StreamHandler()],
                    level=logging.INFO)


class Server:
    def __init__(self, port):
        """
        :param
            port: порт сервера
        """
        self.port = port
        self.clients = []
        self.users = 'users.json'
        self.server_run()
        self.status = None

    def server_run(self):
        """
        Запуск сервера
        """
        self.sock = socket.socket()
        self.sock.bind(('', self.port))
        self.sock.listen(5)
        logging.info(f'Сервер запущен! Порт {self.port}.')
        while True:
            conn, addr = self.sock.accept()
            Thread(target=self.listen_client, args=(conn, addr)).start()  # ??? что это?
            logging.info(f"Подключился клиент {addr}")
            self.clients.append(conn)

    def listen_client(self, conn, address):
        """
        Отправка сообщения клиента, либо закрытие соединения
        Args:
            conn (socket): сокет с данными клиента
            address (tuple): ip-адрес и номера соединения
        """
        self.authorization(address, conn)
        while True:
            try:
                data = conn.recv(1024)
            except ConnectionRefusedError:
                conn.close()
                self.clients.remove(conn)
                logging.info(f'Отключение клиента {address}!')
                break

            if data:
                status, data, username = pickle.loads(data)
                logging.info(f"Прием данных от клиента '{username}_{address[1]}': {data}")
                if status == "message":
                    self.broadcast(data, conn, address, username)

            else:
                # Закрываем соединение
                conn.close()
                self.clients.remove(conn)
                logging.info(f"Отключение клиента {address}!")
                break

    def authorization(self, address, conn):
        """
        Авторизация пользователя на сервере
        :param address: IP-адрес и номер соединения
        :param conn: сокет
        """
        try:
            self.users_authorization = self.read_json()
        except json.decoder.JSONDecodeError:
            self.registration(address, conn)

        registration_user = True
        for users in self.users_authorization:
            if address[0] in users:
                for key, value in users.items():
                    if key == address[0]:
                        name_user = value['name']
                        password_user = value['password']
                        # login = input('Введите имя пользователя: ')
                        # password = input('Введите пароль: ')
                        # if check_date
                        conn.send(pickle.dumps(["passwd", "Введите свой пароль: "]))
                        passwd = pickle.loads(conn.recv(1024))[1]
                        conn.send(pickle.dumps(["success", f"Здравствуйте, {name_user}"])) if self.check_password(
                            passwd, password_user) else self.authorization(address, conn)
                        registration_user = False
        if registration_user:
            self.registration(address, conn)

    def broadcast(self, messenger, conn, address, username):
        """
        Отправка данных клиенту (сообщение и имя пользователя с номером соединения)
        :param messenger: сообщение
        :param conn: сокет с данными
        :param address: ip-адрес и номер соединения
        :param username: имя клиента
        """
        username += f"_{address[1]}"
        for sock in self.clients:
            if sock != conn:
                data = pickle.dumps(["message", messenger, username])
                sock.send(data)
                logging.info(f"Отправляем данные клиенту {sock.getsockname()}: {messenger}")

    def read_json(self):
        """Чтение файла с авторизованными пользователями"""
        with (self.users, 'r') as file:
            users_text = json.load(file)
        return users_text

    def registration(self, address, conn):
        """
        Регистрация новых пользователей
        и добавление информации о них в json файл
        Args:
            :param address: IP-адрес и номер соединения
            :param conn: сокет
        """
        conn.send(pickle.dumps(
            ["auth", ""]))
        name = pickle.loads(conn.recv(1024))[1]
        conn.send(pickle.dumps(["passwd", "Введите пароль: "]))
        passwd = self.hash_generation(pickle.loads(conn.recv(1024))[1])
        conn.send(pickle.dumps(["success", f"Приветствую, {name}"]))
        self.users_authorization.append({address[0]: {'name': name, 'password': passwd}})
        self.write_json()
        self.users_authorization = self.read_json()

    def write_json(self):
        """
        Запись пользователей в json-файл
        """
        with open(self.users, 'w', encoding='utf-8') as file:
            json.dump(self.users_authorization, file, indent=4)

    def check_password(self, password, userpassword):
        """
        Проверяем пароль из файла и введенный пользователем
        Args:
            :param password: введенный пароль пользователем
            :param userpassword: пароль пользователя из json
        returns:
            boolean: True/False
        """
        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        return key == userpassword

    def hash_generation(self, password):
        """
        Генерация пароля
        Args:
            password: пароль
        returns:
            str: хэш пароль
        """
        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        return key


def main():
    """
    Проверка корректности порта
    Запуск сервера
    """
    port = 2000
    if not port_validation(port):
        if not free_port(port):
            port_free = False
            while not port_free:
                port += 1
                port_free = free_port(port)
    try:
        server = Server(port)
    except KeyboardInterrupt:
        logging.info('Сервер остановился!')


if __name__ == '__main__':
    main()
