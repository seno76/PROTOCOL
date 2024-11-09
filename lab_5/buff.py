import random
from sympy import isprime, gcd
import hashlib

"""Схема аутентификации Гиллу – Кискате"""

# Генерирования простого числа с n бит
def gen_prime(bit): 
    while True:
        p = random.getrandbits(bit)
        if isprime(p):
            return p

def find_e(n, ph): 
    e = random.randint(2, ph - 1) 
    while gcd(e, ph) != 1: 
        e = random.randint(2, ph - 1) 
    return e 

def gen_p_q_n(bit):
    p = gen_prime(bit)
    q = gen_prime(bit)
    n = p * q
    return p, q, n

def gen_B(v, n, J, bit):
    B = random.randint(0, n - 1)
    while J * pow(B, v, n) % n != 1:
        B = random.randint(0, n - 1)
    return B

def step_1(n, v):
    r = random.randint(1, n - 1)
    T = pow(r, v, n)
    return r, T

def step_2(v):
    d = random.randint(0, v - 1)
    return d

def step_3(r, B, d, n):
    D = r * pow(B, d, n) % n
    return D

def step_4(T, D, v, J, d, n):
    T_ = pow(D, v, n) * pow(J, d, n) % n
    return T == T_

if __name__ == "__main__":
    bit = 10
    J = 120

    
    with open("atributs.txt", "rb") as f:
        file_data = f.read()

    # Вычисляем SHA-256 хэш от данных файла
    hash_object = hashlib.sha256(file_data)
    hex_dig = hash_object.hexdigest()
        
        
    print(int(hex_dig))

    v = 4
    p, q, n = gen_p_q_n(bit)

    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    print("e", e)
    

    s = pow(e, -1, phi)
    x = pow(J, -s, n)
    print("s", s)
    print("x", x)


    y = pow(x, e, n)
    print("y", y)

    # ------------------------

    r = random.randint(1, n - 1)
    a = pow(r, e, n)
    print("r", r)
    print("a", a)

    # ------------------------

    c = random.randint(0, e - 1)
    print("c", c)

    # ------------------------

    z = r * pow(x, c, n) % n
    print("z", z)

    # ------------------------

    print(pow(z, e, n) == a * pow(y, c, n) % n)    


    

    

    
    
