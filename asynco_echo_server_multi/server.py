import asyncio
import queue
import socket
import hashlib
import json
import pickle
import logging

from validation import free_port, port_validation

logging.basicConfig(
    format='%(asctime)s {%(levelname)s %(funcName)s: %(message)s}',
    handlers=[
        logging.FileHandler('log/server.log', encoding='utf-8'),
        logging.StreamHandler()
    ],
    level=logging.INFO
)


class Server:
    def __init__(self, ip, port):
        """
        :param port: Port number
        """
        self.port = port
        self.users_authorization = {}
        self.clients = {}
        self.users = 'users.json'
        self.status = None
        self.ip = ip
        self.loop = asyncio.get_event_loop()
        self.queue = queue.Queue()
        self.server_task = self.loop.create_task(self.server_run())
        self.messages_task = self.loop.create_task(self.process_messages())

    async def server_run(self):
        """
        Start the server
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(5)
        self.sock = sock
        logging.info(f'Server started! Port {self.port}.')
        while True:
            conn, addr = await self.sock.accept()
            logging.info(f"Client connected: {addr}")
            self.clients[conn] = addr
            self.loop.create_task(self.listen_client(conn))

    async def listen_client(self, conn):
        """
        Send message to client, or close connection
        Args:
            conn (socket): socket with client data
        """
        address = self.clients[conn]
        await self.authorization(address, conn)
        try:
            while True:
                data = await self.loop.sock_recv(conn, 1024)
                if not data:
                    break

                status, message, username = json.loads(data.decode('utf-8'))
                logging.info(f"Message from '{username}_{address[1]}': {message}")
                await self.broadcast(message, conn, username)

            # Close the connection
            conn.close()
            del self.clients[conn]
            logging.info(f"Client disconnected: {address}!")
        except ConnectionResetError:
            conn.close()
            del self.clients[conn]
            logging.warning(f"Client unexpectedly disconnected: {address}!")

    async def authorization(self, address, conn):
        """
        Authorize the user on the server
        :param address: IP address and connection number
        :param conn: Socket object
        """

        name_user = None

        try:
            self.users_authorization = await self.read_json()
            if address[0] in self.users_authorization:
                await conn.sendall(json.dumps(["passwd", "Enter your username"]).encode('utf-8'))
                name_user = json.loads(await conn.recv(1024).decode('utf-8'))[1]
                for user in self.users_authorization[address[0]]:
                    if await self.check_name(user['name'], name_user):
                        logging.info(f'User {name_user} found')
                    else:
                        raise ValueError
                    while True:
                        await conn.sendall(json.dumps(["passwd", "Enter your password"]).encode('utf-8'))
                        passwd = json.loads(await conn.recv(1024).decode('utf-8'))[1]

                        if self.check_password(passwd, user['password']):
                            logging.info(f'Password "{passwd}" is correct!')
                            await conn.sendall(json.dumps(["success", f"Welcome, {name_user}"]).encode('utf-8'))

                            break
                        else:
                            await conn.sendall(json.dumps(["passwd", "Incorrect password"]).encode('utf-8'))
                else:
                    raise ValueError
            else:
                raise ValueError
        except (json.decoder.JSONDecodeError, ValueError):
            self.registration(address, conn, name_user)

    async def broadcast(self, message, conn, username):
        """
        Send data to client (message and user name with connection number)
        :param messenger: message
        :param conn: socket with data
        :param username: client name
        """
        address = self.clients[conn]
        username += f"_{address[1]}"
        for sock, addr in self.clients.items():
            if sock == conn:
                continue
            data = json.dumps(["message", message, username]).encode('utf-8')
            await sock.sendall(data)
            logging.info(f"Sending data to {address}: {message}")

    async def read_json(self):
        """Read the file with authorized users"""
        async with aiofiles.open(self.users, 'r', encoding='utf-8') as file:
            users_text = await file.read()
        return json.loads(users_text)

    async def registration(self, address, conn, name):
        """
        Register new users and add information about them to the json file
        Args:
            :param address: IP address and connection number
            :param conn: socket
        """
        await conn.sendall(pickle.dumps(["passwd", "Register a new user"]))
        if name is None:
            await conn.sendall(pickle.dumps(["name", "Enter your username"]))
            name = pickle.loads(await conn.recv(1024))[1]
        await conn.sendall(pickle.dumps(["password", "Enter your password"]))
        password = self.hash_generation(pickle.loads(await conn.recv(1024))[1])
        await conn.sendall(pickle.dumps(["success", f"Welcome, {name}"]))

        if address[0] in self.users_authorization:
            self.users_authorization[address[0]].append({'name': name, 'password': password})
        else:
            self.users_authorization[address[0]] = [{'name': name, 'password': password}]

        await self.write_json()
        self.users_authorization = await self.read_json()

    async def write_json(self):
        """
        Write users to json file
        """
        async with aiofiles.open(self.users, mode='w', encoding='utf-8') as file:
            await file.write(json.dumps(self.users_authorization, indent=4))

    def check_password(self, password, userpassword):
        """
        Check the password from the file and the one entered by the user
        Args:
            :param password: password entered by the user
            :param userpassword: user password from json
        returns:
            boolean: True/False
        """
        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        return key == userpassword

    async def check_name(self, name, username):
        """
        Compare the login from json to the one entered by the user
        :param name: data from json file
        :param username: user-entered login
        :return:
            boolean: True/False
        """
        return name == username

    async def hash_generation(self, password):
        """
        Generate a password
        Args:
            password: password
        returns:
            str: password hash
        """

        key = hashlib.md5(password.encode() + b'salt').hexdigest()
        return key


async def main():
    """
    Check port validity
    Start the server
    """
    port = "2002"
    IP = "127.0.0.1"
    if not await port_validation(port):
        if not await free_port(port):
            port_free = False
            while not port_free:
                port += 1
                port_free = await free_port(port)
    try:
        server = Server(IP, port)
    except KeyboardInterrupt:
        logging.info('Server stopped!')
    finally:
        await server.server_task
        await server.messages_task


if __name__ == '__main__':
    asyncio.run(main())



# import asyncio
# import queue
# import socket
# import hashlib
# import json
# import pickle
# from threading import Thread
# import logging
# from time import sleep
#
# from validation import free_port, port_validation
#
# logging.basicConfig(format='%(asctime)s {%(levelname)s %(funcName)s: %(message)s}',
#                     handlers=[logging.FileHandler('log/server.log', encoding='utf-8'), logging.StreamHandler()],
#                     level=logging.INFO)
#
#
# class Server:
#     def __init__(self, ip, port):
#         """
#         :param port: Порт сервера
#         """
#         self.port = port
#         self.users_authorization = []
#         self.clients = []
#         self.users = 'users.json'
#         self.status = None
#         self.ip = ip
#         self.loop = asyncio.get_event_loop()
#         self.queue = queue.Queue()
#         self.loop.create_task(self.server_run())
#         self.loop.create_task(self.process_messages())
#
#     async def server_run(self):
#         """
#         Запуск сервера
#         """
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.bind((self.ip, self.port))
#         sock.listen(5)
#         self.sock = sock
#         logging.info(f'Сервер запущен! Порт {self.port}.')
#         while True:
#             conn, addr = await self.sock.accept()
#             logging.info(f"Подключился клиент {addr}")
#             self.clients.append(conn)
#             self.loop.create_task(self.listen_client(conn, addr))
#
#     async def listen_client(self, conn, address):
#         """
#         Отправка сообщения клиента, либо закрытие соединения
#         Args:
#             conn (socket): сокет с данными клиента
#             address (tuple): ip-адрес и номера соединения
#         """
#         self.authorization(address, conn)
#         while True:
#             try:
#                 data = await self.loop.sock_recv(conn, 1024)
#             except ConnectionRefusedError:
#                 conn.close()
#                 self.clients.remove(conn)
#                 logging.info(f'Отключение клиента {address}!')
#                 break
#
#             if data:
#                 status, message, username = json.loads(data.decode('utf-8'))
#                 logging.info(f"Получено сообщение от клиента '{username}_{address[1]}': {message}")
#                 self.broadcast(message, conn, address, username)
#
#             else:
#                 # Закрываем соединение
#                 conn.close()
#                 self.clients.remove(conn)
#                 logging.info(f"Отключение клиента {address}!")
#                 break
#
#     async def authorization(self, address, conn):
#         """
#         Авторизация пользователя на сервере
#         :param address: IP-адрес и номер соединения
#         :param conn: сокет
#         """
#
#         name_user = None
#
#         try:
#             self.users_authorization = self.read_json()
#             print(f'{self.users_authorization=}')
#             for values in self.users_authorization:
#                 print(f'{values=}')
#                 if address[0] in values:
#                     await conn.sendall(json.dumps(["passwd", "запрашивает имя"]).encode('utf-8'))
#                     name_user = json.loads(await conn.recv(1024).decode('utf-8'))[1]
#                     for user in values[address[0]]:
#                         if self.check_name(user['name'], name_user):
#                             print(f'Пользователь {name_user} найден')
#                         else:
#                             raise ValueError
#                         while True:
#                             await conn.sendall(json.dumps(["passwd", "запрашивает пароль"]).encode('utf-8'))
#                             passwd = json.loads(await conn.recv(1024).decode('utf-8'))[1]
#
#                             if self.check_password(passwd, user['password']):
#                                 print('Пароль верный')
#                                 logging.info(f'Пароль "{passwd}" верный!')
#                                 await conn.sendall(json.dumps(["success", f"Приветствую, {name_user}"]).encode('utf-8'))
#
#                                 break
#                             else:
#                                 await conn.sendall(json.dumps(["passwd", "пароль не верный"]).encode('utf-8'))
#                 else:
#                     raise ValueError
#         except (json.decoder.JSONDecodeError, ValueError):
#             self.registration(address, conn, name_user)
#
#     async def broadcast(self, messenger, conn, address, username):
#         """
#         Отправка данных клиенту (сообщение и имя пользователя с номером соединения)
#         :param messenger: сообщение
#         :param conn: сокет с данными
#         :param address: ip-адрес и номер соединения
#         :param username: имя клиента
#         """
#         username += f"_{address[1]}"
#         for sock in self.clients:
#             if sock == conn:
#                 data = json.dumps(["message", messenger, username]).encode('utf-8')
#                 await sock.sendall(data)
#                 logging.info(f"Отправляем данные клиенту {sock.getsockname()}: {messenger}")
#
#     async def read_json(self):
#         """Чтение файла с авторизованными пользователями"""
#         async with open(self.users, 'r', encoding='utf-8') as file:
#             users_text = await file.read()
#         return json.loads(users_text)
#
#     async def registration(self, address, conn, name):
#         """
#         Регистрация новых пользователей
#         и добавление информации о них в json файл
#         Args:
#             :param address: IP-адрес и номер соединения
#             :param conn: сокет
#         """
#         await conn.sendall(pickle.dumps(["passwd", "Регистрация нового пользователя"]))
#         if name is None:
#             await conn.sendall(pickle.dumps(["name", "запрашивает имя"]))
#             name = pickle.loads(await conn.recv(1024))[1]
#         await conn.sendall(pickle.dumps(["password", "запрашивает пароль"]))
#         password = self.hash_generation(pickle.loads(await conn.recv(1024))[1])
#         await conn.sendall(pickle.dumps(["success", f"Приветствую, {name}"]))
#         print(address, name, password)
#         for index, addr in enumerate(self.users_authorization):
#             if addr == address[0]:
#                 self.users_authorization[index].append([{'name': name, 'password': password}])
#                 break
#         else:
#             self.users_authorization.append({address[0]: [{'name': name, 'password': password}]})
#
#         await self.write_json()
#         self.users_authorization = await self.read_json()
#
#     async def write_json(self):
#         """
#         Запись пользователей в json-файл
#         """
#         async with aiofiles.open(self.users, mode='w', encoding='utf-8') as file:
#             await file.write(json.dumps(self.users_authorization, indent=4))
#
#     def check_password(self, password, userpassword):
#         """
#         Проверяем пароль из файла и введенный пользователем
#         Args:
#             :param password: введенный пароль пользователем
#             :param userpassword: пароль пользователя из json
#         returns:
#             boolean: True/False
#         """
#         key = hashlib.md5(password.encode() + b'salt').hexdigest()
#         print(key, userpassword)
#         return key == userpassword
#
#     async def check_name(self, name, username):
#         """
#         Сравниваем логин из json с введенным пользователем
#         :param name: данные из json-файла
#         :param username: введенный логин пользователем
#         :return:
#             boolean: True/False
#         """
#         return name == username
#
#     async def hash_generation(self, password):
#         """
#         Генерация пароля
#         Args:
#             password: пароль
#         returns:
#             str: хэш пароль
#         """
#
#         key = hashlib.md5(password.encode() + b'salt').hexdigest()
#         return key
#
#
# async def main():
#     """
#     Проверка корректности порта
#     Запуск сервера
#     """
#     port = 2002
#     IP = "127.0.0.1"
#     if not await port_validation(port):
#         if not await free_port(port):
#             port_free = False
#             while not port_free:
#                 port += 1
#                 port_free = await free_port(port)
#     try:
#         server = Server(IP, port)
#         await server.start()
#     except KeyboardInterrupt:
#         logging.info('Сервер остановился!')
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
