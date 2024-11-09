import random
from sympy import isprime, mod_inverse, gcd
import hashlib

# Шаг 1: Вычисление значения J из файла
def compute_j_from_file(filename):
    with open(filename, "rb") as f:
        file_data = f.read()
    hash_object = hashlib.sha256(file_data)
    J = int(hash_object.hexdigest(), 16)
    with open("J_value.txt", "w") as f:
        f.write(str(J))
    return J

# Шаг 2: Выбор случайных простых чисел p и q, вычисление n
def generate_primes(bit):
    p = random_prime(2 ** (bit - 1), 2 ** (bit))
    q = random_prime(2 ** (bit - 1), 2 ** (bit))
    n = p * q
    with open("n_value.txt", "w") as f:
        f.write(f"{n}\n{p}\n{q}")
    return n, p, q

# Шаг 3: Вычисление функции Эйлера φ(n)
def compute_euler_totient(n, p, q):
    phi_n = (p - 1) * (q - 1)
    with open("phi_value.txt", "w") as f:
        f.write(str(phi_n))
    return phi_n

# Шаг 4: Выбор числа e и вычисление обратного элемента s
def choose_e_and_compute_s(phi_n):
    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    s = mod_inverse(e, phi_n)
    with open("e_s_values.txt", "w") as f:
        f.write(f"{e}\n{s}")
    return e, s

# Шаг 5: Вычисление закрытого ключа x
def compute_private_key(J, s, n):
    x = pow(J, -s, n)
    with open("private_key.txt", "w") as f:
        f.write(str(x))
    return x

# Шаг 6: Вычисление открытого ключа y
def compute_public_key(x, e, n):
    y = pow(x, e, n)
    with open("public_key.txt", "w") as f:
        f.write(f"{n}\n{e}\n{y}")
    return n, e, y

# Шаг 7: Генерация случайного числа r и вычисление a = r^e mod n
def generate_r_and_compute_a(n, e):
    r = random.randint(1, n - 1)
    a = pow(r, e, n)
    with open("r_value.txt", "w") as f:
        f.write(str(r))
    with open("a_value.txt", "w") as f:
        f.write(str(a))
    return r, a

# Шаг 8: Выбор случайного значения c и отправка его стороне A
def generate_c(e):
    c = random.randint(0, e - 1)
    with open("c_value.txt", "w") as f:
        f.write(str(c))
    return c

# Шаг 9: Вычисление значения z = r * x^c mod n и отправка его стороне B
def compute_z(r, x, c, n):
    z = (r * pow(x, c, n)) % n
    with open("z_value.txt", "w") as f:
        f.write(str(z))
    return z

# Шаг 10: Проверка подлинности на стороне B
def verify_authenticity(z, e, a, y, c, n):
    left_side = pow(z, e, n)
    right_side = (a * pow(y, c, n)) % n
    with open("verification_result.txt", "w", encoding="UTF-8") as f:
        if left_side == right_side:
            f.write("Подлинность доказана.")
            print("Подлинность доказана.")
        else:
            f.write("Ошибка проверки подлинности.")
            print("Ошибка проверки подлинности.")
    return left_side == right_side

# Вспомогательная функция для генерации случайного простого числа в диапазоне
def random_prime(start, end):
    num = random.randint(start, end)
    while not isprime(num):
        num = random.randint(start, end)
    return num

# Объединенное меню для выполнения всех шагов
def menu():
    while True:
        print("\nМеню:")
        print("1. Вычисление значения J и сохранение")
        print("2. Генерация простых чисел p, q и вычисление n")
        print("3. Вычисление функции Эйлера φ(n)")
        print("4. Выбор e и вычисление s")
        print("5. Вычисление закрытого ключа x")
        print("6. Вычисление открытого ключа y")
        print("7. Генерация r и вычисление a")
        print("8. Генерация случайного c")
        print("9. Вычисление z и отправка его стороне B")
        print("10. Проверка подлинности")
        print("11. Выйти из программы")
        choice = input("Выберите действие (1-11): ")

        if choice == '1':
            filename = input("Введите имя файла с атрибутами: ")
            J = compute_j_from_file(filename)
            print(f"Числовое значение J сохранено в J_value.txt")

        elif choice == '2':
            bit = int (input("Укажите битность чисел p и q: "))
            n, p, q = generate_primes(bit)
            print(f"Число n и простые числа p, q сохранены в n_value.txt")

        elif choice == '3':
            with open("n_value.txt", "r") as f:
                _, p, q = [int(line.strip()) for line in f.readlines()]
            phi_n = compute_euler_totient(n, p, q)
            print(f"Значение функции Эйлера φ(n) сохранено в phi_value.txt")

        elif choice == '4':
            with open("phi_value.txt", "r") as f:
                phi_n = int(f.read().strip())
            e, s = choose_e_and_compute_s(phi_n)
            print("Числа e и s сохранены в e_s_values.txt")

        elif choice == '5':
            with open("J_value.txt", "r") as f:
                J = int(f.read().strip())
            with open("n_value.txt", "r") as f:
                n = int(f.readline().strip())
            with open("e_s_values.txt", "r") as f:
                _, s = [int(line.strip()) for line in f.readlines()]
            x = compute_private_key(J, s, n)
            print("Закрытый ключ x сохранен в private_key.txt")

        elif choice == '6':
            with open("private_key.txt", "r") as f:
                x = int(f.read().strip())
            with open("e_s_values.txt", "r") as f:
                e = int(f.readline().strip())
            with open("n_value.txt", "r") as f:
                n = int(f.readline().strip())
            n, e, y = compute_public_key(x, e, n)
            print("Открытый ключ (n, e, y) сохранен в public_key.txt")

        elif choice == '7':
            with open("public_key.txt", "r") as f:
                n, e, y = [int(line.strip()) for line in f.readlines()]
            r, a = generate_r_and_compute_a(n, e)
            print("Значения r и a сохранены в файлы r_value.txt и a_value.txt")

        elif choice == '8':
            with open("e_s_values.txt", "r") as f:
                e = int(f.readline().strip())
            c = generate_c(e)
            print("Случайное значение c сохранено в файл c_value.txt")

        elif choice == '9':
            with open("r_value.txt", "r") as f:
                r = int(f.read().strip())
            with open("private_key.txt", "r") as f:
                x = int(f.read().strip())
            with open("c_value.txt", "r") as f:
                c = int(f.read().strip())
            with open("n_value.txt", "r") as f:
                n = int(f.readline().strip())
            z = compute_z(r, x, c, n)
            print("Значение z сохранено в файл z_value.txt")

        elif choice == '10':
            with open("z_value.txt", "r") as f:
                z = int(f.read().strip())
            with open("a_value.txt", "r") as f:
                a = int(f.read().strip())
            with open("public_key.txt", "r") as f:
                n, e, y = [int(line.strip()) for line in f.readlines()]
            with open("c_value.txt", "r") as f:
                c = int(f.read().strip())
            verify_authenticity(z, e, a, y, c, n)

        elif choice == '11':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    menu()