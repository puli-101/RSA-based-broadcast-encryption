from Crypto.Util.number import getPrime, getRandomRange
from sympy import *
from functools import reduce
from arithmetics import *
from datetime import datetime
import json

log_dictionary = {}
debug = False

def save_log():
    """
        Fonction pour sauvegarder les nombres generes lors de l'execution
    """
    with open("../logs/key-gen_"+str(datetime.now())+".json", 'w') as fp:
        json.dump(log_dictionary, fp)

def get_primes(N, lam):
    """
        Cela fait partie du Setup
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

    for i in range (0, round(N/2)):
        p *= primes[i]
        q *= primes[i+round(N/2)]
    if (N%2 == 1):
        q *= primes[-1]

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
    print("Calcul de p et q...")
    while True:
        (primes, p0, q0, p, q) = get_primes(N, lam)
        #on itere jusqu'a ce qu'on trouve p et q premiers -> test miller rabin
        if not millerRabin(p) and not millerRabin(q):
            break
        tries += 1
        #print("Essais",tries)
    
    n = p*q
    gamma = randint(n, 2*n)
    p_bar = []
    for i in range(N):
        p_bar_i = 1
        for j in range(N):
            if i != j:
                p_bar_i *= primes[j]
        p_bar.append(p_bar_i)
    
    #On cherche un generateur
    g1 = find_generator(p, [p0]+primes[:round(N/2) + 1]) 
    g2 = find_generator(q, [q0]+primes[round(N/2) + 1:])
    
    alpha = chinese_remainder_prime_modules(g1,g2,p,q)
    g = pow(alpha, 2, n)

    #public keys
    g_i = [(pow(g, p_bar[i], n)) for i in range(N)]
    y_i = [pow(g_i[i], gamma, n) for i in range(N)]

    """for i in range(0, N):
        gen = g_i[i]
        prime = primes[i]
        expos = pow(gen, p0*prime*q0, n)
        print(gen, prime, expos)
    """
    for gen in g_i:
        for prime in primes:
            expos = pow(gen, p0*prime*q0, n)
            #print(expos)
            if (expos == 1):
                print("!")

    #gamma_i = gamma mod p_0*q_0*p_i
    private_keys = [gamma % (p0*q0*p_bar[i]) for i in range(N)]
    
    #Affichage des valeurs dans la terminale
    if debug:
        print("p :",p,"q :",q)
        print("n",n)
        print("p_i[] : ",primes)
        print("p0 :", p0)
        print("q0 :", q0)
        print("gamma :",gamma)
        print("g_p :",g1)
        print("g_q :",g2)
        print("g :",g)

    #Enregistrement des valeurs generes dans un fichier
    log_dictionary["N"] = N
    log_dictionary["lam"] = lam
    log_dictionary["gamma"] = gamma
    log_dictionary["gamma_i"] = private_keys
    log_dictionary["y_i"] = y_i
    log_dictionary["g_i"] = g_i
    log_dictionary["p0"] = p0
    log_dictionary["q0"] = q0
    log_dictionary["p_i"] = primes
    log_dictionary["n"] = n
    save_log()

    return ((g_i,y_i), n), private_keys



def Enc(public_keys, T, N, n):
    r = randint(2, n)
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