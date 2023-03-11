#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arithmetics import *
from broadcast_encryption import *

def menu():
    print("-"*20)
    print("1. Chiffrer un message du clavier")
    print("2. Chiffrer fichier")
    print("3. Dechiffrer fichier")
    print("4. Afficher fichier")
    print("5. Fermer")
    print("Option : " ,end="")

def test_RSA():
    options = [chiffrer_terminal, 
                chiffrer_fichier,
                dechiffrer_fichier,
                afficher_fichier,
                exit]
    
    print("Alice envoie un message a Bob")
    print("Generation des cles")

    (bob['n'],bob['e'],bob['d']) = generate_key()
    (alice['n'],alice['e'],alice['d']) = generate_key()

    print("Cle publique de Alice : (n : ",hex(alice['n']),", e : ",alice['e'],")")
    print("Cle publique de Bob : (n : ",hex(bob['n']),", e : ",bob['e'],")")

    while True:
        menu()
        o = int(input())
        if (o > 0 and o < 6):
            options[o - 1]()

if __name__ == "__main__":
    #Exemple d'utilisation
    N = 8
    lam = 40 #en nombre de bits recommendation de l'article : 2 ** 80

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
    
    
