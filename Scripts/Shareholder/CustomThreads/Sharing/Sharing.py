import os
import sys
from CustomThreads.groups import parametres
from CustomThreads.Utils.Utils_function import write_data
from CustomThreads.Utils.Utils_function import check_dir
from CustomThreads.Utils.Utils_function import logMsg, logError

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE

CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT

COD200 = par.COD200
COD300 = par.COD300

COD500 = par.COD500 # User already signedup [Shareholder]
COD500_desc = par.COD500_desc

COD444 = par.COD444 # Generale error
COD444_desc = par.COD444_desc


def sharingShareholder(self, s_i, t_i, hx_i, id_user):
    print "     sharingShareholder"
    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_name = path_user + "/" + FILE_NAME_SHARE
    msg = ''

    try:
        # check if the user is already signed-up
        if not os.path.isdir(path_user):
            # the id_user is NOT present
            # create user_id dir
            os.makedirs(path_user)

        data = s_i + CHAR_DATA_SPLIT + t_i + CHAR_DATA_SPLIT + hx_i + "\n"

        # write into file
        write_data(path_file_name, data)

        # send back ACK
        msg = COD200 + CHAR_DATA_SPLIT + "share information saved"


    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD500 + CHAR_DATA_SPLIT + COD500_desc

        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD500 + " " + str(e)
        logError("SHARING", "Shareholder", COD500, payload, id_user)

    # Log message (From, To, Payload, Phase, id_user)
    logMsg("Shareholder", "Dealer", msg, "SHARING", id_user)



    self.csocket.send((bytes(msg).encode("utf-8")))
    print "     Client at " + str(self.clientAddress) + " disconnected..."
