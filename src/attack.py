from arithmetics import *
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


def get_p0_q0(factors, pk, N, n):
    """
        On essaie tous les combinaisons possibles pour trouver p0 et q0
    """
    for i in range (0, N + 2):
        p0 = factors[i]
        for j in range (i + 1, N + 2):
            q0 = factors[j]
            matches = 0
            print("Trying for p0 :", p0,"q0 :",q0)
            for k in range(j + 1, N + 2):
                p_l = factors[k]
                for g_l in pk:
                    #les g_l sont d'un certain ordre p0*q0*p_l qu'on cherche
                    if (pow(g_l, p0 * q0 * p_l, n) == 1):
                        matches += 1
                        break
            if matches == N:
                return p0, q0 
    return None, None



def get_gamma_4sk(sk, pk, lam, N, n):
    """
        Algorithme heuristique pour trouver gamma mod produit p_i 
        a partir de 4 cle secretes (sk), la taille en nombre de bits de chaque p_i (lam i.e. lambda)
        et le nombre d'utilisateurs en total (N)
        et n = p*q
    """
    print("Retrieving all primes...")
    #on obtient le produit des p_i sauf p_0 et p_1 plus le produit de quelques autres termes
    batch_1 = get_prime_factors_from_2_sk(sk[0], sk[1])
    batch_2 = get_prime_factors_from_2_sk(sk[2], sk[3])

    factors = filter_batches(batch_1, batch_2, lam)

    print("All prime factors : ",factors)

    print("Retrieving p0 and q0...")
    g_i, y_i = pk
    p0, q0 = get_p0_q0(factors, g_i, N, n)
    if p0 == None:
        print("! p0 and q0 not found !")
    else:
        print("p0:",p0,"q0:",q0)
    #gamma = CRT(gamma_1 mod p1_bar, gamma_2 mod p2)
    return factors

    