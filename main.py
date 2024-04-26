import math

import numpy as np
import pandas as pd


def get_r(class_of_obj):
    if class_of_obj == 'A':
        x1 = 'A_x1'
        x3 = 'A_x3'
    else:
        x1 = 'B_x1'
        x3 = 'B_x3'
    for i in range(data[x1].size):
        new_point = np.array((data[x1].get(i), data[x3].get(i)))
        r = math.dist(point, new_point)
        if r == 0:
            continue
        groups[r] = class_of_obj


T = 9

excel_data = pd.read_excel('Выборка_лаб6.xlsx', sheet_name='Вар2', keep_default_na=False, header=1)
A_x1 = excel_data['A_x1'].tolist()
A_x3 = excel_data['A_x3'].tolist()
B_x1 = excel_data['B_x1'].tolist()
B_x3 = excel_data['B_x3'].tolist()

data = pd.DataFrame({
    'A_x1': A_x1,
    'A_x3': A_x3,
    'B_x1': B_x1,
    'B_x3': B_x3})

mistakes_A = 0
for n in range(100):
    point = np.array((data['A_x1'].get(n), data['A_x3'].get(n)))
    groups = {}
    get_r('A')
    get_r('B')

    groups_sorted = sorted(groups.items())
    Ta = 0
    Tb = 0
    for i in range(T):
        if groups_sorted[i][1] == 'A':
            Ta += 1
        else:
            Tb += 1
    if Ta < Tb:
        mistakes_A += 1

mistakes_B = 0
for n in range(100):
    point = np.array((data['B_x1'].get(n), data['B_x3'].get(n)))

    groups = {}
    get_r('A')
    get_r('B')
    groups_sorted = sorted(groups.items())
    Ta = 0
    Tb = 0
    for i in range(T):
        if groups_sorted[i][1] == 'A':
            Ta += 1
        else:
            Tb += 1
    if Ta >= Tb:
        mistakes_B += 1

print(f"Колич ошибок A = {mistakes_A}")
print(f"Колич ошибок B = {mistakes_B}")
print(f"Точность правила = {1-(mistakes_A+mistakes_B)/200}")

x1 = excel_data['x1'].tolist()
x3 = excel_data['x3'].tolist()
x1 = list(filter(lambda a: a!='', x1))
x3 = list(filter(lambda a: a!='', x3))
new_data = pd.DataFrame({
    'x1': x1,
    'x3': x3})
result = {}
for n in range(new_data['x1'].size):
    point = np.array((new_data['x1'].get(n), new_data['x3'].get(n)))
    groups = {}
    get_r('A')
    get_r('B')

    groups_sorted = sorted(groups.items())
    Ta = 0
    Tb = 0
    for i in range(T):
        if groups_sorted[i][1] == 'A':
            Ta += 1
        else:
            Tb += 1
    if Ta >= Tb:
        result[n] = 'A'
    else:
        result[n] = 'B'
print("Результаты классификации")
for i in range(len(result)):
    print(f"{i+1}:{result[i]}")