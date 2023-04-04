import arithmetics
from sage.all import *

def get_prime_factors_from_2_sk(gamma_1, gamma_2):
    diff = abs(gamma_1 - gamma_2)
    return ecm.factor(diff)

def filter_batches(liste_1, liste_2, lam):
    """
        il faut supprimer les doublon sauf s'ils apparaissent plusieurs fois
        et les facteurs premiers de taille different a lambda
    """
    l = []
    for x in liste_1:
        if x >= 2**(lam-1):
            l += [x]
    for i in range(0, len(liste_2)):
        x = liste_2[i]
        if x >= 2 ** (lam - 1) and (not (x in liste_1) or liste_1.count(x) < liste_2[i:].count(x)):
            l += [x]
    return l

def get_gamma_4sk(sk, lam, N):
    #on obtient le produit des p_i sauf p_0 et p_1 plus le produit de quelques autres termes
    batch_1 = get_prime_factors_from_2_sk(sk[0], sk[1])
    batch_2 = get_prime_factors_from_2_sk(sk[2], sk[3])

    factor = filter_batches(batch_1, batch_2, lam)

    print("All prime factors : ",factor)
    #gamma = CRT(gamma_1 mod p1_bar, gamma_2 mod p2)
    return factor

    