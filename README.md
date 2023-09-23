# 2IN013_RSA-based-broadcast-encryption

The dissemination of encrypted data (using public key encryption) allows for the creation of a unique and compact ciphertext for a set of recipients so that only legitimate recipients can decrypt this text independently and without interactions. In 2022, Sigurd Eskeland proposed such a system for the dissemination of encrypted data based on the RSA primitive. The objective of this project was first to understand how the RSA primitive works and how Eskeland's system operates. In a second phase, we analyzed the security of Eskeland's system and succeded to find attacks that could recover all or part of the decryption keys or information about certain ciphertexts. These attacks were implemented to demonstrate their effectiveness in practice.

To run certain programs it is required to install 

    pip3 install rsa
    pip3 install pycryptodome
    pip3 install sympy
    sudo apt install sagemath
    pip3 install sage

Execution

    Additionnally it is best to run the main program main.py from the "scr/" folder
    After generating multiple setup configurations, to test the continued fractions attack one needs to execute the "test_continue_fractions.py" file from the "src/" folder

Made by

	David Pulido Cornejo
	Kevin Huang
	Lounes Douar

Suppervised by 

	Damiend Vergnaud PhD

Sorbonne Universié

Sigurd Eskeland. Collusion-resistant Broadcast Encryption based on Hidden RSA Subgroups. In Proceedings of the 19th International Conference on Security and Cryptography - SECRYPT, 291-298, 2022 , Lisbon, Portugal.
