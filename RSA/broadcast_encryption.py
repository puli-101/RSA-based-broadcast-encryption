from Crypto.Util.number import getPrime, getRandomRange
from sympy import *
from functools import reduce
from arithmetics import *
#il faut installer pycryptodome : pip3 install pycryptodome et
#sympy : pip3 install sympy

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

def get_inverse(a, p):
    """
        algorithme pour trouver l'inverse de a mod p où p est premier
    """
    return pow(a, p - 2, p)

def find_generator(p, primes = []):
    """
        etant donne p et la factorisation de phi(p) on renvoie un generateur de p premier > 2
        (normalement on connait deja la factorisation de phi(p) par le Setup)
        https://en.wikipedia.org/wiki/Primitive_root_modulo_n
    """
    if len(primes) == 0:
        primes = [2] + [i for i in range(3, p, 2) if (p - 1) % i == 0]
    def is_generator(g, phi, primes):
        for prime in primes:
            if pow(g, phi//prime, p) == 1:
                return False
        return True
    for g in range(2, p):
        if is_generator(g, p - 1, primes):
            return g

def get_primes(N, lam):
    """
        On genere N nombres premiers de taille environ lambda
        Retour :    liste des N nbrs premiers,
                    p0
                    q0
                    p = 2p0 * PI(p_i) + 1
                    q = 2q0 * PI(p_j) + 1
    """
    primes = []
    while len(primes) < N:
        p = randprime(2 ** (lam - 1),2 ** lam)
        #il faut s'assurer qu'ils sont uniques
        if not p in primes:
            primes += [p]
    p0 = randprime(2 ** (lam - 1),2 ** lam)
    q0 = randprime(2 ** (lam - 1),2 ** lam)

    p = 2*p0
    q = 2*q0

    for i in range (1, round(N/2) + 1):
        p *= primes[i-1]
        q *= primes[i+round(N/2) - 1]
    
    p += 1
    q += 1
    
    return (primes, p0, q0, p, q)
    
def Setup(N, lam):
    primes = []
    p0 = 1
    q0 = 1
    p = 0
    q = 0
    tries = 0
    while True:
        (primes, p0, q0, p, q) = get_primes(N, lam)
        #on itere jusqu'a ce qu'on trouve p et q premiers -> test miller rabin
        if not millerRabin(p) and not millerRabin(q):
            break
        tries += 1
        print("Essais",tries)
    
    
    n = p*q
    print("p :",p,"q :",q)
    print("n",n)
    print("p_i[] : ",primes)
    print("p0 :", p0)
    print("q0 :", q0)
    gamma = randint(n, 2*n)
    print("gamma :",gamma)
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
    print("!",g1)
    print("!",g2)
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