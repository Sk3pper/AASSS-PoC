import os
import random
import socket

import datetime
from CustomThreads.groups import parametres

par = parametres()
BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES


IP_LOG = par.IP_LOG
PORT_LOG = par.PORT_LOG

CHAR_LOG_DATA_SPLIT = par.CHAR_LOG_DATA_SPLIT
CHAR_LOG_MSG_SPLIT = par.CHAR_LOG_MSG_SPLIT
WHICH_LOG = par.WHICH_LOG
DELIM_LOG = par.DELIM_LOG

# scrive i dati in un file
# se presente gli appende
# se non presente crea il file da zero
def write_data(path_file_name, data):
    """
    :type path_file_name: str
    :type data: str
    """
    # file does not exist
    if not os.path.isfile(path_file_name):
        with open(path_file_name, "w+") as f:
            f.write(data)
            print "     " + str(data[:-1]) + " are saved in path:" + path_file_name
            return True
    # file exists
    else:
        with open(path_file_name, "a") as f:
            f.write(data)
            print "     " + str(data[:-1]) + " are saved in path:" + path_file_name
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

# dato un numero max, restituisce un numero compreso tra 1-m
def genRand(m):
    return random.SystemRandom().randint(1, m)


def readPenultimeLine(pathFiletoRead):  # read a text file as a list of lines
    # find the last line, change to a file you have
    fileHandle = open(pathFiletoRead, "r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    return lineList[len(lineList) - 1]
    # or simply
    # return lineList[-1]


def split(data, char):
    return data.split(char)

def strToIntList(list):
    newDataInt = []
    for l in list:
        newDataInt.append(int(l))

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
               str(id_user)+ DELIM_LOG

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