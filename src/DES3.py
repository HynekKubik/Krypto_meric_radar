from Crypto.Cipher import DES3
from hashlib import md5
import string
import random

def get_random_string_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def encrypt(file, key):
    hashed_key = md5(key.encode('ascii')).digest()
    key_3des = DES3.adjust_key_parity(hashed_key)
    cipher = DES3.new(key_3des, DES3.MODE_EAX, nonce=b'0')

    with open(file, 'rb') as input_file:
        file_bytes = input_file.read()
        enc_bytes = cipher.encrypt(file_bytes)
    with open(file, 'wb') as output_file:
        output_file.write(enc_bytes)

def decrypt(file, key):
    hashed_key = md5(key.encode('ascii')).digest()
    key_3des = DES3.adjust_key_parity(hashed_key)
    cipher = DES3.new(key_3des, DES3.MODE_EAX, nonce=b'0')
    with open(file, 'rb') as input_file:
        file_bytes = input_file.read()
        dec_bytes = cipher.decrypt(file_bytes)
    with open(file, 'wb') as output_file:
        output_file.write(dec_bytes)

def menu_3_DES(file):
    key = get_random_string_password(168)
    encrypt(file,key)
    decrypt(file,key)

# menu_3_DES("/home/hynek/Obrázky/pokus/pokus/1.png")