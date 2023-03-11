from arithmetics import *
import os

alice = {'e' : 0, 'd' : 0, 'n' : 0}
bob = {'e' : 0, 'd' : 0, 'n' : 0}

def generate_key():
    p = get_prime_bits(1024)
    q = get_prime_bits(1024)
    n = p * q
    phi = (p - 1)*(q - 1)
    e = get_invertible(phi)
    try:
        d = fast_inverse(e,phi)
        return (n,e,d)
    except:
        print("Keygen error")
        print("p : ",p)
        print("q : ",q)
        print("n : ",n)
        print("phi:",phi)
        print("e : ",e)
        exit()

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