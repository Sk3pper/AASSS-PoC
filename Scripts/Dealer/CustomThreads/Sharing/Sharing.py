import hashlib
import os
import socket
import sys
from CustomThreads.groups import MODP2048
from CustomThreads.groups import parametres
from CustomThreads.PedersenUtilities.VSS import pedersenSharingChecked
from CustomThreads.Utils.Utils_function import write_data
from CustomThreads.Utils.Utils_function import send_data
from CustomThreads.Utils.Utils_function import logMsg,logError
# load group
g2048 = MODP2048()
n = g2048.n
t = g2048.t

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
IP_SHAREHOLDERS = par.IP_SHAREHOLDERS
PORT_SHAREHOLDERS = par.PORT_SHAREHOLDERS
BROADCAST = par.BROADCAST
debug = par.DEBUG

CHAR_COORD_SPLIT = par.CHAR_COORD_SPLIT
IP_EXTERNAL_SERVER = par.IP_EXTERNAL_SERVER
PORT_EXTERNAL_SERVER = par.PORT_EXTERNAL_SERVER
WHICH_PHASE = par.WHICH_PHASE

FILE_NAME_MC = par.FILE_NAME_MC

END_MESSAGES = par.END_MESSAGES

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES

# SHARING CODES
COD200 = par.COD200  # Everything is went well

COD100 = par.COD100  # User already signed-up [DEALER]
COD100_desc = par.COD100_desc

COD550 = par.COD550  # Problem with SHA2, user_id dir is not present. Send MC before!
COD550_desc = par.COD550_desc

COD444 = par.COD444 # Generale error
COD444_desc = par.COD444_desc

DELIM = par.DELIM


# SHA1: request from client
def sharing1Dealer(self, MC, id_user):
    print "          sharing1Dealer"
    msg = ''
    path_user = PATH_DATA_USERS + "/" + id_user
    try:
        # check if the user is already signed-up
        if not os.path.isdir(path_user):  # the id_user is NOT present
            # send to ExternalServer SHA1|||MC||id_user
            out_data = WHICH_PHASE[0]+CHAR_MSG_SPLIT+MC+CHAR_DATA_SPLIT+id_user + par.CHAR_DATA_SPLIT + DELIM

            # Log the message (From, To, Payload, Phase, id_user)
            logMsg("Dealer", IP_EXTERNAL_SERVER, out_data, "SHARING", id_user)

            # send the request and wait the replay
            in_data = send_data(IP_EXTERNAL_SERVER, PORT_EXTERNAL_SERVER, out_data)

            # check if ES has had problem
            if COD200 in in_data:
                # save locally the MC-value that it will be used in the REC-phase

                # create user_id dir
                os.makedirs(path_user)

                # create file and write inside the data
                path_file_name = path_user + "/" + FILE_NAME_MC
                data = str(MC)+"\n"
                # flush data
                write_data(path_file_name, data)

                # prepare the replay for the user - COD200 - no value
                msg = COD200 + CHAR_DATA_SPLIT + "now you can contact the external service"
            else:
                # something is went bad from ExternalServer-side
                # replay with the error
                msg = in_data
                # Phase, Actor, CODError, Payload,  id_user
                logError("SHARING", "Dealer", "None", in_data, id_user)
        else:
            # user is already present --> double signup
            msg = COD100+CHAR_DATA_SPLIT+COD100_desc
            # Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "Dealer", COD100, COD100_desc, id_user)

    except Exception as e:
        print "\n         General Error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444
        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "Dealer", COD444, payload, id_user)

    # Log the message (From, To, Payload, Phase, id_user)
    logMsg("Dealer", "Client", msg, "SHARING", id_user)

    # replay to the user with the External Server code
    self.csocket.send((bytes(msg).encode("utf-8")))
    print "     Client at " + str(self.clientAddress) + " disconnected..."


def sharing2Dealer(self, sPrime, id_user, abscissa_vector=None):
    print "     __sharing2"
    msg = ''
    path_user = PATH_DATA_USERS + "/" + id_user
    path_file_name = path_user + "/" + FILE_NAME_COMM

    try:
        # Dealer has to save only the commitments
        # Check if the user_dir is present (must be) because is created in the SHA1
        if not os.path.isdir(path_user):
            msg = COD550 + CHAR_DATA_SPLIT + COD550_desc
            # Log error Phase, Actor, CODError, Payload,  id_user
            logError("SHARING", "Dealer", COD550, COD550_desc, id_user)
        else:
            # compute shares and t-shares CHECKED!
            # after this step we are secure that the shares and commitmets are consistent
            shares, t_shares, Commitments, coordinates = pedersenSharingChecked(sPrime, g2048.t, g2048.n,
                                                                                abscissa_vector)
            # send to each Shareholder one share
            # the coordinates are sorted so each Shareholder take the coordinate in order of number
            unicast_sent_response = unicastSend(shares, t_shares, coordinates, id_user)

            if unicast_sent_response != True:
                # something is went bad from Shareholder-side
                # replay with the Shareholder error (should be 500)
                msg = unicast_sent_response
                logError("SHARING", "Dealer", "500", "A lot of wrong saves has went bad, we can't continue", id_user)
            else:
                # send in broadcast the Commitments
                broadcastSend(Commitments, id_user)

                data = ''
                for c in Commitments:
                    data = data + str(c) + CHAR_DATA_SPLIT
                data = data[:-len(CHAR_DATA_SPLIT)] + "\n"

                # flush data
                write_data(path_file_name, data)

                # replay to the user with coordinates
                # since coordinates are sorted and the minimum coordinate is sent to J1 and so on
                back_data = ''
                for c in coordinates:
                    back_data += str(c) + CHAR_COORD_SPLIT
                back_data = back_data[:-len(CHAR_COORD_SPLIT)]
                print "     back_data:" + back_data

                msg = COD200 + CHAR_DATA_SPLIT + back_data

    except Exception as e:
        print "\n          General error: " + str(e)
        msg = COD444 + CHAR_DATA_SPLIT + COD444_desc
        # Log error Phase, Actor, CODError, Payload,  id_user
        payload = COD444_desc + str(e)
        logError("SHARING", "Dealer", COD444, payload, id_user)

    # since this phase is called also from REC2-Dealer to rebuilt share over S''. If we went from that
    # phase we don't replay with coordinates

    if self != None:
        # From, To, Payload, Phase, id_user
        logMsg("Dealer", "Client", msg, "SHARING", id_user)

        self.csocket.send((bytes(msg).encode("utf-8")))
        print "     Client at " + str(self.clientAddress) + " disconnected..."

    # END
    logMsg("Dealer", "Client", END_MESSAGES, "SHARING", id_user)


def unicastSend(shares, t_shares, coordinates,id_user):
    print "\n     unicastSend"
    i = 0
    j = 1

    wrong_send = []
    for IP in IP_SHAREHOLDERS:
        out_data = "SHA"+CHAR_MSG_SPLIT
        out_data = out_data + str(shares[i])+CHAR_DATA_SPLIT
        out_data = out_data + str(t_shares[i]) + CHAR_DATA_SPLIT

        # hash the coordinate x_i
        hash = hashlib.sha256()
        hash.update(str(coordinates[i]))
        out_data = out_data + str(hash.hexdigest()) + CHAR_DATA_SPLIT

        # set the user_id
        out_data = out_data + id_user + par.CHAR_DATA_SPLIT + DELIM

        # Log the message(From, To, Payload, Phase, id_user
        sh = "Shareholder-"+str(j)
        logMsg("Dealer", sh, out_data, "SHARING", id_user)

        # send out_data to (IP,PORT_SHAREHOLDERS)
        try:
            in_data = send_data(IP, PORT_SHAREHOLDERS, out_data)

            # check if everything is went well, of not mark it
            # NOT IN!!!!
            if COD200 not in in_data:
                wrong_send.append(IP)

        except Exception as e:
            print "\n          General error: " + str(e)
            # Log error Phase, Actor, CODError, Payload,  id_user
            wrong_send.append(IP)
            payload = COD444_desc + str(e) + " IP: "+str(IP)
            logError("SHARING", "Dealer", COD444, payload, id_user)

        i += 1
        j += 1

    if len(wrong_send) <= (n-t):
        # report the error
        for i in range(0, len(wrong_send)):
            logError("SHARING", "Dealer", "None", wrong_send[i], id_user)

        return True
    else:
        return False


def broadcastSend(Commitments, id_user):
    print "\n     broadcastSend"
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # comment if you are doing 700-DIGIT test

    out_data = ''

    for c in Commitments:
        out_data = out_data + str(c) + CHAR_DATA_SPLIT

    out_data = out_data + id_user
    print "\n          out_data = "+out_data

    # Log the message (From, To, Payload, Phase, id_user
    logMsg("Dealer", "Broadcast", out_data, "SHARING", id_user)

    # send the broadcast message
    print "size packet UDP: "+str(len(out_data))
    client.sendto(out_data, (BROADCAST, PORT_SHAREHOLDERS))

    '''
    # only for 700 DIGIT TEST
    for IP in IP_SHAREHOLDERS:
        print "     IP: "+str(IP)
        client.sendto(out_data, (IP, PORT_SHAREHOLDERS))
    '''

    return True
