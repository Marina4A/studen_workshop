import socket
import logging


def port_validation(port):
    """Проверяется корректность порта"""
    if -1 < port < 65536:
        return free_port(port)
    logging.info("Некорректное значение порта!")
    return False


def free_port(port):
    """Проверка свободен ли порт"""
    try:
        sock = socket.socket()
        sock.bind(("", port))
        sock.close()
        return True
    except OSError:
        logging.info(f'Порт "{port}" занят!')
        return False


def ip_validation(ip_adress):
    """Проверка корректности IP"""
    if func_len(ip_adress) and func_num(ip_adress) and interval_ip(ip_adress):
        logging.info('IP корректен!')
        return True
    logging.info(f'IP "{ip_adress}" некорректен!')
    return False


def func_num(ip_adress):
    """Проверка, что все элементы IP являются целыми числами"""
    ls = [x for x in ip_adress if not x.isdigit()]
    if len(ls) == 0:
        return True
    logging.info(f'{" ".join(ls)} - не целое число')
    return False


def interval_ip(ip_adress):
    """
    Проверка, что все элементы IP находятся
    в диапазоне от 0 до 255
    """
    ls = [ip for ip in ip_adress if not -1 < int(ip) < 256]
    if len(ls) == 0:
        return True
    logging.info(f'{" ".join(ls)} не выходит(ят) в диапазон от 0 до 255')
    return False


def func_len(ip_adress):
    """
    Проверка, что IP состоит
    из четырех элементов, разделенные
    точкой
    """
    if len(ip_adress) == 4:
        return True
    logging.info(f'Адрес - это четыре числа, разделенные точками.')
    return False
