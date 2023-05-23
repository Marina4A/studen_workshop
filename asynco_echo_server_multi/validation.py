import asyncio
import socket
import logging


async def port_validation(port: str) -> bool:
    """Проверяется корректность порта"""
    if -1 < int(port) < 65536:
        return await free_port(port)
    logging.info(f"Некорректное значение порта: {port}")
    return False


async def free_port(port: str) -> bool:
    """Проверка свободен ли порт"""
    async with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            await asyncio.wait_for(sock.connect(('localhost', int(port))), timeout=0.1)
            logging.info(f'Порт "{port}" занят!')
            return False
        except (socket.timeout, ConnectionRefusedError):
            # Порт свободен
            return True


async def ip_validation(ip_address: list[str]) -> bool:
    """Проверка корректности IP"""
    if len(ip_address) != 4:
        logging.info(f'IP "{ip_address}" некорректен!')
        return False
    for part in ip_address:
        try:
            if not 0 <= int(part) <= 255:
                raise ValueError
        except ValueError:
            logging.info(f'IP "{ip_address}" некорректен!')
            return False
    logging.info('IP корректен!')
    return True
