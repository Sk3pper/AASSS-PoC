
# load group
import random
import socket
import sys

from aesCustomKey import AES_encrypt
from groups import MODP2048, parametres

g2048 = MODP2048()
par = parametres()


# take a number and compute (g^s g^r mod q)
def sPrime(s, p, q, g, h):
    s_int = strToInt(s)
    r = genRand(g2048.MAX_COORDINATE)
    sPr = pedersenModq(s_int, r, p, q, g, h)
    return sPr, r


def strToInt(s):
    n = len(s)
    f = 0
    for i in range(n):
        f += encode(s[i]) * (94 ** (n - i - 1))  # create integer from base 94 string (characters)
    return f


def encode(c):
    x = ord(c)
    if x > 32 and x < 127:
        return x - 33
    print("Sorry, I can only handle standard ASCII characters 33-126!")
    exit(1)


def split(data, char):
    return data.split(char)


# restituisce (g^m mod p)*(g^r mod p) mod p
def pedersenModq(m, r, p, q, g, h):
    # print "S': "+str(m)
    # print "r : "+str(r)
    # print "g^s' mod q: "+str(pow(g2048.g, m, g2048.q))
    # print "h^r mod q: " + str(pow(g2048.h, r, g2048.q))
    return (pow(g, m, q) * pow(h, r, q)) % q


# dato un numero max, restituisce un numero compreso tra 1-m
def genRand(m):
    return random.SystemRandom().randint(1, m)


def computeMC(s_prime, p, q, g, h):
    r_prime = genRand(g2048.MAX_COORDINATE)
    MC_before = pedersenModq(s_prime, r_prime,p, q, g, h)
    # print "         MC_beforeEnc = (g^S' h^r')mod q= " + str(MC_before) + "     r'=" + str(r_prime)
    k = str(genRand(sys.maxint))
    # pass message to encypt with that key
    MC = AES_encrypt(k, str(MC_before))

    return MC, k, r_prime, MC_before


def computeEms(MS, k, MC_beforeEnc):
    # print "                     data to encrypt with key as MS: k= "+str(k)+" MC_beforeEnc="+str(MC_beforeEnc)
    data = str(MC_beforeEnc)+par.CHAR_DATA_SPLIT+str(k)

    # pass message to encypt with that key
    Ems = AES_encrypt(MS, str(data))

    return Ems


# send out_data to IP,PORT and wait reply
def contactActor(IP, PORT, out_data):
    print "          Send to " + IP  # + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.sendall(bytes(out_data).encode("utf-8"))
    # print "SIZE: "+str(len(out_data.encode("utf-8")))
    in_data = client.recv(14096)
    print "          From " + IP  # + ": " + str(in_data.decode())
    return in_data