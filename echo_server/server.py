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
                        # дописать
                        registration_user = False
        if registration_user:
            self.registration(address, conn)

    def broadcast(self):
        pass

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
        pass

    def write_json(self):
        """
        Запись пользователей в json-файл
        """
        with open(self.users, 'w', encoding='utf-8') as file:
            json.dump(self.users_authorization, file, indent=4)


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
