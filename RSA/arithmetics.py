#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import *
from random import *

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

def millerRabin(n):
    """
        Cryptography Made Simple, Algorithm 2.2 page 30
        True : Composite
        False : Probably prime
    """
    s = 0
    m = n - 1

    while m % 2 == 0:
        s += 1
        m //= 2
    
    k = 20     #k >= 20
    for j in range(0, k):
        a = randint(2, n - 2) % n
        b = fast_exp(a, m, n)
        if b != 1 and b != (n-1):
            i = 1
            while i < s and b != (n-1):
                b = b*b % n 
                if b == 1:
                    return True
                i += 1
            if b != (n-1):
                return True
    return False

def get_prime_range(lowerBound, upperBound):
    """
        Genere nombre premier entre lowerBound et upperBound
    """
    p = 0
    while True:
        p = randint(lowerBound, upperBound)
        if not millerRabin(p):
            break
    
    return p

def get_prime_digits(n):
    """
        Genere un nombre premiere de n chiffres
    """
    lowerBound = 10**n
    upperBound = lowerBound * 10
    return get_prime_range(lowerBound, upperBound)

def get_prime_bits(n):
    return get_prime_range(2 ** (n - 1),2 ** n)

def pgcd(a,b):
    if (b == 0):
        return a
    return pgcd(b, a%b)

def get_invertible(phi):
    """
        Trouve un nombre inversible modulo phi
    """
    for i in range(3, phi):
        if (pgcd(i,phi) == 1):
            return i
    return -1


    
