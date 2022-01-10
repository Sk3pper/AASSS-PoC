import os
import socket

import datetime
from CustomThreads.groups import parametres
from CustomThreads.PedersenUtilities.VSS import genRand
from CustomThreads.groups import MODP2048


# load group
g2048 = MODP2048()
par = parametres()

CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
PATH_DATA_USERS = par.PATH_DATA_USERS
CHAR_COORD_SPLIT = par.CHAR_COORD_SPLIT
WHICH_PHASE = par.WHICH_PHASE

FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
FILE_NAME_NW_INFORMATION = par.FILE_NAME_NW_INFORMATION
FILE_NAME_MC = par.FILE_NAME_MC

IP_SHAREHOLDERS = par.IP_SHAREHOLDERS
PORT_SHAREHOLDERS = par.PORT_SHAREHOLDERS

PORT_EXTERNAL_SERVER = par.PORT_EXTERNAL_SERVER
IP_EXTERNAL_SERVER = par.IP_EXTERNAL_SERVER

IP_LOG = par.IP_LOG
PORT_LOG = par.PORT_LOG

CHAR_LOG_DATA_SPLIT = par.CHAR_LOG_DATA_SPLIT
CHAR_LOG_MSG_SPLIT = par.CHAR_LOG_MSG_SPLIT
DELIM_LOG = par. DELIM_LOG

COD200 = par.COD200  # every is went well
COD300 = par.COD300  # saving is not went well
COD400 = par.COD400  # xi != h(xi)
COD450 = par.COD450  # (s_i,t_i) given by DEALER TO SHAREHOLDER is not consistent with commitments
COD500 = par.COD500  # (s_i,t_i) given by SHAREHOLDER TO DEALER is not consistent with commitments
COD550 = par.COD550  # S' != \overline(S')
COD999 = par.COD999  # error in SHA1-ExternalServer
COD888 = par.COD888  # error in REC1 ES

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES

WHICH_LOG = par.WHICH_LOG

def write_data(path_file_name, data):
    """
    :type path_file_name: str
    :type data: str
    """
    # file does not exist
    if not os.path.isfile(path_file_name):
        with open(path_file_name, "w+") as f:
            f.write(data)
            print "     " + str(data[:-2]) + " are saved in path:" + path_file_name
            return True
    # file exists
    else:
        with open(path_file_name, "a") as f:
            f.write(data)
            print "     " + str(data[:-2]) + " are saved in path:" + path_file_name
            return True


# check if exists a user dir -> if not create it
def check_dir(path_user):
    if not os.path.isdir(path_user):
        os.makedirs(path_user)


def send_data(IP, PORT, out_data):
    print "          For " + IP + ": " + " out_data = " + out_data

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    client.sendall(bytes(out_data).encode("utf-8"))
    in_data = client.recv(BUFFER_SIZE_REQUEST_MESSAGES)
    print "          From " + IP + ": " + str(in_data.decode())

    return in_data


def readPenultimeLine(pathFiletoRead):  # read a text file as a list of lines
    # find the last line, change to a file you have
    fileHandle = open(pathFiletoRead, "r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    return lineList[len(lineList) - 1]
    # or simply
    # return lineList[-1]

def readIntPenultimeLine(pathFiletoRead):
    data = split(readPenultimeLine(pathFiletoRead), CHAR_DATA_SPLIT)
    data[len(data) - 1] = data[len(data) - 1][:-1]
    newIntData = strToIntList(data)

    return newIntData


def computeCoordinate():
    coordinate = []
    for i in range(0, g2048.n):
        r = genRand(g2048.MAX_COORDINATE)
        while r in coordinate:
            r = genRand(g2048.MAX_COORDINATE)

        coordinate.append(r)
    coordinate.sort()

    str_coordinate = ""
    for xi in coordinate:
        str_coordinate = str_coordinate + str(xi) + CHAR_COORD_SPLIT

    str_coordinate = str_coordinate[:-len(CHAR_COORD_SPLIT)]

    return str_coordinate


def split(data, char):
    return data.split(char)


def strToIntList(list):
    newDataInt = []
    for l in list:
        if l is not None:
            newDataInt.append(int(l))
        else:
            newDataInt.append(0)
    return newDataInt


def logMsg(From, To, Payload, Phase, id_user):
    timestamp = str(datetime.datetime.now())

    # timestamp, From, To, Payload, Phase, id_user
    out_data = WHICH_LOG[0] + CHAR_LOG_MSG_SPLIT + \
               str(timestamp) + CHAR_LOG_DATA_SPLIT + \
               str(From) + CHAR_LOG_DATA_SPLIT + \
               str(To) + CHAR_LOG_DATA_SPLIT + \
               str(Payload) + CHAR_LOG_DATA_SPLIT + \
               str(Phase) + CHAR_LOG_DATA_SPLIT + \
               str(id_user) + DELIM_LOG

    print "          Send to " + IP_LOG + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP_LOG, PORT_LOG))
    client.sendall(bytes(out_data).encode("utf-8"))
    client.close()


def logError(Phase, Actor, CODError, Payload,  id_user):
    #  ERROR-|-timestamp|-|Phase|-|Actor|-|CODError|-|Payload|-|id_user
    timestamp = str(datetime.datetime.now())

    # timestamp, From, To, Payload, Phase, id_user
    out_data = WHICH_LOG[1] + CHAR_LOG_MSG_SPLIT + \
               str(timestamp) + CHAR_LOG_DATA_SPLIT + \
               str(Phase) + CHAR_LOG_DATA_SPLIT + \
               str(Actor) + CHAR_LOG_DATA_SPLIT + \
               str(CODError) + CHAR_LOG_DATA_SPLIT + \
               str(Payload) + CHAR_LOG_DATA_SPLIT + \
               str(id_user) + DELIM_LOG

    print "          Send to " + IP_LOG + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP_LOG, PORT_LOG))
    client.sendall(bytes(out_data).encode("utf-8"))
    client.close()