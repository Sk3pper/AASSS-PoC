import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import binascii
import base64
from Crypto import Random
from pbkdf2 import PBKDF2

'''
binascii.a2b_hex(hexstr): Return the binary data represented by the hexadecimal string hexstr.

'''
ITERATION = 100
BLOCK_SIZE = 16
def AES_encrypt(key, plaintext):
    # salt_test = "4c1e7a5026cf6bb72170c61de1d87b09"
    salt_bin_random = Random.new().read(BLOCK_SIZE)
    salt_hex = binascii.b2a_hex(salt_bin_random)

    # iv_test = "41d5e2a12d26661a3c06f5aafcdced3a"
    IV_bin_random = Random.new().read(BLOCK_SIZE)
    IV_hex = binascii.b2a_hex(IV_bin_random)

    key_bin = PBKDF2(key, salt_bin_random, iterations=ITERATION).read(32)  # 256-bit key
    key_hex = binascii.b2a_hex(key_bin)

    # create cipher
    cipher = Cipher(algorithms.AES(key_bin), modes.CBC(IV_bin_random), backend=default_backend())
    e = cipher.encryptor()

    # padding the plaintext
    padding_message = padding.PKCS7(128).padder()
    padded_message = padding_message.update(plaintext) + padding_message.finalize()

    # print "padded_message: " + padded_message

    ct = e.update(padded_message) + e.finalize()
    ciphertext_base64 = binascii.b2a_base64(ct)[:-len("\n")]

    print "key_hex: "+key_hex
    print "salt_hex: "+salt_hex
    print "iv_test: "+IV_hex
    print "ciphertext_base64: "+ciphertext_base64
    transitmessage = str(salt_hex) + str(IV_hex) + str(ciphertext_base64)
    print "transitmessage: "+transitmessage

    return transitmessage


def AES_decrypt(key, ciphertext):
    salt_hex = ciphertext[0:32]
    iv_hex = ciphertext[32:64]
    ciphertext_base64 = ciphertext[64:len(ciphertext)]

    salt_bin = binascii.a2b_hex(salt_hex)
    iv_bin = binascii.a2b_hex(iv_hex)
    ciphertext_bin = base64.b64decode(ciphertext_base64)
    key_bin = PBKDF2(key, salt_bin, iterations=ITERATION).read(32)  # 256-bit key
    key_hex = binascii.b2a_hex(key_bin)

    print "key_hex: "+key_hex
    print "salt_hex: " + salt_hex
    print "iv_hex: " + iv_hex
    print "ciphertext_base64: " + ciphertext_base64

    # construct a decryptor with the IV and key
    cipher = Cipher(algorithms.AES(key_bin), modes.CBC(iv_bin), backend=default_backend())
    d = cipher.decryptor()

    # get the (padded) plaintext out
    padded_plaintext = d.update(ciphertext_bin) + d.finalize()

    # remove the padding to get the original plaintext
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    print "plaintext: "+plaintext
    return plaintext
    # return str(plaintext+"3")

# example of usage
if __name__ == "__main__":

    key = "6917524648341986992"
    plaintext = "425782||s5Wr/UirHuyb8j2u76ZP2/1ny3/Ub7YXb63ZnLSL4GY=||+YAMiFI/2ypW2ZHst27avw=="
    print "key: " + key + "    plaintext: "+plaintext

    ciphertext = AES_encrypt(key, plaintext)
    # ciphertext ="bc539b975faba14443ea7419de537b199fab2eec6fbe9483c4acfa25def9bde17bYnLVnZXQwBPBZH4o3l9slkw5tJlYu9pbLUYPIhvLN9XjrViQwKjiTzWe3BXI/qVIUiCp20SjkYsamkw+YI7Lijc1d2Z0FTNIK2161lhLFLVWDTSEmDha4J7cVlsqAd"
    print "\n"
    AES_decrypt(key, ciphertext)