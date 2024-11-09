import random
from sympy import isprime, gcd 

# Генерирования простого числа с n бит
def gen_prime(n): 
    while True:
        p = random.getrandbits(n)
        if isprime(p):
            return p

# Генерация параметров доверенного центра
def trusted_center(n_bits):
    p = gen_prime(n_bits)
    q = gen_prime(n_bits)
    return p, q, p * q

# Генерация секрета для пользователя (публичный и приватный ключ)
def gen_secret(k, n):
    s_lst = []
    while len(s_lst) != k:
        param = random.randint(1, n - 1)
        if gcd(param, n) == 1:
            s_lst.append(param)
    b_lst = [random.choice([0, 1]) for _ in range(k)]
    v_i = []
    for i in range(k):
        v_i.append(((-1) ** b_lst[i] * pow(s_lst[i] ** 2, -1, n)) % n)
    return s_lst, b_lst, v_i

# Генерирование бинарной последовательности заданной длины k
def gen_bin_vec(k):
    return [random.choice([0, 1]) for _ in range(k)]

# Передача пользователем Алисы данные для ее подтверждения
def get_x(n):
    r = random.randint(1, n - 1)
    x = pow(r, 2, n)
    return r, x

# Вычисление параметра y Алисы
def get_y(a_s_lst, bin_vec_bob, r, n, k):
    y = 1
    for i in range(k):
        y *= pow(a_s_lst[i], bin_vec_bob[i], n)
    y = (r * y) % n
    return y
 
# Проверка аутентификации Алисы
def chek_aunth(x, y, k, n, a_v_i, bin_vec_bob):
    z = 1
    for i in range(k):
        z *= pow(a_v_i[i], bin_vec_bob[i], n)
    z = (pow(y, 2) * z) % n
    return z in [-x % n, x % n] and z != 0

# Полная функция реализующая данный протокол    
# (запускается при необходимости)
def feiga_fiat_shamir(n_bits, k, t):
    p, q, n = trusted_center(n_bits)
    a_s_lst, a_b_lst, a_v_i = gen_secret(k, n)
    for _ in range(t):
        r = random.randint(1, n - 1)
        x = pow(r, 2, n)
        bin_vec_bob = gen_bin_vec(k)
        y = 1
        for i in range(k):
            y *= pow(a_s_lst[i], bin_vec_bob[i], n)
        y = (r * y) % n
        z = 1
        for i in range(k):
            z *= pow(a_v_i[i], bin_vec_bob[i], n)
        z = (pow(y, 2) * z) % n
        if z in [-x % n, x % n] and z != 0:
            print("Аутентификация успешна!")
        else:
            print("Аутентификация провалена!")

# Чтение параметра у из файла
def read_y_in_file():
    with open("y_data.txt", "r", encoding="UTF-8") as f:
        line = f.readline().split()
        y = int(line[0])
    return y


# Чтение приватного ключа
def read_primary_key_file():
    with open("primary_key.txt", "r", encoding="UTF-8") as f:
        line = f.readline().split()
        a_s_lst = [int(el) for el in line]
    return a_s_lst

# Чтение данных о r и x из файла 
def read_data_for_bob():
    with open("data_for_bob.txt", "r", encoding="UTF-8") as f:
        line = f.readline().split()
        x = int(line[0])
    return x

if __name__ == "__main__":
    # feiga_fiat_shamir(11, 3, 3)
    param = input("""Введите режим работы
1 - Генерация параметров системы
2 - Генерация секрета для участника 
3 - Отправка параметра x
4 - Отправка битового вектора Боба
5 - Отправка параметра y
6 - Проведение Бобом аутентификации \n:>""")
    while param not in ["1", "2", "3", "4", "5", "6"]:
        param = input(":>")
    
    if param == "1":
        
        n_bits = input("Укажите битность генерируемых чисел: ")
        while not n_bits.isdigit():
            n_bits = input("Количество бит:")
        p, q, n = trusted_center(int(n_bits))

        print(f"p = {p}, q = {q}, n = {n}")
        print("Укажите параметры безопасности:")

        k = int(input("k = "))
        t = int(input("t = "))

        print("Параметры записаны в файл param_system.txt")
        with open("param_system.txt", "w", encoding="UTF-8") as f:
            f.write(f"{p} {q} {n} {k} {t}")

    elif param == "2":

        with open("param_system.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            k = int(line[-2])
            t = int(line[-1])
            n = int(line[2])

        s_lst, b_lst, v_i = gen_secret(k, n)
        v_i = " ".join(map(lambda x: str(x), v_i))
        s_lst = " ".join(map(lambda x: str(x), s_lst))

        print(f"Публичный ключ: ({v_i}; {n})")
        print(f"Приватный ключ: {s_lst}")

        with open("public_key.txt", "w", encoding="UTF-8") as f:
            f.write(f"({v_i}; {n})")

        with open("primary_key.txt", "w", encoding="UTF-8") as f:
            f.write(f"{s_lst}")

        print("Данные сохранены в файлы public_key.txt и primary_key.txt")

    elif param == "3":

        with open("param_system.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            k = int(line[-2])
            n = int(line[2])

        a_s_lst = read_primary_key_file()
        r, x  = get_x(n)

        with open("data_for_bob.txt", "w", encoding="UTF-8") as f:
            f.write(f"{x}")

        with open("r.txt", "w", encoding="UTF-8") as f:
            f.write(f"{r}")


        print("r параметр записан в файл r.txt")
        print("x записан в файл data_for_bob.txt")

    elif param == "4":

        with open("param_system.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            k = int(line[-2])

        bin_vec = gen_bin_vec(k)

        with open("bin_vec_bob.txt", "w", encoding="UTF-8") as f:
            str_ = " ".join([str(bit) for bit in bin_vec])
            f.write(str_)

        print("Бинарный вектор Боба записан в файл bin_vec_bob.txt")

    elif param == "5":

        a_s_lst = read_primary_key_file()

        with open("bin_vec_bob.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            bin_bob = [int(el) for el in line]

        
        with open("r.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            r = int(line[0])


        with open("param_system.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            k = int(line[-2])
            n = int(line[2])

        y = get_y(a_s_lst, bin_bob, r, n, k)

        with open("y_data.txt", "w", encoding="UTF-8") as f: 
            f.write(str(y))
        
        print("Передаваемый параметр у Алисы записан в файл y_data.txt")

    else:
        y = read_y_in_file()
       
        with open("public_key.txt", "r",encoding="UTF-8") as f:
            line = f.readline()[1:-1].replace(";", " ").split()[:-1]
            a_v_i = [int(el) for el in line]
        
        with open("param_system.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            k = int(line[-2])
            n = int(line[2])

        with open("bin_vec_bob.txt", "r", encoding="UTF-8") as f:
            line = f.readline().split()
            bin_vec_bob = [int(el) for el in line]

        x = read_data_for_bob()

        if chek_aunth(x, y, k, n, a_v_i, bin_vec_bob):
            print("Аутентификация успешна!")
        else:
            print("Аутентификация провалена!")