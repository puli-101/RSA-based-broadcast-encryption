from arithmetics import *
from pathlib import Path
import os
from datetime import datetime
import time
import json

f = None
debug = False

def is_missing_primes(approx, product, lam, n):
    """
        teste si l'approximation approx = a/b 
        est egal a 1/(4 * p_l * p_2l) i.e. les 
    """
    approx = Fraction(1, approx)
    if approx.denominator != 1:
        return False
    
    #print("Testing possible solution")
    #si l'approximation est bonne 
    #pour tout x dans Zn, x ^ (product * approx) = 1 mod n

    for i in range(0,20):
        x = randint(2, n - 2)
        if pow(x, product * approx.numerator, n) != 1:
            #print("exit")
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

def get_gamma_2sk_dev_frac(sk, pk, lam, N, n, factors):
    #extraction des facteurs premiers connus de p - 1 et q - 1 ou n = p*q
    #print("Retrieving all known prime factors of phi(n)...")
    #factors = get_factors(sk,pk,lam)
    #print(factors)
    global f
    start_time = time.time()
    
    product = 1
    for nums in factors:
        product *= nums
    if debug:
        print("Product", product)
    approx = find_primes_from_product_over_n(product, lam, n)

    attack_time = "%.6s," % (time.time() - start_time)
    print("Exec time :",attack_time)
    f.write(attack_time)

    if approx == None:
        #print("Fatal Error: unable to factor p - 1 and q - 1")
        return False
    
    #missing = ecm.factor(Fraction(1, approx).numerator)
    #print("Missing primes : ", missing)

    return True

if __name__ == "__main__":

    f = open("attack.csv","w")
    f.write("N,lam,exec_time,succeed\n")

    print("Continued Fractions Attack Tester")
    print("Please execute this code from the folder src/")
    input("Press Enter to continue...")
    
    for file_name in os.scandir("../logs"):
        if not file_name.is_file():
            continue
        try:
            loaded_data = {}
            with open(file_name.path, 'r') as fp:
                loaded_data = json.load(fp)
            public_keys = (loaded_data["g_i"], loaded_data["y_i"])
            private_keys = loaded_data["gamma_i"]
            lam = loaded_data["lam"]
            N = loaded_data["N"]
            n = loaded_data["n"]

            p0 = loaded_data["p0"]
            q0 = loaded_data["q0"]
            p_i = loaded_data["p_i"]

            factors = p_i[1:-1]
            factors += [p0] + [q0]

            print("----------------------------")
            print(file_name.path)
            print("N :",N)
            print("Lambda :",lam)
            f.write(str(N)+","+str(lam)+",")
            if get_gamma_2sk_dev_frac([private_keys[0], private_keys[-1]], public_keys, lam, N, n, factors):
                print("Attack succesful")
                f.write("1\n")
            else:
                f.write("0\n")
                print("Attack failed")
        except:
            print("----------")
            print("Error while loading "+file_name.path)
    f.close()
    