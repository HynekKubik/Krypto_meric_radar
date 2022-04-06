
#!/usr/bin/env python3
from Crypto import*
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import base64



def generate_keys():
    modulus_length = 2048

    key = RSA.generate(modulus_length)
    #print (key.exportKey())

    pub_key = key.publickey()
    #print (pub_key.exportKey())
    session_key = get_random_bytes(16)
    return key, pub_key, session_key
####stare
def enc(file, pub_key, ses_key):
    #file = "/home/hynek/Obrázky/Snímek obrazovky pořízený 2021-12-01 21-04-26.png"
    with open(file, "rb") as f:
        data = f.read()
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(pub_key)
    enc_session_key = cipher_rsa.encrypt(ses_key)
    #file = file + "encrypted_data.bin"
    file_out = open(file, "wb")
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(ses_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()

    return enc_session_key, file
def dec(file, enc_session_key, private_key):
    file_in = open(file, "rb")
    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    print(ciphertext)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    #file = file.strip("encrypted_data.bin")
    with open(file, 'wb') as fo:
        fo.write(data)

def menuAesRsa(file_name):
  private, public, sesKey = generate_keys()
  enc_session_key, file = enc(file_name,public,sesKey)
  dec(file,enc_session_key,private)


#menu("/home/hynek/Obrázky/pokus/1.png")