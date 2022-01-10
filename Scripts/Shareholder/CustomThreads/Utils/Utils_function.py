import os
import socket

from CustomThreads.groups import parametres

par = parametres()
IP_LOG = par.IP_LOG
PORT_LOG = par.PORT_LOG

CHAR_LOG_DATA_SPLIT = par.CHAR_LOG_DATA_SPLIT
CHAR_LOG_MSG_SPLIT = par.CHAR_LOG_MSG_SPLIT

WHICH_LOG = par.WHICH_LOG
DELIM_LOG = par.DELIM_LOG

import datetime


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