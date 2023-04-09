#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arithmetics import *
from broadcast_encryption import *
from attack import *

loaded_data = {}

def menu():
    print("1. Load session (files stored at tests/*.log)")
    print("2. Regenerate numbers")
    print("q to quit")

def regen():
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
        menu()
        o = input()
        if int(o) == 1:
            print("Filename : (si les fichiers sont dans le repertoire logs, n'oubliez pas d'ajouter ../logs/ avant le nom du fichier) ",end="")
            file_name = input()
            private_keys, public_keys, lam, N, n = retrieve_data(file_name)
            if (private_keys != None):
                break
            else:
                print("File",file_name,"does not exist !")
        elif int(o) == 2:
            #print("Select number of users :")
            #N = int(input())
            private_keys, public_keys, lam, N, n = regen()
            break
        elif o == "q":
            break
    
    print("\nSetting up 4-sk attack...")
    gamma = get_gamma_4sk(private_keys[:4], public_keys, lam, N, n)

    
