import sympy
import hashlib
import random


# Расширенный алгоритм Евклида
def gcd_xt(a, b):
    s0, t0 = 1, 0
    s1, t1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return s0, t0, a


# Вычисление хэша файла
def get_file_hash(filepath, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


# Генерирование простого числа с заданной битностью
def generate_prime(bits):
    return sympy.randprime(pow(2,(bits-1)), pow(2, bits))


# Поиск числа взаимно простого с p
def generate_coprime(p):
    while True:
        k = random.randint(2, p - 2)
        if sympy.gcd(k, p) == 1:
            return k


# Подпись сообщения
def sign_message(file_message, p, g, x):
    m = int(get_file_hash(file_message), 16)
    k = generate_coprime(p - 1)
    # k_inv, _, _ = gcd_xt(k, p - 1)
    k_inv = pow(k, -1, p - 1)
    r = pow(g, k, p)
    s = (m - x * r) * k_inv % (p - 1)
    return r, s


# Генерирование открытого и закрытого ключей
def gen_params(param=128):
    p = generate_prime(param)
    g = sympy.primitive_root(p)
    x = sympy.randprime(2, p - 1)
    y = pow(g, x, p)
    return p, g, x, y


# Проверка подписи другой стороной
def verify_signature(data, r, s, p, g, y):
    if not (0 < r < p and 0 < s < p - 1):
        return False
    m = int(get_file_hash(data), 16)
    v1 = pow(g, m, p)
    v2 = (pow(y, r, p) * pow(r, s, p)) % p
    return v1 == v2


# Чтение публичного ключа
def read_public_key(name_file="public_key.txt"):
    with open(name_file, "r") as f:
            line = f.readline()
            lst = list(map(lambda x: int(x), line[1:-1].split(",")))
            p, g, y = lst[0], lst[1], lst[2]
    return p, g, y


# Чтение приватного ключа
def read_private_key(name_file="private_key.txt"):
    with open(name_file, "r") as f:
            x = int(f.readline())
    return x


# Подписание данных
def reaa_signed_data(name_file="signed_data.txt"):
    with open(name_file, "r") as f:
            line = f.readline()
            lst = list(map(lambda x: int(x), line[1:-1].split(",")))
            r, s = lst[0], lst[1]
    return r, s

if __name__ == "__main__":
    param = input("Введите режим работы (1 - Генерация ключей, 2 - Подпись документа, 3 - Проверка подписи): ")
    try:
        if param == "1":
            # Step 1 - Генерирование параметров открытого и закрытого ключа
            param1 = input("1 - Использовать старые ключи, 2 - сгенерировать новые: ")
            if param1 == "2":
                par = input("Введите количество бит простого числа: ")
                p, g, x, y = gen_params(int(par))
                with open("private_key.txt", "w") as f:
                    f.write(str(x))
                with open("public_key.txt", "w") as f:
                    f.write(f"({p}, {g}, {y})")
                print("Проход 1: Ключи успешно сгенерированы!")
                x1, x2, x3 = read_public_key()
                x4 = read_private_key()
                print(f"Публичный ключ: ({x1}, {x2}, {x3})")
                print(f"Приватный ключ: {x4}")
            elif param1 == "1":
                print("Проход 1: Используются данные из файлов private_key.txt и public_key.txt")
                x1, x2, x3 = read_public_key()
                x4 = read_private_key()
                print(f"Публичный ключ: ({x1}, {x2}, {x3})")
                print(f"Приватный ключ: {x4}")
        elif param == "2":
            file_path = input("Введите путь к файлу который необходимо отправить: ")
            # Step 2 - Подпись тектого файла
            x = read_private_key()
            p, g, y = read_public_key()
            r, s = sign_message(file_path, p, g, x)
            with open("signed_data.txt", "w") as f:
                f.write(f"({r}, {s})")
            print(f"Проход 2: Файл {file_path} успешно подписан!")
            print(f"Полученная подпись: ({r}, {s})")
        elif param == "3":
            file_path = input("Введите путь к файлу, у которого надо проверть подпись: ")
            # Step 3 - Проверка полученного письма
            r, s = reaa_signed_data()
            print(f"Подпись файла: ({r}, {s})")
            p, g, y = read_public_key()
            flag = verify_signature(file_path, r, s, p, g, y)
            if flag:
                print(f"Проход 3: Полученный файл {file_path} не был изменен!!!")
            else:
                print(f"Проход 3: Полученный файл {file_path} был изменен в процессе передачи!!!")
    except FileNotFoundError:
        print("Указан неправильный файл!")