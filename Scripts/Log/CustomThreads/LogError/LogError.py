import os
import sys
from CustomThreads.groups import parametres
from CustomThreads.Utils.Utils_function import write_data
from CustomThreads.Utils.Utils_function import check_dir

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS

CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
FILE_NAME_ERROR = par.FILE_NAME_ERROR

CHAR_REPORT_SPLIT = par.CHAR_REPORT_SPLIT  # \t


def logErr(self, timestamp, id_user, Phase, Actor, CODError, Payload):
    path_user = PATH_DATA_USERS + "/" + id_user

    # check if exists a user dir -> if not create it
    check_dir(path_user)

    # save the data
    path_file_name = path_user + "/" + FILE_NAME_ERROR

    #timestamp  Phase   From    To  CODError    Payload
    data = str(timestamp) + CHAR_REPORT_SPLIT +\
           str(Phase) + CHAR_REPORT_SPLIT + \
           str(Actor) + CHAR_REPORT_SPLIT + \
           str(CODError) + CHAR_REPORT_SPLIT + \
           str(Payload) + "\n"

    # flush data
    write_data(path_file_name, data)

    print "     Client at " + str(self.clientAddress) + " disconnected..."
