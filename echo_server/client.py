import socket
import logging
from threading import Thread
import sys
import pickle
from validation import ip_validation, port_validation
from getpass import getpass
from time import sleep

logging.basicConfig(filename='log/client.log', encoding='utf-8',
                    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s", level=logging.INFO)


class Client:
    """
    Клиент
    """

    def __init__(self, server_ip, port):
        """
        Args:
            server_ip (str): localhost/ip-адресс сервера
            port (int): порт сервера
        """
        self.sock = None
        self.server_ip = server_ip
        self.port = port
        self.message = ''
        self.server_connection()
        self.message_receiving()

    def server_connection(self):
        """Соединение клиента с сервером"""
        self.sock = socket.socket()
        self.sock.setblocking(1)
        try:
            self.sock.connect((self.server_ip, self.port))
        except ConnectionRefusedError:
            print(f"Не удалось присоединиться к серверу {self.server_ip, self.port}")
            sys.exit(0)
        finally:
            logging.info(
                f"Установлено соединение {self.sock.getsockname()} с сервером ('{self.server_ip}', {self.port})")

    def message_receiving(self):
        """Ввод сообщения, проверка на exit для выхода"""
        Thread(target=self.data_acquisition).start()
        print('Чтобы разорвать соединение введите "exit".')
        self.username = input(f"Введите имя:")
        # password = input('Введите пароль:')
        self.send_password()
        self.send_name()
        self.welcome()
        while self.message != 'finish':
            while True:
                self.message = input('Введите сообщение:')
                if self.message.lower() == 'exit':
                    logging.info(f"Разрыв соединения {self.sock.getsockname()} с сервером!")
                    break
                send_message = pickle.dumps(['message', self.message, self.username])
                self.sock.send(send_message)
                logging.info(f"Отправка данных от {self.sock.getsockname()} на сервер: {self.message}")
        self.sock.close()

    def send_password(self):
        """Отправка пароля на сервер"""
        password = getpass(self.data)
        self.sock.send(pickle.dumps(['password', password]))
        sleep(1.5)

    def send_name(self):
        """Отправка имени на сервер"""
        self.sock.send(pickle.dumps(["name", self.username]))
        sleep(1.5)

    def welcome(self):
        """Приветственное сообщение"""
        print(self.data)
        self.username = self.data.split(" ")[1]
        logging.info(f"Клиент {self.sock.getsockname()} прошел авторизацию!")

    def data_acquisition(self):
        """Получение данных от клиента"""
        while True:
            try:
                self.data = self.sock.recv(1024)
                if not self.data:
                    sys.exit(0)
                print(f"\n{pickle.loads(self.data)[2]} -->", pickle.loads(self.data)[1])
                logging.info(f"Клиент {self.sock.getsockname()} принял данные от сервера: {pickle.loads(self.data)[1]}")
            except OSError:
                break


def main():
    """
    Ввод порта и ip сервера, валидация данных
    """
    IP_DEFAULT = "127.0.0.1"
    PORT_DEFAULT = 1025

    user_ip = input("Введите ip сервера (enter для значения по умолчанию):")
    if not ip_validation(user_ip):
        user_ip = IP_DEFAULT
        print(f"Установили ip-адресс {user_ip} по умолчанию!")

    user_port = input("Введите порт (enter для значения по умолчанию):")
    if not port_validation(user_port):
        user_port = PORT_DEFAULT
        print(f"Установили порт {user_port} по умолчанию!")

    Client(user_ip, user_port)


if __name__ == "__main__":
    main()
