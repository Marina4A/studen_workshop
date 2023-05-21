import multiprocessing as mp
import numpy as np
import time


# Функция для генерации случайной квадратной матрицы
def generate_random_square_matrix(size):
    return np.random.rand(size, size)


# Функция для вычисления одной строки результирующей матрицы
def calc_row(row_index, matrix1, matrix2):
    row = []
    for j in range(len(matrix2[0])):
        sum = 0
        for k in range(len(matrix1[0])):
            sum += matrix1[row_index][k] * matrix2[k][j]
        row.append(sum)

    return row


# Функция для параллельного вычисления матрицы-произведения
def calc_matrix(matrix1, matrix2, stop_event=None):
    results = []

    # количество потоков не больше числа строк в первой матрице
    num_worker_threads = matrix1.shape[0]

    with mp.Pool(processes=num_worker_threads) as pool:
        for i in range(len(matrix1)):
            if stop_event and stop_event.is_set():
                break

            result = pool.apply_async(calc_row, args=(i, matrix1, matrix2))
            results.append(result)

        # получаем результаты
        matrix_mult = []
        for result in results:
            matrix_mult.append(result.get())

    return np.array(matrix_mult)


if __name__ == '__main__':
    # размерность квадратных матриц
    size = 500

    # создаём две случайные квадратные матрицы
    matrix1 = generate_random_square_matrix(size)
    matrix2 = generate_random_square_matrix(size)

    # проверяем, можно ли перемножить матрицы
    if matrix1.shape[1] != matrix2.shape[0]:
        print('Matrices cannot be multiplied!')
    else:
        # создаем событие для остановки вычислений
        stop_event = mp.Event()

        # запускаем процесс вычисления матрицы-произведения в отдельном потоке
        process = mp.Process(target=calc_matrix, args=(matrix1, matrix2, stop_event))
        process.start()

        try:
            # выводим сообщение и ждем 3 секунды
            print('Calculating...')
            time.sleep(3)

            # отправляем сигнал остановки процесса вычисления
            stop_event.set()

            # ждем завершения процесса вычисления
            process.join()

            # выводим сообщение об остановке вычислений
            print('Calculation stopped.')
        except KeyboardInterrupt:
            # если пользователь нажал Ctrl+C, отправляем сигнал остановки процесса вычисления
            stop_event.set()
            process.join()
            print('Calculation stopped by user.')
