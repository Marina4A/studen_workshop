import socket
import hashlib
import json
import pickle
from threading import Thread
import logging

from validation import is_free_port, port_validation



class Server:
    def __init__(self, port):
        self.port = port

    def server_run(self):
        pass


def main():
    port = 2000
    if not port_validation(port):


if __name__ = '__main__':
    main()