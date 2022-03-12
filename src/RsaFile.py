#!/usr/bin/python3

import rsa
import glob
import os.path

#4096 ----501
#2048 ----245
#1024 ----117


def generate_keys():
    (pubKey, privKey) = rsa.newkeys(2048)
    key_file = get_path_keys()
    with open(key_file + '/keys/pubkey.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open(key_file + '/keys/privkey.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

def load_keys():
    key_file = get_path_keys()
    with open(key_file + '/keys/pubkey.pem', 'rb') as f:
        pubKey = rsa.PublicKey.load_pkcs1(f.read())

    with open(key_file + '/keys/privkey.pem', 'rb') as f:
        privKey = rsa.PrivateKey.load_pkcs1(f.read())

    return pubKey, privKey

def encrypt(msg, key):
    return rsa.encrypt(msg, key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key)
    except:
        return False

def get_path_keys():
        root = os.getcwd()
        root = root.split("/")
        #print(root)
        if root[-1] == "src":
            root.pop()
            root = "/".join(root)
        return root
        #print(root)
# def sign_sha1(msg, key):
#     return rsa.sign(msg.encode('ascii'), key, 'SHA-1')
#
# def verify_sha1(msg, signature, key):
#     try:
#         return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
#     except:
#         return False

# generate_keys()
# pubKey, privKey = load_keys()
# path = "/home/hynek/Stažené/key.txt"
# with open(path, 'rb') as fo:
#     plaintext = fo.read()
# print(type(plaintext))
# #plaintext = input('Enter a message:')
# #plaintext = bytes(plaintext, 'ascii')
# print(type(plaintext))
# #plaintext= ''.join(format(ord(i), '08b') for i in plaintext)
# #print(type(plaintext))
# print(plaintext)
# #print(pubKey)
# # info = [plaintext[i:i+2] for i in range(0, len(plaintext), 117)]
# # print(len(info))
# # for i in info:
# ciphertext = encrypt(plaintext, pubKey)
#
# # signature = sign_sha1(plaintext, privKey)
#
# plaintext1 = decrypt(ciphertext, privKey)
#
# print(f'Cipher text: {ciphertext}')
# #print(f'Signature: {signature}')
#
# if plaintext == plaintext1:
#     print(f'Plain text: {plaintext}')
# else:
#     print('Could not decrypt the message.')

# if verify_sha1(plaintext, signature, pubKey):
#     print('Signature verified!')
# else:
#     print('Could not verify the message signature.')

def menu_RSA(filename):
    size = int(os.path.getsize(filename))
    if size < 2045:
        generate_keys()
        pubKey, privKey = load_keys()
        #path = "/home/hynek/Stažené/key.txt"
        with open(filename, 'rb') as fo:
            plaintext = fo.read()
        ciphertext = encrypt(plaintext, pubKey)
        plaintext1 = decrypt(ciphertext, privKey)
        #print("ok")
        if plaintext != plaintext1:
            print("RSA faild")

    else:
        print("to big file")

#menu("/home/hynek/Stažené/key.txt")
#get_path_keys()
