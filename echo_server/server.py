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
                pass



    def authorization(self, address, conn):
        pass


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
