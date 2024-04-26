import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# Загрузка данных из Excel-файла
excel_data = pd.read_excel('Выборка_лаб6.xlsx', sheet_name='Вар2', keep_default_na=False, header=1)

data = list(zip(excel_data['A_x1'], excel_data['A_x3']))
data += list(zip(excel_data['B_x1'], excel_data['B_x3']))

cel_data=[]
for i in range(1, 201):
    if i <= 100:
        cel_data.append('A')
    else:
        cel_data.append('B')

# Разделение данных на признаки (X) и целевую переменную (y)
X = data
y = cel_data  # Предположим, что 'группа' - это ваша целевая переменная

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Обучение наивного байесовского классификатора
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Оценка качества классификации на тестовом наборе
accuracy = classifier.score(X_test, y_test)
print("Accuracy:", accuracy)

# Вычисление меры существенности для каждой переменной
importance_measure = abs(classifier.theta_[0] - classifier.theta_[1])  # Веса для каждой переменной

# Вывод меры существенности для каждой переменной
y_pred = classifier.predict(X_test)

for i in range(len(y_pred)):
    if y_test[i] != y_pred[i]:
        print(i, 'ошибка', X_test[i])
    #print(y_test[i], y_pred[i])

# # Выбор пары переменных с минимальной мерой существенности
# min_importance_index = importance_measure.argmin()
# min_importance_pair = ['x1', 'x2']  # Используем изначальные названия столбцов
#
# print("Минимальная мера существенности:", importance_measure.min())
# print("Пара переменных с минимальной мерой существенности:", min_importance_pair)