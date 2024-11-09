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
def compute_euler_totient(p, q):
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

# Шаг 7: Подписание сообщения из файла
def sign_message_from_file(message_file, r, e, x, n):
    with open(message_file, "r", encoding="UTF-8") as f:
        M = f.read().strip()  # Читаем сообщение из файла
    a = pow(r, e, n)
    d = hash_message(M, a) % e
    z = (r * pow(x, d, n)) % n
    with open("d_z.txt", "w", encoding="UTF-8") as f:
        f.write(f"Signature d: {d}\nSignature z: {z}")
    return d, z

# Хеширование сообщения
def hash_message(M, a):
    hasher = hashlib.sha256()
    hasher.update(f"{M}{a}".encode())
    return int(hasher.hexdigest(), 16)

# Вспомогательная функция для генерации случайного простого числа в диапазоне
def random_prime(start, end):
    num = random.randint(start, end)
    while not isprime(num):
        num = random.randint(start, end)
    return num

# Проверка подписи
def verify_signature_from_file(message_file, signature_file, e, J, n):
    # Чтение сообщения из файла
    with open(message_file, "r", encoding="UTF-8") as f:
        M = f.read().strip()
    
    # Чтение подписи из файла
    with open(signature_file, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        d = int(lines[-2].split(": ")[1])
        z = int(lines[-1].split(": ")[1])
    
    # Вычисление a' и d'
    a_ = (pow(z, e, n) * pow(J, d, n)) % n
    d_ = hash_message(M, a_) % e
    
    # Проверка равенства d и d'
    with open("signature_verification_result.txt", "w", encoding="UTF-8") as f:
        if d == d_:
            f.write("Подпись действительна.")
            print("Подпись действительна.")
        else:
            f.write("Ошибка проверки подписи.")
            print("Ошибка проверки подписи.")
    return d == d_

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
        print("7. Генерация r")
        print("8. Подписание сообщения из файла")
        print("9. Проверка подписи")
        print("10. Выйти из программы")
        choice = input("Выберите действие (1-10): ")

        if choice == '1':
            filename = input("Введите имя файла с атрибутами: ")
            J = compute_j_from_file(filename)
            print(f"Числовое значение J сохранено в J_value.txt")

        elif choice == '2':
            bit = int(input("Укажител битность чисел p и q: "))
            n, p, q = generate_primes(bit)
            print(f"Число n и простые числа p, q сохранены в n_value.txt")

        elif choice == '3':
            with open("n_value.txt", "r") as f:
                _, p, q = [int(line.strip()) for line in f.readlines()]
            phi_n = compute_euler_totient(p, q)
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
            r = random.randint(1, n - 1)  # Генерация r в диапазоне от 1 до n-1
            with open("r_value.txt", "w") as f:
                f.write(str(r))
            print("Значение r сохранено в r_value.txt")

        elif choice == '8':
            message_file = input("Введите имя файла с сообщением для подписи: ")
            with open("r_value.txt", "r") as f:
                r = int(f.read().strip())
            with open("e_s_values.txt", "r") as f:
                e = int(f.readline().strip())
            with open("n_value.txt", "r") as f:
                n = int(f.readline().strip())
            with open("private_key.txt", "r") as f:
                x = int(f.read().strip())
            d, z = sign_message_from_file(message_file, r, e, x, n)
            print(f"Подпись сообщения сохранена в файлы {message_file}, d_z.txt")

        elif choice == '9':
            message_file = input("Введите имя файла с сообщением для проверки подписи: ")
            with open("J_value.txt", "r") as f:
                J = int(f.read().strip())
            with open("n_value.txt", "r") as f:
                n = int(f.readline().strip())
            with open("public_key.txt", "r") as f:
                n, e, y = [int(line.strip()) for line in f.readlines()]
            verify_signature_from_file(message_file, "d_z.txt", e, J, n)

        elif choice == '10':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")

menu()