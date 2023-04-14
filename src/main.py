#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arithmetics import *
from broadcast_encryption import *
from attack import *

loaded_data = {}

def menu(n):
    if n == 1:
        print("Attention : si les fichiers de teste sont dans le repertoire logs, n'oubliez pas d'ajouter ../logs/ avant le nom du fichier !")
        print("1. Load session (files stored at tests/*.log)")
        print("2. Regenerate numbers")
        print("q to quit")
    elif n == 2:
        print("Select attack type")
        print("1. 4-sk")
        print("2. 2-sk")
        print("q to quit")

def regen(N, lam):
    #Exemple d'utilisation
    print("Setting up...")
    (public_keys, n), private_keys = Setup(N, lam)
    #target users
    T = [0, 1]
    print("Generating encryption key and header...")
    kT, z = Enc(public_keys, T, N, n)
    print("k_T :",kT)
    print("z :",z)
    print("Decrypting header...")
    decrypted_kT = Dec(private_keys[T[-1]], z, n)
    if (kT == decrypted_kT):
        print("Keys match")
    else:
        print("Keys don't match")
    return private_keys, public_keys, lam, N, n

def retrieve_data(file_name):
    global loaded_data
    try:
        with open(file_name, 'r') as fp:
            loaded_data = json.load(fp)
        public_keys = (loaded_data["g_i"], loaded_data["y_i"])
        private_keys = loaded_data["gamma_i"]
        lam = loaded_data["lam"]
        N = loaded_data["N"]
        n = loaded_data["n"]
        return private_keys, public_keys, lam, N, n
    except:
        return None, None, None, None, None

if __name__ == "__main__":
    private_keys = None
    public_keys = None
    lam = None
    N = None 
    n = None

    while True:
        menu(1)
        o = input()
        if o == "1":
            print("Filename : ",end="")
            file_name = input()
            private_keys, public_keys, lam, N, n = retrieve_data(file_name)
            if (private_keys != None):
                print("Files loaded successfully...")
                break
            else:
                print("File",file_name,"does not exist !")
        elif o == "2":
            print("Select number of users [1,100], (8 par defaut) : ",end="")
            N = int(input())
            print("Lambda, (80 par defaut) : ",end="")
            lam = int(input())
            private_keys, public_keys, lam, N, n = regen(N, lam)
            break
        elif o == "q":
            break
    
    while True:
        menu(2)
        o = input()
        if o == "1":
            print("\nSetting up 4-sk attack...")
            gamma = get_gamma_4sk(private_keys[:4], public_keys, lam, N, n)
        elif o == "2":
            print("\nSetting up 2-sk attack...")
            gamma = get_gamma_2sk(private_keys[:2], public_keys, lam, N, n)
        elif o == "q":
            break
    

    
