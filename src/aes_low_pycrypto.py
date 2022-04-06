from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



def aes(file):
    with open(file, "rb") as f:
        data = f.read()

    #data = b'secret data'
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    print(type(data))
    ciphertext, tag = cipher.encrypt_and_digest(data)

    file_out = open(file, "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()
    # with open(file, "wb") as f:
    #     wr = f.write(ciphertext)

    file_in = open(file, "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]

    # let's assume that the key is somehow available again
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file, "wb") as f:
        wr = f.write(data)


#aes("/home/hynek/Dokumenty/encription.txt")
