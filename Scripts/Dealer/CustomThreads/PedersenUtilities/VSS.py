import random

from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres

# load group
g2048 = MODP2048()
par = parametres()

debug = par.DEBUG


def genRand(m):
    return random.SystemRandom().randint(1, m)

def genRand2(m):
    return random.SystemRandom().randint(0, m)


# compute shares, t-shares and commits and cheks if everything was went well
def pedersenSharingChecked(sPrime, t, n, abscissa_vector=None):
    shares = None
    t_shares = None
    coordinates = None
    Commitments = None
    check = False

    while not check:
        shares, t_shares, Commitments, coordinates = pedersenSharing(sPrime, t, n, abscissa_vector)
        check_list = []
        print "\n     check the validity of shares and Commitments"
        for i in range(0, len(coordinates)):
            check_list.append(pedersenVerify(coordinates[i], shares[i+1], t_shares[i+1], Commitments))
        check = True
        for i in range(0, len(check_list)):
            check = check and check_list[i]

        print "          check:"+str(check)

        # (secure) shares without key!
        shares_without = shares[1:]
        t_shares_without = t_shares[1:]
        if debug:
            print "\n     shares_without: " + str(shares_without)
            print "     t_shares_without: " + str(t_shares_without)

        # recovery
        recovery_coord = []
        recovery_share = []
        recovery_t = []
        number = set()

        for i in range(0, g2048.t):
            # non posso prendere lo stesso numero
            r = genRand2(g2048.n-1)
            print "pre while"
            while r in number:
                r = genRand2(g2048.n-1)
            number.add(r)

            recovery_coord.append(coordinates[r])
            recovery_share.append(shares_without[r])
            recovery_t.append(t_shares_without[r])

        print "     number:"+str(number)
        if debug:
            print "\n     recovery_coord: " + str(recovery_coord)
            print "     recovery_share: " + str(recovery_share)
            print "     recovery_t: " + str(recovery_t)

        recoveredK = pedersenRecover(recovery_coord, recovery_share, recovery_t, Commitments)
        if debug:
            print "\n     recoveredK: " + str(recoveredK)
        if recoveredK == sPrime:
            if debug:
                print "     secret: " + str(sPrime) + " recoveredK: " + str(recoveredK) + "        True"
            check = check and True

        else:
            print "secret: " + str(sPrime) + " recoveredK: " + str(recoveredK) + "        False"
            check = check and False

    return shares[1:], t_shares[1:], Commitments, coordinates


# Compute shares,t-share and commits for Pedersen VSS
def pedersenSharing(k, t, n, abscissa_vector=None):
    # define a_i and b_i, terms of polynomials
    a = [k]
    b = [genRand(g2048.p)]
    for i in range(1, t):
        a.append(genRand(g2048.q))
        b.append(genRand(g2048.q))

    # define random coordinates:
    # the coordinates must be distinct
    coordinate = []
    if abscissa_vector == None:
        print "     abscissa_vector == None"
        for i in range(1, n + 1):
            r = genRand(g2048.MAX_COORDINATE)
            while r in coordinate:
                r = genRand(g2048.MAX_COORDINATE)

            coordinate.append(r)
        coordinate.sort()
    else:
        print "     abscissa_vector != None"
        coordinate = abscissa_vector
        coordinate.sort()
        print "     coordinate: " + str(coordinate)

    if debug:
        print "\n     Paramtres: "
        printList("     a_", "b_", "x_", a, b, coordinate)

    # compute shares
    if debug:
        print "\n     compute shares: "

    share = [k]
    t_share = [b[0]]
    i = 1
    print "     coordinate: "+str(coordinate)
    for c in coordinate:
        # for c in range(1, n + 1):
        share.append(poly(c, a))
        t_share.append(poly(c, b))
        if debug:
            print "          x_" + str(i) + "= " + str(c) + " share= " + str(share[i]) + " t-share= " + str(t_share[i])
        i += 1

    # compute commitments
    if debug:
        print "\n     compute commitments: "
    C = []
    for i in range(0, t):
        C.append(pedersenCommit(a[i], b[i]))
        if debug:
            print "          c_" + str(i) + "= " + str(C[i])
    return (share, t_share, C, coordinate)


# Verify a Pedersen share: we need x_i, s_i,t_i and commitments
def pedersenVerify(xi, share, t_share, Commitments):
    # compute g^si h^ti mod p
    # print "\n     Compute g^si h^ti mod p"
    v = pedersenCommit(share, t_share)

    result = 1
    for j in range(len(Commitments)):
        result = (result * pow(Commitments[j], xi ** j, g2048.p)) % g2048.p

    return v == result


# return a0 +a1x+a2x^2+...+a_t-1x^t-1
def poly(x, f):
    result = 0
    for i in range(len(f)):
        result += f[i] * pow(x, i, g2048.p)
    return result


def printList(s1, s2, s3, a, b, c):
    if debug:
        for i in range(0, len(a)):
            print "    " + s1 + str(i) + "= " + str(a[i]) + "       " + s2 + str(i) + "= " + str(
                b[i]) + "       " + s3 + str(i + 1) + "= " + str(c[i])

        for i in range(len(a), len(c)):
            print "                                        " + s3 + str(i + 1) + "= " + str(c[i])


# recover the Secret with pederse: check if the shares are consistent
def pedersenRecover(coordinates, shares, t, C):
    for i in range(len(coordinates)):
        if debug:
            print "          x_" + str(i) + "= " + str(coordinates[i]) + " share= " + str(shares[i]) + " t-share= " + str(t[i]) + " Commitments:" + str(C)
        if not pedersenVerify(coordinates[i], shares[i], t[i], C):
            if debug:
                print 'wrong share!'
            return 'wrong share!'
    if debug:
        print "     All shares are correct!"

    return sssRecover(coordinates, shares)


# sss Recover using Lagrange thereom t
def sssRecover(coordinates, shares):
    sommatoria = 0
    for j in range(len(coordinates)):
        v_j = 1
        for k in range(len(coordinates)):
            if k != j:
                v_j *= (coordinates[k] * pow(coordinates[k] - coordinates[j], g2048.p - 2, g2048.p)) % g2048.p
        s_j = shares[j]
        sommatoria += (s_j * v_j)
    return sommatoria % g2048.p



def pedersenCommit(m, r):
    return (pow(g2048.g, m, g2048.p) * pow(g2048.h, r, g2048.p)) % g2048.p
