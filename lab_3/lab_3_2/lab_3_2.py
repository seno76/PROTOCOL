import hashlib
import string
import random

# Генерация хэша по строке
def hash_function(value):
    return hashlib.md5(value.encode()).hexdigest()

# Генерация случайной последовательности для секретного ключа пользователя
def generate_random_key(count):
    with open("alph.txt", "r", encoding="UTF-8") as f:
        alph = f.readline()
    letters_and_digits = alph
    random_key = ''.join(random.choice(letters_and_digits) for _ in range(count))
    return random_key

# Добавление пользователя в базу данных
def add_user_to_database(name, hash, file_name="database.txt"):
    with open(file_name, "a", encoding="UTF-8") as f:
        f.write(f"{name} : {hash}\n")

# Получение из базы данных хэша пользователя
def get_hash_for_user(name):
    with open("database.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(":")
            name_user = data[0].strip()
            hash_user = data[1].strip()
            if name == name_user:
                return hash_user
    return None

# Проверка пользователя в базе данных
def check_user_in_database(name):
    with open("database.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(":")
            name_user = data[0].strip()
            if name_user == name:
                return True
    return False

# Удаление пользователя из бд
def del_user_from_database(name):
    lst = []
    with open("database.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(":")
            name_user = data[0].strip()
            if name_user != name:
                lst.append(line)
    with open("database.txt", "w", encoding="UTF-8") as f:
        for i in range(len(lst)):
            f.write(lst[i])

# Создание временных паролей в файле пользователя
def initialize_passwords(N, username, K):
    W_list = [K]
    for _ in range(N):
        W_list.append(hash_function(W_list[-1]))
    W_list = W_list[::-1]
    
    filename = f"{username}_passwords.txt"
    with open(filename, 'w') as f:
        for W in W_list[1:-1]:
            f.write(W + '\n')
    print(f"Инициализация завершена. Список паролей сохранен в '{filename}'")
    return W_list[-1], W_list[0]

# Чтение паролей из файла пользователя
def read_passwords(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Обновление и запись последовательности паролей
def update_password_file(filename, W_list):
    with open(filename, 'w') as f:
        for W in W_list:
            f.write(W + '\n')

# Удаление использованного пароля
def remove_used_password(filename):
    passwords = read_passwords(filename)
    updated_passwords = passwords[1:]
    update_password_file(filename, updated_passwords)

# Вывод текущих паролей из файла пользователя
def print_current_passwords(filename):
    passwords = read_passwords(filename)
    print(f"Текущие одноразовые пароли в файле '{filename}':")
    for i, password in enumerate(passwords):
        print(f"W{len(passwords) - i}: {password}")

def step_1_file(name, secret_key, file_name):
    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(f"{name} {secret_key}")

def step_1_file_read(file_name):
    with open(file_name, "r", encoding="UTF-8") as f:
        line = f.readline().split()
        name = line[0].strip()
        secret_key = line[1].strip()
    return name, secret_key

# Отправка данных пользователя при аутентификации
def auth_user():
    name = input("Введите свое имя: ")
    filename = f"{name}_passwords.txt"
    if check_user_in_database(name):
        lst_hash = read_passwords(filename)
        if not lst_hash:
            print("Временные пароли для автоизации закончились, необходимо сгенерировать новые")
            del_user_from_database(name)
        else:
            hash = input("Введите пароль: ")
            step_1_file(name, hash, "data_user2.txt")
    else:
        print(f"Пользователь {name} не был добавлен в базу данных (выполните шаг 1-2)")

# Аутентификация на сервере
def authenticate_server(name_user, secret_key, file_passwd):
    print(f"Проверка пароля на сервере...")
    if hash_function(secret_key) == get_hash_for_user(name_user):
        remove_used_password(file_passwd)
        update_hash_for_user(name_user, secret_key)
        print(f"Аутентификация успешна: h(h(N)) = {hash_function(secret_key)} совпадает с W(N+1).")
        return True
    else:
        print(f"Аутентификация не удалась: W(N+1) не совпадает.")
        return False

# Обновление хэша пользователя в БД
def update_hash_for_user(name, new_hash):
    res = []
    with open("database.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            data = lines[i].strip().split(":")
            name_user = data[0].strip()
            if name_user == name:
                lines[i] = f"{name} : {new_hash}\n"
            res.append(lines[i])
    str_data = "".join(res)
    with open("database.txt", "w", encoding="UTF-8") as f:
        f.write(str_data)

if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("0. Генерация случайной последовательности Алисы")
        print("1. Отправка имени пользователя и его случайной последовательности")
        print("2. Инициализация одноразовых паролей и их отпрака пользователю")
        print("3. Просмотреть текущие одноразовые пароли")
        print("4. Отправка данных пользователя на сервер")
        print("5. Аутентификация пользователя")
        print("6. Выйти из программы")
        choice = input("Выберите действие (0-6): ")

        if choice == '0':

            len_ = input("Введите длину генерируемой последовательности: ")
            secret_key = generate_random_key(int(len_))
            print(secret_key)
            with open("random_num.txt", "w", encoding="UTF-8") as f:
                f.write(secret_key)
            print("Случайная последовательность записана в файл random_num.txt")

        elif choice == '1':
            name = input("Введите имя пользователя: ").strip()
            if check_user_in_database(name):
                print(f"Пользователь {name} уже содержится в базе данных")
            else:
                secret_key = input(f"Введите случайную последовательность пользователя {name}: ")
                step_1_file(name, secret_key, "data_user.txt")
                print(f"Имя и секретный ключ пользователя сохранены в файл data_user.txt")

        elif choice == '2':
            N = int(input("Укажите количество временных паролей: "))
            name, secret_key = step_1_file_read("data_user.txt")
            filename = f"{name}_passwords.txt"
            start_passwd, end_passwd = initialize_passwords(N, name, secret_key)
            add_user_to_database(name, end_passwd)
        
        elif choice == '3':
            name = input("Введите имя пользователя для просмотра паролей: ").strip()
            filename = f"{name}_passwords.txt"
            print_current_passwords(filename)
        
        elif choice == '4':
            auth_user()

        elif choice == '5':
            name, secret_key = step_1_file_read("data_user2.txt")
            filename = f"{name}_passwords.txt"
            authenticate_server(name, secret_key, filename)
        
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")