import multiprocessing as mp
import numpy as np


# функция для вычисления одной строки результирующей матрицы
def calc_row(row_index, matrix1, matrix2, output_file):
    row = []
    for j in range(len(matrix2[0])):
        sum = 0
        for k in range(len(matrix1[0])):
            sum += matrix1[row_index][k] * matrix2[k][j]
        row.append(sum)

    # записываем результаты в файл
    np.savetxt(output_file, [row], fmt='%.2f')


# функция для параллельного вычисления матрицы-произведения
def calc_matrix(matrix1, matrix2, num_processes, output_file):
    pool = mp.Pool(processes=num_processes)

    for i in range(len(matrix1)):
        pool.apply_async(calc_row, args=(i, matrix1, matrix2, output_file))

    # ожидание завершения всех задач в пуле
    pool.close()
    pool.join()


if __name__ == '__main__':
    # определяем количество процессов равное количеству ядер процессора
    num_processes = mp.cpu_count()

    # читаем матрицы из файлов
    matrix1 = np.loadtxt('matrix1.txt')
    matrix2 = np.loadtxt('matrix2.txt')

    # проверяем, можно ли перемножить матрицы
    if matrix1.shape[1] != matrix2.shape[0]:
        print('Matrices cannot be multiplied!')
    else:
        # перемножаем матрицы и записываем результат в файл
        calc_matrix(matrix1, matrix2, num_processes, 'result1.txt')
