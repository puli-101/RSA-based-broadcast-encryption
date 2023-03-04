from Crypto.Util.number import getPrime, getRandomRange
import random
from sympy import *

def find_generator(p, q):
    def is_generator(g, phi, primes):
        for prime in primes:
            if phi % prime == 0 and pow(g, phi//prime, p) == 1:
                return False
        return True
    phi_p = p - 1
    phi_q = q - 1
    primes = [2] + [i for i in range(3, phi_p + 1, 2) if phi_p % i == 0]
    for g in range(2, p):
        if is_generator(g, phi_p, primes):
            return g
    for g in range(2, q):
        if is_generator(g, phi_q, primes):
            return g
    return None


def Setup(N, lam):
    p = randprime(1,lam)
    q = randprime(1,lam)
    n = p * q
    primes = [randprime(1,lam) for _ in range(N)]
    p0 = randprime(1,lam)
    q0 = randprime(1,lam)
    gamma = random.randint(n, 2*n)
    p_bar = []
    for i in range(N):
        p_bar_i = 1
        for j in range(N):
            if i != j:
                p_bar_i *= primes[j]
        p_bar.append(p_bar_i)
    g = pow(find_generator(p,q),2,n)
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
N = 3 
lam = 1024 
(public_keys, n), private_keys = Setup(N, lam)
message = 42
T = [0, 1]
kT, z = Enc(public_keys, T, message, N, n)
decrypted_kT = Dec(private_keys[0], z, n)

print(kT)
print(decrypted_kT)
