#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arithmetics import *
from broadcast_encryption import *
from attack import *

if __name__ == "__main__":
    #Exemple d'utilisation
    N = 8
    lam = 80 #en nombre de bits recommendation de l'article : 2 ** 80

    print("Setting up...")
    (public_keys, n), private_keys = Setup(N, lam)
    T = [0, 1]
    print("Generating encryption key and header...")
    kT, z = Enc(public_keys, T, N, n)
    print("k_T :",kT)
    print("z :",z)
    print("Decrypting header...")
    decrypted_kT = Dec(private_keys[0], z, n)
    if (kT == decrypted_kT):
        print("Keys match")
    else:
        print("Keys don't match")
    
    print("\nSetting up 4-sk attack...")
    gamma = get_gamma_4sk(private_keys[:4], lam, N)

    
