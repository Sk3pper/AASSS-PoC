import random
import socket
import threading
import os
import sys
from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.aesCustomKey import AES_encrypt, AES_decrypt
from CustomThreads.Utils.Utils_function import write_data, send_data, check_dir, genRand, readPenultimeLine, split, \
    strToIntList
from CustomThreads.Utils.Utils_function import logMsg, logError

# load group
g2048 = MODP2048()
par = parametres()

CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
WHICH_PHASE = par.WHICH_PHASE

FILE_NAME_EMS = par.FILE_NAME_EMS
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_INFORMATION = par.FILE_NAME_INFORMATION
IP_DEALER = par.IP_DEALER
PORT_DEALER = par.PORT_DEALER

COD100 = par.COD100
COD200 = par.COD200
COD222 = par.COD222
COD333 = par.COD333

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES


# NEW CODES
COD900 = par.COD900
COD900_desc = par.COD900_desc

COD444 = par.COD444 # Generale error
COD444_desc = par.COD444_desc

COD930 = par.COD930  # E_MS_Dealer != E_MS_Client --> Dealer or Client is cheating(5a)
COD930_desc = par.COD930_desc
COD960 = par.COD960  # D_k[MC_given_inSHA] != pre_MC --> Client is cheating (5b)
COD960_desc = par.COD960_desc

DELIM = par.DELIM


def reconstructionES1(self, eMS_Dealer, id_user):
    print "     __reconstruction1"

    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_name = path_user + "/" + FILE_NAME_EMS

    try:
        if not os.path.isdir(path_user):
            print "ERROR, THE DIRECTORY OF USER DOES NOT EXIT, YOU HAVE TO DO SHARING PHASE BEFORE TO START WITH REC PHASE"
            msg = COD900 + CHAR_DATA_SPLIT + COD900_desc

            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("RECONSTRUCTION", "ExternalServer", COD900, COD900_desc, id_user)

        else:
            # sSecond||coordinate||mcPrime||eMS
            data = str(eMS_Dealer) + "\n"
            # flush data
            write_data(path_file_name, data)

            msg = "The client now can contact me"
            msg = COD200 + CHAR_DATA_SPLIT + msg

    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc
        payload = COD444_desc+ " "+str(e)
        # Log error Phase, Actor, CODError, Payload,  id_user
        logError("RECONSTRUCTION", "ExternalServer", COD444, payload, id_user)

    # Log messge (From, To, Payload, Phase, id_user)
    logMsg("ExternalServer", "Dealer", msg, "RECOSTRUCTION", id_user)

    self.csocket.send((bytes(msg).encode("utf-8")))

    print "     Client at " + str(self.clientAddress) + " disconnected..."

def retrieve_inf(path_user):
    
    #  si preleva eMS inviato dal dealer
    path_file_ems = path_user + "/" + FILE_NAME_EMS
    print "     path_file_ems: " + path_file_ems
    # read files and extract the informations, take the last penultimate-line, because the last-line is the \n char
    E_ms_Dealer = readPenultimeLine(path_file_ems)[:-len("\n")]
    print "     E_ms_Dealer:" + str(E_ms_Dealer)

    # si preleva k', MS e MC salvati durante la LogError phase
    path_file_info = path_user + "/" + FILE_NAME_INFORMATION
    print "     path_file_info: " + path_file_info
    # read files and extract the informations, take the last penultimate-line, because the last-line is the \n char
    info = readPenultimeLine(path_file_info)
    print "     info:" + str(info)
    data_splited = split(info, CHAR_DATA_SPLIT)
    # MC||MS||k'
    MC = data_splited[0]
    MS = data_splited[1]
    k_prime = data_splited[2][:-len("\n")]

    print "\n     MC: " + MC
    print "     MS: " + MS
    print "     k_prime: " + k_prime

    return E_ms_Dealer, MC, MS, k_prime,


def reconstructionES2(self, E_ms_Client, id_user):
    print "     __reconstruction2"
    path_user = PATH_DATA_USERS + "/" + id_user

    try:
        # retrieve information from FILE_NAME_EMS and FILE_NAME_INFORMATION
        E_ms_Dealer, MC, MS, k_prime = retrieve_inf(path_user)

        print "\n     E_ms_Dealer: " + str(E_ms_Dealer)
        print "     eMS: " + str(E_ms_Client)

        if str(E_ms_Dealer) == str(E_ms_Client):
            print "     decrypted eMS (since E_ms_Dealer==E_ms_Client) are not different to take one or other: " + E_ms_Dealer

            # if E_ms_Dealer== str(E_ms_Client) it is possible to open eMS with the key=MS
            # decrypt the message
            decrypted_eMS = AES_decrypt(MS, E_ms_Client)

            print "     decrypted_eMS: "+str(decrypted_eMS)

            # open E_ms[k, (g^s' h^r')] with MS
            # and take k and MC_decs
            info = split(decrypted_eMS, CHAR_DATA_SPLIT)
            MC_dec = info[0]
            k = info[1]
            print "\n     MC_dec: " + MC_dec
            print "     k: " + k

            # decrypt MC given in the sharing phase with k given inside E_ms
            dec_MC_saved_Sharing = AES_decrypt(k, MC)

            print "\n     dec_MC_saved_Sharing: " + str(dec_MC_saved_Sharing)
            print "     MC_dec: " + str(MC_dec)

            # check if are equals
            if dec_MC_saved_Sharing == MC_dec:
                # if they are equal send back E_ms[k']
                emsk_prime = AES_encrypt(MS, k_prime)
                print "     E_MS[k_prime]: " + emsk_prime
                print "     send to the client Ems[k']"
                msg = COD200 + CHAR_DATA_SPLIT + str(emsk_prime)

                # From, To, Payload, Phase, id_user
                logMsg("ExternalServer", "Client", msg, "RECOSTRUCTION", id_user)

                self.csocket.send((bytes(msg).encode("utf-8")))

                # Wait MC' from Client
                MC_prime = self.csocket.recv(BUFFER_SIZE_REQUEST_MESSAGES)

                # Log clinet's message
                logMsg("Client", "ExternalServer", MC_prime, "RECONSTRUCTION", id_user)

                print "     MC_prime:" + MC_prime

                # calculate MS' = E_k'''[MC']
                keyThird = str(genRand(sys.maxint))

                # keyThird must be a string
                MS_prime = AES_encrypt(keyThird, str(MC_prime))

                # saving locally the new info: MC'||MS_prime||kThird
                path_file_name = path_user + "/" + FILE_NAME_INFORMATION
                data = str(MC_prime) + CHAR_DATA_SPLIT + str(MS_prime) + CHAR_DATA_SPLIT + str(keyThird) + "\n"

                # flush data
                write_data(path_file_name, data)

                # sending MS_prime to the client.
                msg = COD200 + CHAR_DATA_SPLIT + MS_prime

                # THE CONNECTION IS ESTBLASHED

                # Now the ES sends all data to the dealer in order to prove that it can replace the secres S'
                # model: k||kPrime||MS||(g^sPrime h^rPrime)||MC||id_user
                out_data_dealer = WHICH_PHASE[3] + CHAR_MSG_SPLIT + \
                    str(k) + CHAR_DATA_SPLIT + \
                    str(k_prime) + CHAR_DATA_SPLIT + \
                    str(MS) + CHAR_DATA_SPLIT + \
                    str(MC_dec) + CHAR_DATA_SPLIT + \
                    str(MC_prime) + CHAR_DATA_SPLIT + \
                    str(id_user) + par.CHAR_DATA_SPLIT + DELIM

                # From, To, Payload, Phase, id_user
                logMsg("ExternalServer", "Dealer", str(out_data_dealer), "RECOSTRUCTION", id_user)

                send_data(IP_DEALER, PORT_DEALER, out_data_dealer)

            else:
                print "     MC_saved_Sharing_decrypted != MC_dec_given_inside_Ems - Dealer or Client is cheating"
                msg = COD960 + CHAR_DATA_SPLIT + COD960_desc
                # Log error Phase, Actor, CODError, Payload,  id_user
                logError("RECONSTRUCTION", "ExternalServer", COD960, COD960_desc, id_user)

        else:
            print "     E_ms_Dealer != E_ms_Client - Dealer or Client is cheating"
            msg = COD930 + CHAR_DATA_SPLIT + COD930_desc

            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("RECONSTRUCTION", "ExternalServer", COD930, COD930_desc, id_user)

    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc

        payload = COD444_desc + " " + str(e)
        # Log error Phase, Actor, CODError, Payload,  id_user
        logError("RECONSTRUCTION", "ExternalServer", COD444, payload, id_user)

    # Log message (From, To, Payload, Phase, id_user)
    logMsg("ExternalServer", "Client", str(msg), "RECOSTRUCTION", id_user)

    # send back
    self.csocket.send((bytes(msg).encode("utf-8")))

    print "     Client at " + str(self.clientAddress) + " disconnected..."
