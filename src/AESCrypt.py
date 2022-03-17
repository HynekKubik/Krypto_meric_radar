
#!/usr/bin/python3
import sys
import os
import argparse
import signal
import getpass
import base64
import hashlib
import random
import string
from src.AES import AES


SALT_LEN = 64
BLOCK_LEN = 16
KEY_LEN = 32


def error(msg): sys.exit(msg)


def get_file_content(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except IOError:
        error('Unable to open the specified file')


def write_file(filename, content):
    try:
        with open(filename, 'wb+') as f:
            f.write(content)
    except IOError:
        error('Unable to write to file')


def derive_key(password: bytes, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac(
        hash_name='sha512',
        password=password,
        salt=salt,
        iterations=100000,
        dklen=KEY_LEN
    )
    return key


def sigint_handler(_, __):
    print("\r" + (' ' * 80) + "\rGood bye ☺️")
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)


def interactive_mode(aes):
    exit("Interactive mode is currently not supported, please specify an input file")


def decrypt(data, password):
    data = base64.b64decode(data)
    salt, iv, ciphertext = data[:SALT_LEN], data[SALT_LEN:SALT_LEN + BLOCK_LEN], data[SALT_LEN+BLOCK_LEN:]
    return AES(derive_key(password.encode(), salt)).decrypt(ciphertext, iv)


def encrypt(data, password):
    salt = os.urandom(64)
    ciphertext, iv = AES(derive_key(password.encode(), salt)).encrypt(data)
    return base64.b64encode(salt + iv + ciphertext)


def file_mode(password, args):
    data = get_file_content(args.f)
    if args.d:
        res = decrypt(data, password)
    else:
        res = encrypt(data, password)
    outfile = args.f if not args.o else args.o
    write_file(outfile, res)


def menu_AES_basic(file):
    password = get_random_string_password(32)
    num = 1
    data = get_file_content(file)

    res = encrypt(data, password)
    outfile = file
    write_file(outfile, res)
    data = get_file_content(file)
    res = decrypt(data, password)
    outfile = file
    write_file(outfile, res)

def get_random_string_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))

    return password


