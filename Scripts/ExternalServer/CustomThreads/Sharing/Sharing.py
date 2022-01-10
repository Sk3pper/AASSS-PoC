import os

import sys
from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.aesCustomKey import AES_encrypt, AES_decrypt
from CustomThreads.Utils.Utils_function import write_data, send_data, check_dir, genRand, readPenultimeLine, split
from CustomThreads.Utils.Utils_function import logMsg, logError

# load group
g2048 = MODP2048()

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_INFORMATION = par.FILE_NAME_INFORMATION
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
debug = par.DEBUG

COD200 = par.COD200

COD300 = par.COD300  # Problem while ES was computing E_k'[MC] because MC!=D_k'[MS]
COD300_desc = par.COD300_desc

COD150 = par.COD150  # User already signed-up [External Server]
COD150_desc = par.COD150_desc

COD170 = par.COD170  # User_id is not present -> Dealer did not contact me or client is anticipating the steps
COD170_desc = par.COD170_desc

COD400 = par.COD400  # MC_from_client != MC_from_Dealer
COD400_desc = par.COD400_desc

COD444 = par.COD444  # Generale error
COD444_desc = par.COD444_desc

DELIM = par.DELIM


# called from Dealer
def sharing1ES(self, MC, id_user):
    print "     __sharing1"
    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_name = path_user + "/" + FILE_NAME_INFORMATION
    msg = ''

    try:
        # check if the user is already signed-up
        if not os.path.isdir(path_user):  # the id_user is NOT present so it can signup
            # Computing MS = E_k'[MC]
            # random key
            k_prime = str(genRand(sys.maxint))
            # compute MS
            MS = AES_encrypt(k_prime, str(MC))
            print "     MS: " + str(MS)
            print "    k_prime: " + str(k_prime)
            # test if everything is went well
            # check that enc and dec working
            # decrypt the message
            MC_decrypt_kPrime = AES_decrypt(k_prime, MS)
            print "     MC_decrypt_kPrime: " + str(MC_decrypt_kPrime)
            print '     {"k_prime":"' + str(k_prime) + '","ciphertext":"' + str(MS) + '"}'

            if MC_decrypt_kPrime != MC:
                print "     ERROR: MC != Dk'[MS]: MC= " + str(MC) + " MS=" + str(MS) + " D_kPrime[MS]=" + str(
                    MC_decrypt_kPrime) + " kPrime=" + k_prime
                msg = COD300 + CHAR_DATA_SPLIT + COD300_desc

                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("SHARING", "ExternalServer", COD300, COD300_desc, id_user)
            else:
                data = str(MC) + CHAR_DATA_SPLIT + str(MS) + CHAR_DATA_SPLIT + str(k_prime) + "\n"
                # create the user_dir
                os.makedirs(path_user)

                # flush data
                write_data(path_file_name, data)

                msg = "The client now can contact me"
                msg = COD200 + CHAR_DATA_SPLIT + msg
        else:
            # user is already present --> double signup
            msg = COD150 + CHAR_DATA_SPLIT + COD150_desc
            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "ExternalServer", COD150, COD150_desc, id_user)

    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc

        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "ExternalServer", COD444, payload, id_user)

    # Log the message (From, To, Payload, Phase, id_user
    logMsg("ExternalServer", "Dealer", msg, "SHARING", id_user)

    # send back to the dealer
    self.csocket.send((bytes(msg).encode("utf-8")))
    print "     Client at " + str(self.clientAddress) + " disconnected..."


# called from CLIENT
def sharing2ES(self, MC_Client, id_user):
    print "     __sharing2"
    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_info = path_user + "/" + FILE_NAME_INFORMATION
    msg = ''

    try:
        # check if the direcory is presents
        if not os.path.isdir(path_user):
            print "\n     ERROR, THE DIRECTORY OF USER DOES NOT EXIT, YOU HAVE TO DO SHARING PHASE BEFORE TO START WITH REC PHASE"
            msg = COD170 + CHAR_DATA_SPLIT + COD170_desc
            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "ExternalServer", COD170, COD170_desc, id_user)
        else:
            # Extract the information from FILE_NAME_INFORMATION
            # Take the last penultimate-line, because the last-line is the \n char
            mc_ms_info = split(readPenultimeLine(path_file_info), CHAR_DATA_SPLIT)
            print "     mc_ms_info: " + str(mc_ms_info)

            MC_Dealer = mc_ms_info[0]
            MS = mc_ms_info[1]

            # check if MC_Client == MC_Dealer se si:
            print "     MC_Dealer: " + str(MC_Dealer) + "MC_Client: " + str(MC_Client)
            if str(MC_Client) == str(MC_Dealer):
                # set message
                msg = COD200 + CHAR_DATA_SPLIT + str(MS)
            else:
                print "     ERRORE MC_client != MC_dealer"
                # set message
                msg = COD400 + CHAR_DATA_SPLIT + COD400_desc

                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("SHARING", "ExternalServer", COD400, COD400_desc, id_user)

    except Exception as e:
        print "\n         General Error: " + e.message
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc
        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "ExternalServer", COD444, payload, id_user)

    # Log the message (From, To, Payload, Phase, id_user
    logMsg("ExternalServer", "Client", msg, "SHARING", id_user)

    # send back to the Client
    self.csocket.send((bytes(msg).encode("utf-8")))
    print "     Client at " + str(self.clientAddress) + " disconnected..."