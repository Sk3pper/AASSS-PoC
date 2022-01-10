import hashlib
import os

from  CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.Utils.Utils_function import logMsg, logError

# load group
g2048 = MODP2048()
par = parametres()

PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT

COD100 = par.COD100
COD200 = par.COD200
COD400 = par.COD400
COD450 = par.COD450

# NEW CODES
COD700 = par.COD700  # x_i given to the SHAREHOLDER is not right --> deaelr compromised? (1)
COD700_desc = par.COD700_desc
COD750 = par.COD750 # (s_i,t_i) given to the SHAREHOLDER is not consistent --> dealer compromised sharing? (2)
COD750_desc = par.COD750_desc
COD760 = par.COD760  # user_id is not present --> you have to pass to signup before
COD760_desc = par.COD760_desc

COD444 = par.COD444 # Generale error
COD444_desc = par.COD444_desc


def reconstructionShareholder(self, x_i, id_user):
    print "     reconstructionShareholder"

    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_comm = path_user + "/" + FILE_NAME_COMM
    path_file_share = path_user + "/" + FILE_NAME_SHARE

    try:
        if not os.path.isdir(path_user):
            print "         ERROR, THE DIRECTORY OF USER DOES NOT EXIT, YOU HAVE TO DO SHARING PHASE BEFORE TO START WITH REC PHASE"
            msg = COD760 + CHAR_DATA_SPLIT + COD760_desc

            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "Shareholder", COD760, COD760_desc, id_user)

        else:
            # take informations saved
            print "     path_file_comm: " + path_file_comm
            print "     path_file_share: " + path_file_share

            # read files and extract the informations, take the last penultimate-line,
            # because the last-line is the \n char
            Commitments = readIntPenultimeLine(path_file_comm, False)
            print "     Commitments:" + str(Commitments)

            share_info = readIntPenultimeLine(path_file_share, True)
            s_i = share_info[0]
            t_i = share_info[1]
            hx_i = share_info[2]
            print "     share_info: " + str(share_info)

            # check se h(x_i) == h(x_i) se si:
            hash = hashlib.sha256()
            hash.update(str(x_i))
            print "     hash.hexdigest()=" + str(hash.hexdigest())

            if hash.hexdigest() == hx_i:
                # Use pedersen formula
                check = pedersenVerify(x_i, s_i, t_i, Commitments)

                if check:
                    print "\n     the given coordinate x_i is CORRECT, send back s_i and t_i"
                    # s_i = 13
                    msg = COD200 + CHAR_DATA_SPLIT + str(s_i) + CHAR_DATA_SPLIT + str(t_i)
                else:
                    print "     ERRORE the coordinate shares(s_i and t_i) given to me is not coerent"
                    msg = COD750 + CHAR_DATA_SPLIT + COD750_desc

                    # Log error Phase, Actor, CODError, Payload,  id_user
                    logError("SHARING", "Shareholder", COD750, COD750_desc, id_user)

            else:
                print "     ERRORE x_i != hx_i"
                msg = COD700 + CHAR_DATA_SPLIT + COD700_desc

                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("SHARING", "Shareholder", COD700, COD700_desc, id_user)

    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc

        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "Shareholder", COD444, payload, id_user)

    # Log the message (From, To, Payload, Phase, id_user)
    logMsg("Shareholder", "Dealer", msg, "RECONSTRUCTION", id_user)

    self.csocket.send((bytes(msg).encode("utf-8")))

    print "     Client at " + str(self.clientAddress) + " disconnected..."


def readPenultimeLine(pathFiletoRead):  # read a text file as a list of lines
    # find the last line, change to a file you have
    fileHandle = open(pathFiletoRead, "r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    return lineList[len(lineList) - 1]
    # or simply
    # return lineList[-1]


def readIntPenultimeLine(pathFiletoRead, hash):
    data = split(readPenultimeLine(pathFiletoRead), CHAR_DATA_SPLIT)
    data[len(data) - 1] = data[len(data) - 1][:-1]
    newIntData = []

    if not hash:
        for d in data:
            newIntData.append(int(d))
    else:
        for i in range(0, len(data) - 1):
            newIntData.append(int(data[i]))

        newIntData.append(data[len(data) - 1])
    # print "newIntData:"+str(newIntData)
    return newIntData


def pedersenCommit(m, r):
    return (pow(g2048.g, m, g2048.p) * pow(g2048.h, r, g2048.p)) % g2048.p


# Verify a Pedersen share: we need x_i, s_i,t_i and commitments
def pedersenVerify(xi, share, t_share, Commitments):
    # compute g^si h^ti mod p
    # print "\n     Compute g^si h^ti mod p"
    v = pedersenCommit(share, t_share)
    print "     share: " + str(share) + " t-share: " + str(t_share) + " x_i: " + str(xi)
    print "     g^si h^ti mod p = " + str(v)

    # print "\n     Compute produttoria"
    result = 1
    for j in range(len(Commitments)):
        result = (result * pow(Commitments[j], xi ** j, g2048.p)) % g2048.p

    print "     produttoria: " + str(result)
    return v == result


def split(data, char):
    return data.split(char)
