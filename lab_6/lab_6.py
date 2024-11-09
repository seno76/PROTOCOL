import random

def generate_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return "Невозможно создать регулярный граф: произведение n и k должно быть четным"
    if k >= n:
        return "Невозможно создать регулярный граф: степень вершины должна быть меньше числа вершин"
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(1, k // 2 + 1):
            neighbor = (i + j) % n
            graph[i][neighbor] = 1
            graph[neighbor][i] = 1  
    if k % 2 == 1:
        for i in range(n // 2):
            neighbor = (i + n // 2) % n
            graph[i][neighbor] = 1
            graph[neighbor][i] = 1
    return graph

def read_matrix_from_file(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        matrix = [list(map(int, line.split())) for line in f]
    return matrix

def write_matrix_to_file(matrix, filename):
    with open(filename, 'w', encoding="UTF-8") as f:
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

def generate_permutation(matrix_size, p=None):
    permutation = list(range(matrix_size))
    random.shuffle(permutation)
    while p is not None and permutation == p:
        random.shuffle(permutation)
    return permutation

def write_permutation_to_file(permutation, filename):
    with open(filename, 'w', encoding="UTF-8") as file:
        file.write(' '.join(map(str, permutation)) + '\n')

def read_permutation_from_file(filename):
    with open(filename, 'r', encoding="UTF-8") as file:
        return list(map(int, file.readline().split()))

def apply_permutation(matrix, permutation):
    return [[matrix[i][j] for j in permutation] for i in permutation]

def mix_permutation(permutation_1, permutation_2):
    return [permutation_2[i] for i in permutation_1]

def write_bit_to_file(bit, filename="challenge.txt"):
    with open(filename, 'w', encoding="UTF-8") as file:
        file.write(str(bit))

def read_bit_from_file(filename="challenge.txt"):
    with open(filename, 'r', encoding="UTF-8") as file:
        return int(file.read().strip())

def print_graph(matrix):
    for row in matrix:
        print(" ".join(f"{val:2}" for val in row))

def main():
    while True:
        print("\n1. Пегги создает графы G1, G2 и H")
        print("2. Виктор выбирает граф для проверки")
        print("3. Пегги отвечает на запрос Виктора")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            # Шаг 1: Генерация графа и перестановок
            n = int(input("Укажите количество вершин графа: "))
            degree = int(input("Укажите степени вершин у графа: "))
            G1 = generate_regular_graph(n, degree)
            write_matrix_to_file(G1, "G1.txt")
            
            # Генерация изоморфного графа G2
            secret_permutation = generate_permutation(len(G1))
            write_permutation_to_file(secret_permutation, "secret_permutation.txt")
            G2 = apply_permutation(G1, secret_permutation)
            write_matrix_to_file(G2, "G2.txt")

            # Создание графа H, случайной перестановкой G2
            h_permutation = generate_permutation(len(G1))
            write_permutation_to_file(h_permutation, "permutation.txt")
            H = apply_permutation(G2, h_permutation)
            write_matrix_to_file(H, "H.txt")
            print("Графы G1, G2 и H созданы и записаны в файлы.")

        elif choice == "2":
            # Шаг 2: Виктор выбирает случайный бит и записывает его в файл
            bit = random.randint(0, 1)
            write_bit_to_file(bit)
            print(f"Виктор выбрал граф для проверки: {'G1' if bit == 0 else 'G2'}.")

        elif choice == "3":
            # Шаг 3: Пегги отвечает на запрос Виктора, проверяя изоморфизм
            try:
                bit = read_bit_from_file()
                H = read_matrix_from_file("H.txt")
                print("Граф H: ")
                print_graph(H)

                if bit == 1:
                    # Проверка изоморфизма с графом G2
                    G2 = read_matrix_from_file("G2.txt")
                    print("Граф G2: ")
                    print_graph(G2)

                    h_permutation = read_permutation_from_file("permutation.txt")
                    new_G2 = apply_permutation(G2, h_permutation)
                    print("Перестановка графа G2: ", h_permutation)
                    print_graph(new_G2)

                    if H == new_G2:
                        print("РЕЗУЛЬТАТ: Изоморфизм доказан для G2 и H.")
                    else:
                        print("РЕЗУЛЬТАТ: Изоморфизм не доказан для G2 и H.")
                else:
                    # Проверка изоморфизма с графом G1
                    G1 = read_matrix_from_file("G1.txt")
                    secret_permutation = read_permutation_from_file("secret_permutation.txt")
                    h_permutation = read_permutation_from_file("permutation.txt")
                    combined_permutation = mix_permutation(h_permutation, secret_permutation)
                    new_G1 = apply_permutation(G1, combined_permutation)
                    print("Перестановка графа G1: ", combined_permutation)
                    print_graph(new_G1)

                    if H == new_G1:
                        print("РЕЗУЛЬТАТ: Изоморфизм доказан для G1 и H.")
                    else:
                        print("РЕЗУЛЬТАТ: Изоморфизм не доказан для G1 и H.")
            except FileNotFoundError:
                print("Ошибка: Сначала необходимо выполнить шаги 1 и 2.")
            except ValueError:
                print("Ошибка: некорректный формат файла 'challenge.txt'.")

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите корректный номер действия.")

main()