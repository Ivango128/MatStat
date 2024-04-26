import math
import warnings

from scipy.stats import norm


import pandas as pd


def read_excel_data(file_path, sheet_name, start_row, end_row, cell_column):
    try:
        # Считываем данные из Excel-файла
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Отфильтровываем строки от start_row до end_row и столбец cell_column
        selected_data = [df.iloc[start_row - 1 : end_row, cell_column - 1]]

        # Выводим результат
        # print(selected_data)

        # Возвращаем список считанных чисел
        return selected_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


class A:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.N = 100
        self.L_x1_x2 = []
        self.L_x1_x3 = []
        self.L_x2_x3 = []
        self.N1 = 0

        # данные класса A
        self.x1_m = 2.027751
        self.x1_std = 0.383061

        self.x2_m = 1.142772
        self.x2_std = 1.065543

        self.x3_m = 0.890612
        self.x3_std = 0.771065


class B:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.N = 100
        self.L_x1_x2 = []
        self.L_x1_x3 = []
        self.L_x2_x3 = []

        self.N1 = 0

        self.x1_m = 2.011010
        self.x1_std = 0.403314

        self.x2_m = 4.679260
        self.x2_std = 4.007921

        #self.x3_lambda = 1 / 5.70125635


def get_number_of_error(input_list, isA=False):
    count = 0
    for value in input_list:
        if value >= 1:
            count += 1

    if isA:
        return 100 - count
    else:
        return count


def get_p_by_normal_distr(x, m, std):
    """
    Вычисляет значение функции плотности распределения для нормального закона.

    Параметры:
    - x: значение случайной переменной, для которой нужно вычислить PDF.
    - mean: среднее значение (математическое ожидание) нормального распределения.
    - std_dev: стандартное отклонение нормального распределения.

    Возвращает:
    - Значение PDF в точке x.
    """

    return norm.pdf(x, loc=m, scale=std)


def get_p_by_exponential_distr(x, scale_param):
    """
    Вычисляет значение функции плотности распределения для экспоненциального закона.

    Параметры:
    - x: значение случайной переменной, для которой нужно вычислить PDF.
    - scale_param: параметр масштаба (инверсия интенсивности) экспоненциального распределения.

    Возвращает:
    - Значение PDF в точке x.
    """
    if x < 0:
        return 0

    return scale_param * math.exp(-scale_param * x)


P_a = 0.5
P_b = 0.5

file_path = "Выборка_лаб6.xlsx"
sheet_name = "Вар2"
start_row = 3  # начальная строка для чтения
end_row = 102  # конечная строка для чтения
cell_column = [1, 2, 3, 5, 6, 7, 9, 10, 11]  # столбец для чтения

a_class = A(
    x1=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[0]),
    x2=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[1]),
    x3=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[2]),
)

b_class = B(
    x1=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[3]),
    x2=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[4]),
    x3=read_excel_data(file_path, sheet_name, start_row, end_row, cell_column[5]),
)

for i in range(0, len(a_class.x1)):
    # в классе B x1 - экпон
    with warnings.catch_warnings():
        warnings.filterwarnings("error")

        # x1 x2
        try:
            a_class.L_x1_x2.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], a_class.x1_m, a_class.x1_std
                        )
                    )
                    * (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x2[i], a_class.x2_m, a_class.x2_std
                        )
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], b_class.x1_m, b_class.x1_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_normal_distr(
                            a_class.x2[i], b_class.x2_m, b_class.x2_std
                        )
                    )
                )
            )
        except Exception:
            a_class.L_x1_x2.append(1)

        try:
            b_class.L_x1_x2.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            b_class.x1[i], a_class.x1_m, a_class.x1_std
                        )
                    )
                    * (
                        P_a
                        * get_p_by_normal_distr(
                            b_class.x2[i], a_class.x2_m, a_class.x2_std
                        )
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], b_class.x1_m, b_class.x1_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_normal_distr(
                            b_class.x2[i], b_class.x2_m, b_class.x2_std
                        )
                    )
                )
            )
        except Exception:
            b_class.L_x1_x2.append(1)

        # x1 x3
        try:
            a_class.L_x1_x3.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], a_class.x1_m, a_class.x1_std
                        )
                    )
                    * (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x3[i], a_class.x3_m, a_class.x3_std
                        )
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], b_class.x1_m, b_class.x1_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
            )
        except Exception:
            a_class.L_x1_x3.append(1)

        try:
            b_class.L_x1_x3.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            b_class.x1[i], a_class.x1_m, a_class.x1_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x1[i], b_class.x1_m, b_class.x1_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
            )
        except Exception:
            b_class.L_x1_x3.append(1)

        # x2 x3
        try:
            a_class.L_x2_x3.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x2[i], a_class.x2_m, a_class.x2_std
                        )
                    )
                    * (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x3[i], a_class.x3_m, a_class.x3_std
                        )
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            a_class.x2[i], b_class.x2_m, b_class.x2_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
            )
        except Exception:
            a_class.L_x2_x3.append(1)

        try:
            b_class.L_x2_x3.append(
                (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            b_class.x2[i], a_class.x2_m, a_class.x2_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
                / (
                    (
                        P_a
                        * get_p_by_normal_distr(
                            b_class.x2[i], b_class.x2_m, b_class.x2_std
                        )
                    )
                    * (
                        P_b
                        * get_p_by_exponential_distr(b_class.x3[i], b_class.x3_lambda)
                    )
                )
            )
        except Exception:
            b_class.L_x2_x3.append(1)

U = []
U.append(
    0.5 * get_number_of_error(a_class.L_x1_x2, True) / 100
    + 0.5 * get_number_of_error(b_class.L_x1_x2) / 100
)
U.append(
    0.5 * get_number_of_error(a_class.L_x1_x3, True) / 100
    + 0.5 * get_number_of_error(b_class.L_x1_x3) / 100
)
U.append(
    0.5 * get_number_of_error(a_class.L_x2_x3, True) / 100
    + 0.5 * get_number_of_error(b_class.L_x2_x3) / 100
)

print("U=", U)
print("min U=", min(U))


x2 = read_excel_data(file_path, sheet_name, start_row, 12, cell_column[7])
x3 = read_excel_data(file_path, sheet_name, start_row, 12, cell_column[8])


print("Классификация тестовой выборки:")
for i in range(0, len(x2)):
    with warnings.catch_warnings():
        warnings.filterwarnings("error")

        try:
            L = (
                (P_a * get_p_by_normal_distr(x2[i], a_class.x2_m, a_class.x2_std))
                * (P_a * get_p_by_normal_distr(x3[i], a_class.x3_m, a_class.x3_std))
            ) / (
                (P_b * get_p_by_normal_distr(x2[i], b_class.x2_m, b_class.x2_std))
                * (P_b * get_p_by_exponential_distr(x3[i], b_class.x3_lambda))
            )


        except Exception:
            L = 1
        finally:
            if L >= 1:
                print("Точка(x2;x3) = (", x3[i], ";", x2[i], ")", "    Класс A\n")
                #print("L=", L,"    Класс A\n")
            else:
                print("Точка(x2;x3) = (", x3[i], ";", x2[i], ")", "    Класс B\n")
                #print("L=", L,"     Класс B\n")

print(
    "Точность параметрического метода:",
    (
        1
        - (
            get_number_of_error(a_class.L_x2_x3, True)
            + get_number_of_error(b_class.L_x2_x3)
        )
        / 200
    ),
)
