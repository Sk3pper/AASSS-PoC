import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


class AESCipher:
    def __init__(self, key):
        # self.key = key
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

# example of usage
if __name__ == "__main__":
    kPrime = "5454"
    # set the key
    cipher = AESCipher(kPrime)
    # pass message to encypt with that key
    encrypted = cipher.encrypt('sto usando AES 256!')

    # decrypt the message
    decrypted = cipher.decrypt(encrypted)
    print encrypted
    print decrypted
