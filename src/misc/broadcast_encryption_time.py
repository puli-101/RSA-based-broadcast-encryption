from Crypto.Util.number import getPrime, getRandomRange
from sympy import *
from functools import reduce
from arithmetics import *
from datetime import datetime
import json
from utilities import *
import time

log_dictionary = {}
debug = False

def get_half_primes(N, lam, secondHalf):
    """
        Cela fait partie du Setup
        On genere N/2 nombres premiers de taille environ lambda
        Retour :    liste des N/2 nbrs premiers,
                    p0 un nombre premier de taille 2lambda
                    p = 2p0 * PI(p_i) + 1
    """
    primes = []
    remainder = 0
    if N % 2 != 0 and not secondHalf:
        remainder = 1
    
    while len(primes) < ((N//2) + remainder):
        p = randprime(2 ** (lam - 1),2 ** lam)
        #il faut s'assurer qu'ils sont uniques
        if not p in primes:
            primes += [p]
    p0 = randprime(2 ** (2 * lam - 1),2 ** (2 * lam))

    p = 2*p0

    for prime in primes:
        p *= prime

    p += 1

    return (primes, p0, p)
    
def Setup(N, lam):
    f=open("Setup_128_50.txt","a")
    start_time = time.time()
    primes = []
    p0 = 1
    q0 = 1
    p = 0
    q = 0
    tries = 0
    print("Calcul de p...")
    while True:
        (primes, p0, p) = get_half_primes(N, lam, False)
        #on itere jusqu'a ce qu'on trouve p et q premiers -> test miller rabin
        if not millerRabin(p):
            break
        tries += 1
        #print("Essais",tries)
    #print("p found after",tries,"tries")
    tries = 0
    print("Calcul de q...")
    while True:
        (secondHalf, q0, q) = get_half_primes(N, lam, True)
        if not millerRabin(q):
            break
        tries += 1
        #print("Essais",tries)
    print("q found after",tries,"tries")
    primes += secondHalf
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
    log_dictionary["p"] = p
    log_dictionary["q"] = q
    save_log("key-gen_", log_dictionary)
    f.write("%.6s\n" % (time.time() - start_time))
    f.close()

    return ((g_i,y_i), n), private_keys



def Enc(public_keys, T, N, n):
    f=open("Enc_128_50.txt","a")
    start_time = time.time()
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
    f.write("%.6s\n" % (time.time() - start_time))
    f.close()
    return kT, z

def Dec(private_key, z, n):
    return pow(z,private_key,n)