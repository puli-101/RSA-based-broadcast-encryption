#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt
import os

P_A = 41947
Q_A = 59281         #P_A et Q_A sont des nombres premieres
E_A = 1423
D_A = 1663530607    #D_A et E_A sont des inverses multiplicatifs [mod phi(N_A)]
N_A = 2486660107    #N_A doit etre le produit de P_A et Q_A

alice = {'p' : P_A, 'q' : Q_A, 'e' : E_A, 'd' : D_A, 'n' : N_A}

P_B = 346207
Q_B = 14821         #P_B et Q_B sont des nombres premieres
E_B = 2591          
D_B = 2265381791    #D_B et E_B sont des inverses multiplicatifs [mod phi(N_B)] 
N_B = 5131133947    #N_B doit etre le produit de P_B et Q_B

#https://primes.utm.edu/curios/index.php?start=6&stop=6

bob = {'p' : P_B, 'q' : Q_B, 'e' : E_B, 'd' : D_B, 'n' : N_B}

def fast_exp(x, n, mod):
    """
        O(log n) algorithme vu en cours d'algo, version iterative
    """
    exp = 1
    if x == 0:
        return 0

    while n != 0:
        if (n % 2) == 1:
            exp = (exp * x) % mod
        n //= 2
        x = (x * x) % mod

    return exp

def get_inverse(p, mod):
    """
        Renvoie inverse multiplicative de p [mod] i.e. q tq p * q = 1 [mod]
        O(n) pas tres efficace , prend quelques minutes
        il y a un algorithme d'euclide de complexite logarithmique 
    """
    p %= mod
    for i in range(1, mod):
        if (i * p) % mod == 1:
            return i
    return -1

def fast_inverse(p, mod):
    """
        Taken from "Guide to Elliptic Curve Cryptography"
    """
    u = p 
    v = mod
    x1 = 1
    x2 = 0
    while u != 1:
        q = v//u 
        r = v - q * u
        x = (x2 - q * x1) % mod
        v = u
        u = r
        x2 = x1
        x1 = x
    return x1

def factor(n):
    """
        Algorithme de factorisation de n, on renvoie le premier diviseur != 1
    """
    for i in range(2,int(sqrt(n)) + 1):
        if n % i == 0:
            return i
    return -1

def chiffrer_terminal():
    print("Saisissez un message : ", end="")
    msg = str(input())

    f = open("msg_terminal.txt", "w")
    print("\nMessage chiffre : ",end="")
    for m in msg:
        #c = m ^ e [mod n]
        c = str(fast_exp(ord(m),bob['e'],bob['n']))
        print(c, end=" ")
        f.write(c+" ")
    f.close()
    print("\n")


def chiffrer_fichier():
    print("Saisissez le nom d'un fichier : ", end="")
    fic = str(input())

    source = open(fic, "r")
    output = open("texte_chiffr-"+fic, "w")

    print("Message chiffre dans "+fic+" : ",end="")

    while True:
        lettre = source.read(1)
        if not lettre:
            break

        c = fast_exp(ord(lettre),bob['e'],bob['n'])
        print(c,end=" ")
        output.write(str(c)+" ")
        
    print("\n")

    source.close()
    output.close()

def dechiffrer_fichier():
    """
        presque la meme chose que chiffrer_fichier
    """
    print("Saisissez le nom d'un fichier : ", end="")
    fic = str(input())

    source = open(fic, "r")
    output = open("texte_brut-"+fic, "w")

    print("Message dechiffre dans "+fic+" : ",end="")
    for line in source:        
        for word in line.split():        
            m = fast_exp(int(word),bob['d'],bob['n'])
            print(chr(m),end="")
            output.write(chr(m))
    print("\n")

    source.close()
    output.close()

def afficher_fichier():
    print("Saisissez le nom d'un fichier : ", end="")
    fic = str(input())

    source = open(fic, "r")

    for line in source:        
        for word in line.split():        
            print(word, end="")
        print()

    source.close()
