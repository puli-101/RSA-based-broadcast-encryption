#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mon_rsa import *

def menu():
    print("-"*20)
    print("1. Chiffrer un message du clavier")
    print("2. Chiffrer fichier")
    print("3. Dechiffrer fichier")
    print("4. Afficher fichier")
    print("5. Fermer")
    print("Option : " ,end="")

if __name__ == "__main__":
    options = [chiffrer_terminal, 
                chiffrer_fichier,
                dechiffrer_fichier,
                afficher_fichier,
                exit]
    print("Alice envoie un message a Bob")
    print("Informations par defaut : ")
    print("Cle publique de Alice : (n : ",alice['n'],", e : ",alice['e'],")")
    print("Cle publique de Bob : (n : ",bob['n'],", e : ",bob['e'],")")
    while True:
        menu()
        o = int(input())
        if (o > 0 and o < 6):
            options[o - 1]()
