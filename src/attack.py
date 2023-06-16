from arithmetics import *
from sage.all import *
from utilities import *

log_dictionary = {}
debug = True

####### Basic Attack
def get_gamma_multi_sk(sk, pk, lam, N, n):
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
    
    #return get_all_gammas(p0,q0, factors, sk[0], sk[1])

############# GCD-based Attack
def get_gamma_2sk_gcd(sk, pk, lam, N, n):
    """
        On suppose que le p_1 et p_2 manquants sont dans p ou q
        Factorisation utilisant le pgcd en se basant sur le theoreme de Fermat
    """
    #exctraction des facteurs connus
    factors = get_factors(sk,pk,lam)
    
    #on factorise n en applicant le pgcd de n et la puissance d'un nombre quelconque mod p
    a = 2
    product = [2] + factors #[2, p0, q0, p_1, ...] sauf p_i et p_j
    p = -1
    q = -1
    for exponent in product:
        a = pow(a, exponent, n)
        b = a - 1
        factor = gcd(int(b),int(n))
        if (factor != 1 and factor != n):
            p = factor
            q = n//p
            break
    if (p != -1):
        print("n-Factoring successful")
        print("p:",p)
        print("q:",q)
        exit(0)
    else:
        print("Unable to factor n")
        exit(-1)

    factors = [int(x) for x in ecm.factor((p - 1)//2) + ecm.factor((q - 1) // 2)]

    print("Retrieving p0 and q0...")
    p0, q0 = get_p0_q0(factors, g_i, N, n)

    #return get_all_gammas(p0,q0, factors, sk[0], sk[1])

########## Continued Fractions Attack
def is_missing_primes(approx, product, lam, n):
    """
        teste si l'approximation approx = a/b 
        est egal a 1/(4 * p_l * p_2l) i.e. les 
    """
    approx = Fraction(1, approx)
    if approx.denominator != 1:
        return False
    
    print("Testing possible solution")
    #si l'approximation est bonne 
    #pour tout x dans Zn, x ^ (product * approx) = 1 mod n

    for i in range(0,20):
        x = randint(2, n - 2)
        if pow(x, product * approx.numerator, n) != 1:
            print("exit")
            return False

    return True

def find_primes_from_product_over_n(product, lam, n):
    """
        On recree le developpement en fraction continue de product/n 
        ou product est le produit des facteurs premiers de p - 1 et q - 1 connus et n = p*q
        A chaque etape du developpement on teste si on a deja trouve les valeurs des nombres premiers manquants
        On retourne les valeurs des p_i et p_j manquants
    """
    coefs = []
    fraction = Fraction(int(product), n)
    while True:
        #algorithme du dev en fraction continue
        real = fraction.numerator//fraction.denominator
        fraction = fraction - real
        coefs.append(real)

        #test a chaque etape si l'approximation courante est les p_i et p_j qui manquent
        approx = get_fraction_from_coefficients(coefs.copy())
        
        if approx.numerator != 0 and is_missing_primes(approx, product, lam, n):
            return approx 
        
        if fraction.numerator == 0:
            break
        fraction = Fraction(fraction.denominator, fraction.numerator)
    
    return None

def get_gamma_2sk_dev_frac(sk, pk, lam, N, n):
    #extraction des facteurs premiers connus de p - 1 et q - 1 ou n = p*q
    print("Retrieving all known prime factors of phi(n)...")
    factors = get_factors(sk,pk,lam)
    print(factors)
    product = 1
    for f in factors:
        product *= f
    if debug:
        print("Product", product)
    approx = find_primes_from_product_over_n(product, lam, n)
    if approx == None:
        print("Fatal Error: unable to factor p - 1 and q - 1")
    
    missing = ecm.factor(Fraction(1, approx).numerator)
    print("Missing primes : ", missing)
    

############### Supplementary functions 

def get_all_gammas(p0, q0, factors, gamma_1, gamma_2):
    """
        A partir de p0, q0, deux sk, et la liste des facteurs p_i
        On extrait la liste de tous les gamma mod p0*q0*(produit de p_i) possibles car on a la congruence
        gamma [mod p0*q0produit p_i] =  { gamma_1 mod p0*q0*p1_bar
                                        { gamma_2 mod p1
    """
    gamma_lst = []
    for p_i in factors:
        if p_i == p0 or p_i == q0:
            continue
        mod1 = 1
        for p in factors:
            if p != p_i:
                mod1 *= p
        #on applique le theoreme des restes chinois
        gamma = CRT(gamma_1, mod1, gamma_2, p_i)
        gamma_lst += [gamma]
        log_dictionary[p_i] = int(gamma) 
    save_log("gamma_list_", log_dictionary)
    return gamma_lst

def get_p0_q0(factors, pk, N, n):
    """
        On essaie tous les combinaisons possibles pour trouver p0 et q0
        Peut etre qu'il y a un moyen de faire mieux
    """
    if (factors == N):
        print("Error list of factors doesn't match number of users + 2")
        exit()
    for p0 in factors:
        for q0 in factors:
            found = False
            for g_l in pk:
                for p_l in factors:
                    #les g_l sont d'un certain ordre p0*q0*p_l qu'on cherche
                    if (pow(g_l, p0 * q0 * p_l, n) == 1):
                        found = True
                        break
            if found:
                return p0, q0 
    return None, None


########### Auxiliary Functions

def get_prime_factors_from_2_sk(gamma_1, gamma_2):
    """
        Factorisation de la difference de deux sk
    """
    diff = abs(gamma_1 - gamma_2)
    return ecm.factor(diff)

def filter_batches(liste_1, liste_2, lam):
    """
        Fonction pour supprimer les valeurs dupliquees 
        et les nombres premiers de bitsize differente a lambda
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

def get_factors(sk,pk,lam):
    g_i, y_i = pk
    #on factorise la difference de deux sk
    batch = get_prime_factors_from_2_sk(sk[0], sk[1])
    
    #on filtre la liste pour mantenir que les nombres premiers plus grandes que 2**lambda
    factors = []
    for prime in batch:
        if prime >= 2 ** (lam - 1):
            factors += [prime]
    
    return factors