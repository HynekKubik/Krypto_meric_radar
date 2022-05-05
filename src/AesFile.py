#!/usr/bin/python3

import Crypto
from Crypto import *
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        # key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
        # enc = Encryptor(key)
        self.key = key

        #menu()


    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        size = str(os.path.getsize(file_name))
        print(size)
        enc = self.encrypt(plaintext, self.key)
        with open(file_name, 'wb') as fo:
            fo.write(enc)
        #size = str(os.path.getsize(file_name + ".enc"))
        print(size)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name, 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)







#clear = lambda: os.system('cls')
def menu_AES(file):
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encryptor(key)
    enc.encrypt_file(str(file))
    #file = file + ".enc"
    enc.decrypt_file(str(file))
    # while True:
    #     #clear()
    #     choice = int(input(
    #         "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
    #     #clear()
    #     if choice == 1:
    #         enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
    #     elif choice == 2:
    #         enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
    #     elif choice == 3:
    #         enc.encrypt_all_files()
    #     elif choice == 4:
    #         enc.decrypt_all_files()
    #     elif choice == 5:
    #         exit()
    #     else:
    #         print("Please select a valid option!")

# path = "/home/hynek/Stažené/landscape-of-mountains-and-forest-4k-vaporwave.jpg"
# menu(path)
