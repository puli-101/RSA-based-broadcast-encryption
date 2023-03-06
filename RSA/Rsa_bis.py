from Crypto.Util.number import getPrime, getRandomRange
import random
from sympy import *
from functools import reduce

"""
def chinese_remainder(m, a):
    sum = 0
    prod = reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a//b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
"""
def find_generator(p):
    res = []
    def is_generator(g, phi, primes):
        for prime in primes:
            if phi % prime == 0 and pow(g, phi//prime, p) == 1:
                return False
        return True
    phi_p = p - 1
    primes = [2] + [i for i in range(3, phi_p + 1, 2) if phi_p % i == 0]
    for g in range(2, p):
        if is_generator(g, phi_p, primes):
            res.append(g)
    return res


def Setup(N, lam):
    primes = [randprime(1,lam) for _ in range(N)]
    p0 = randprime(1,lam)
    q0 = randprime(1,lam)
    """
    p = 1
    q = 1
    for i in range (1,N//2+1):
        p *= primes[i-1]
        q *= primes[i+N//2-1]
    p *= 2*p0
    q *= 2*q0
    p += 1
    q += 1
    """
    p = randprime(1,lam)
    q = randprime(1,lam)
    n = p*q
    gamma = random.randint(n, 2*n)
    p_bar = []
    for i in range(N):
        p_bar_i = 1
        for j in range(N):
            if i != j:
                p_bar_i *= primes[j]
        p_bar.append(p_bar_i)
    #g = pow(chinese_remainder(find_generator(p),find_generator(q)),2,n)
    g1 = find_generator(p)
    g2 = find_generator(q)
    for e in g1 : 
        if e in g2 : 
            g = pow(e,2,n)
            g_i = [(pow(g, p_bar[i], n)) for i in range(N)]
            y_i = [pow(g_i[i], gamma, n) for i in range(N)]
            private_keys = [gamma % (p0*q0*p_bar[i]) for i in range(N)]
            return ((g_i,y_i), n), private_keys



def Enc(public_keys, T, message, N, n):
    r = random.randint(2, n)
    y = 1
    g = 1
    g_i,y_i = public_keys
    for i in range(N):
        if i not in T : 
            y *= y_i[i]
            g *= g_i[i]
    kT = pow(y, r, n)
    z = pow(g, r, n)
    return kT, z

def Dec(private_key, z, n):
    return pow(z,private_key,n)

#Exemple d'utilisation
N = 4
lam = 1024
(public_keys, n), private_keys = Setup(N, lam)
message = 42
T = [0, 1]
kT, z = Enc(public_keys, T, message, N, n)
decrypted_kT = Dec(private_keys[0], z, n)

print(kT)
print(decrypted_kT)
