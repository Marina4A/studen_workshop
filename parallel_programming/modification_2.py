import multiprocessing as mp
import numpy as np


# функция для вычисления одной строки результирующей матрицы
def calc_row(row_index, matrix1, matrix2):
    row = []
    for j in range(len(matrix2[0])):
        sum = 0
        for k in range(len(matrix1[0])):
            sum += matrix1[row_index][k] * matrix2[k][j]
        row.append(sum)

    return row


# функция для параллельного вычисления матрицы-произведения
def calc_matrix(matrix1, matrix2):
    num_processes = mp.cpu_count()
    results = []

    with mp.Pool(processes=num_processes) as pool:
        for i in range(len(matrix1)):
            result = pool.apply_async(calc_row, args=(i, matrix1, matrix2))
            results.append(result)

        # получаем результаты
        matrix_mult = []
        for result in results:
            matrix_mult.append(result.get())

    return np.array(matrix_mult)


if __name__ == '__main__':
    # читаем матрицы из файлов
    matrix1 = np.loadtxt('matrix1.txt')
    matrix2 = np.loadtxt('matrix2.txt')

    # проверяем, можно ли перемножить матрицы
    if matrix1.shape[1] != matrix2.shape[0]:
        print('Matrices cannot be multiplied!')
    else:
        # перемножаем матрицы
        matrix_mult = calc_matrix(matrix1, matrix2)

        # записываем результат в файл
        np.savetxt('result.txt', matrix_mult, fmt='%.2f')
