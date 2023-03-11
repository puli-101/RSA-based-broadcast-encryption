#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt
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


def chinese_remainder(alpha_p, alpha_q, p, q):
    """
        Algorithme associé au théorème chinois de restes
        on assume que p et q sont deux nombres premiers differents
    """
    return (alpha_p * q * get_inverse(q, p) + alpha_q * p * get_inverse(p,q)) % (p*q)

def get_inverse(a, p):
    """
        algorithme pour trouver l'inverse de a mod p où p est premier
    """
    return pow(a, p - 2, p)

def find_generator(p, primes = []):
    """
        etant donne p et la factorisation de phi(p) (la liste primes) on renvoie un generateur de Zp avec p premier > 2
        (normalement on connait deja la factorisation de phi(p) par le Setup)
        https://en.wikipedia.org/wiki/Primitive_root_modulo_n
    """
    if len(primes) == 0:
        primes = [2] + [i for i in range(3, p, 2) if (p - 1) % i == 0]
    def is_generator(g, phi, primes):
        for prime in primes:
            if pow(g, phi//prime, p) == 1:
                return False
        return True
    for g in range(2, p):
        if is_generator(g, p - 1, primes):
            return g