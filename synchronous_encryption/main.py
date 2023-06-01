import os

#from Crypto.Cipher import AES

### Функция шифрования и дешифрования текста обобщенным шифром Цезаря

def caesar_cipher(text, shift, decrypt):
    """
    Функция, реализующая шифрование и дешифрование текста обобщенным шифром Цезаря

    :param text: исходный текст
    :param shift: сдвиг (отрицательное значение для шифрования влево)
    :param decrypt: флаг, указывающий нужно ли дешифровать текст (по умолчанию False - шифрование)
    :return: зашифрованный или расшифрованный текст
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)

    if decrypt == "True":
        shift *= -1

    return text.translate(table)


### Функция шифрования и дешифрования шифра Вернама
def vernam_cipher(message, key):
    """
    Функция для шифрования текста шифром Вернама

    :param message: исходное сообщение
    :param key: ключ (случайная последовательность битов той же длины, что и сообщение)
    :return: зашифрованный текст
    """
    cipher = ''
    for m, k in zip(message, key):
        cipher += chr(ord(m) ^ ord(k))
    return cipher


### Алгоритм шифрования OTP (one time pad)

def otp_cipher(message):
    """
    Функция для шифрования/дешифрования текста с помощью OTP

    :param message: исходное сообщение
    :return: зашифрованный или расшифрованный текст
    """
    key = os.urandom(len(message))  # генерируем ключ случайной длины
    cipher = vernam_cipher(message, key)  # шифруем сообщение с помощью ключа
    return cipher


### Алгоритм цепочки блоков (Cipher block chaining)
def cbc_cipher(message, key, iv):
    choose = input("Вы хотите:\n1. Зашифровать. \n2. Шифровать \nВведите число: ")
    if choose:
        return cbc_encrypt(message, key, iv)
    else:
        return cbc_decrypt(message, key, iv)


def cbc_encrypt(message, key, iv):
    """
    Функция шифрования текста с помощью алгоритма цепочки блоков (Cipher block chaining)

    :param message: исходное сообщение
    :param key: ключ шифрования
    :param iv: вектор инициализации
    :return: зашифрованный текст
    """
    cipher = ''
    previous_block = iv

    # дополняем сообщение до кратности длине ключа
    message += ' ' * ((len(key) - len(message)) % len(key))

    # разбиваем сообщение на блоки и шифруем каждый блок
    for i in range(0, len(message), len(key)):
        block = message[i:i + len(key)]
        xored_block = ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(block, previous_block))
        encrypted_block = vernam_cipher(xored_block, key)
        cipher += encrypted_block
        previous_block = encrypted_block

    return cipher


def cbc_decrypt(ciphertext, key, iv):
    """
    Функция расшифрования текста, зашифрованного с помощью алгоритма цепочки блоков (Cipher block chaining)

    :param ciphertext: зашифрованный текст
    :param key: ключ расшифрования
    :param iv: вектор инициализации
    :return: расшифрованный текст
    """
    message = ''
    previous_block = iv

    # разбиваем сообщение на блоки и дешифруем каждый блок
    for i in range(0, len(ciphertext), len(key)):
        block = ciphertext[i:i + len(key)]
        decrypted_block = vernam_cipher(block, key)
        xored_block = ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(decrypted_block, previous_block))
        message += xored_block
        previous_block = block

    return message.rstrip()  # удаляем дополнительные символы пробелов


def func_main(name_cipher=''):
    while name_cipher != 'выход':
        # cipher_choice = {1: caesar_cipher, 2: vernam_cipher, 3: otp_cipher, 4: cbc_cipher}
        print("Меню:\n1.Шифр Цезаря \n2.Шифр Вернама \n3.Шифрование OTP \n4.Алгоритм цепочки блоков ")
        name_cipher = input("Выберите шифр (введите цифру): ")
        ciphertext = input("Введите текст: ")
        if name_cipher == '1':
            shift = int(input("Введите сдвиг(отрицательное значение для шифрования влево)"))
            decrypt = input("Флаг,указывающий нужно ли дешифровать текст (False/True): ")
            print(caesar_cipher(ciphertext, shift, decrypt))
        elif name_cipher == '2':
            key = input("Ключ (случайная последовательность битов той же длины, что и сообщение): ")
            print(vernam_cipher(ciphertext, key))
        elif name_cipher == '3':
            print(otp_cipher(ciphertext))
        elif name_cipher == '4':
            key = input("Введите ключ: ")
            iv = input("Вектор инициализации: ")
            print(cbc_cipher(ciphertext, key, iv))
        else:
            print("Ошибка ввода, попробуйте еще раз!")

        # print(cipher_choice[name_cipher](ciphertext, key, iv))


if __name__ == "__main__":
    func_main()
