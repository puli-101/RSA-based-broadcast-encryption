#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

P_A = 0
Q_A = 0
E_A = 1423
D_A = 1663530607
N_A = 2486660107

alice = {'p' : P_A, 'q' : Q_A, 'e' : E_A, 'd' : D_A, 'n' : N_A}

def fast_exp(x, n, mod):
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
    p %= mod
    for i in range(1, mod):
        if (i * p) % mod == 1
            return i
    return -1

def factor(n):
    for i in range(2,sqrt(n) + 1):
        if n % i == 0:
            return i
    return -1

def chiffrer_terminal():
    pass

def chiffrer_fichier():
    pass

def dechiffrer_fichier():
    pass

def afficher_fichier():
    pass

def afficher_fichier():
    pass