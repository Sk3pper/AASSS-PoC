import hashlib
import os
from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.Utils.Utils_function import write_data, check_dir

# load group
g2048 = MODP2048()
par = parametres()

COD200 = par.COD200
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_REPORT_MSG = par.FILE_NAME_REPORT_MSG

CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_REPORT_SPLIT = par.CHAR_REPORT_SPLIT

END_MESSAGES = par.END_MESSAGES


def logMsg(self, timestamp, From, To, Payload, Phase, id_user):
    path_user = PATH_DATA_USERS + "/" + id_user

    # check if exists a user dir -> if not create it
    check_dir(path_user)

    # save the data
    path_file_name = path_user + "/" + FILE_NAME_REPORT_MSG

    # this is made in order to understand when a phase is finish
    if Payload != END_MESSAGES:
        data = str(timestamp) + CHAR_REPORT_SPLIT + str(Phase) + CHAR_REPORT_SPLIT + str(From) + CHAR_REPORT_SPLIT + str(To) + CHAR_REPORT_SPLIT +\
               str(Payload) + CHAR_REPORT_SPLIT + "\n"
    else:
        data = "\n\n\n"

    # flush data
    write_data(path_file_name, data)

    print "     Client at " + str(self.clientAddress) + " disconnected..."


