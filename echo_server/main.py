import asyncore
import socket


class EchoServer(asyncore.dispatcher):
    pass


if __name__ == '__main__':
    echo_server = EchoServer()
