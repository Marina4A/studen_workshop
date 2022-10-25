import socket

sock = socket.socket()
sock.connect(('localhost', 9090))

size = 1024

while True:
    text = input('Введите текст: ')  # Запросили текст
    text = text.encode()  # Преобразовали в бинарный вид
    sock.send(text)  # отправили на сервер

    while True:
        data = sock.recv(size)  # Ждем ответ от сервера
        print('Полученные ответ: ', data.decode())
        if len(data) < size:
            break

    sock.close()
