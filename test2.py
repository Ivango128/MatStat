import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


def lda_classification(data, target):
    lda = LinearDiscriminantAnalysis()
    lda.fit(data, target)
    return lda, lda.explained_variance_ratio_


def knn_classification(data, target, k):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(data, target)
    return knn


def compare_classifiers(data, target, k=5):
    # Объединение данных
    data_A = pd.DataFrame({'x1': A_x1, 'x2': A_x3})
    data_B = pd.DataFrame({'x1': B_x1, 'x2': B_x3})
    data = pd.concat([data_A, data_B], ignore_index=True)
    target = ['A'] * len(A_x1) + ['B'] * len(B_x1)

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=42)

    # Обучение LDA
    lda_model, lda_variance = lda_classification(X_train, y_train)
    lda_pred = lda_model.predict(X_test)
    lda_accuracy = accuracy_score(y_test, lda_pred)

    # Обучение kNN
    knn_model = knn_classification(X_train, y_train, k)
    knn_pred = knn_model.predict(X_test)
    knn_accuracy = accuracy_score(y_test, knn_pred)

    # Вывод ошибок в консоль
    lda_errors = []
    knn_errors = []
    for i, (true_label, lda_predicted_label, knn_predicted_label) in enumerate(zip(y_test, lda_pred, knn_pred)):
        if true_label != lda_predicted_label:
            lda_errors.append((i, X_test.iloc[i]['x1'], X_test.iloc[i]['x2']))
        if true_label != knn_predicted_label:
            knn_errors.append((i, X_test.iloc[i]['x1'], X_test.iloc[i]['x2']))

    print("LDA errors:")
    for error in lda_errors:
        print(f"Index: {error[0]}, x1: {error[1]}, x2: {error[2]}")

    print("\nkNN errors:")
    for error in knn_errors:
        print(f"Index: {error[0]}, x1: {error[1]}, x2: {error[2]}")

    return lda_accuracy, knn_accuracy, lda_variance


# Загрузка данных из Excel-файла
excel_data = pd.read_excel('Выборка_лаб6.xlsx', sheet_name='Вар2', keep_default_na=False, header=1)
A_x1 = excel_data['A_x1'].tolist()
A_x3 = excel_data['A_x2'].tolist()
B_x1 = excel_data['B_x1'].tolist()
B_x3 = excel_data['B_x2'].tolist()

# Вызов функции для сравнения
lda_accuracy, knn_accuracy, lda_variance = compare_classifiers(pd.DataFrame(), [], k=5)

print(f"LDA accuracy: {lda_accuracy}")
print(f"kNN accuracy: {knn_accuracy}")
print(f"LDA explained variance ratio: {lda_variance}")

# Визуализация результатов
plt.figure(figsize=(12, 5))

# График распределения классов
plt.subplot(1, 2, 1)
plt.scatter(A_x1, A_x3, color='blue', label='Class A')
plt.scatter(B_x1, B_x3, color='red', label='Class B')
plt.title('Class Distribution')
plt.xlabel('X1')
plt.ylabel('X2')
plt.legend()

# График точности и объясненной дисперсии
plt.subplot(1, 2, 2)
plt.scatter(['LDA', 'kNN'], [lda_accuracy, knn_accuracy], s=100, color=['blue', 'green'], label='Accuracy')
plt.scatter(['LDA'], [lda_variance], s=100, color='red', label='Explained Variance Ratio')
plt.title('Comparison of LDA and kNN')
plt.xlabel('Method')
plt.ylabel('Accuracy / Explained Variance Ratio')
plt.legend()
plt.ylim(0, 1)

plt.show()
