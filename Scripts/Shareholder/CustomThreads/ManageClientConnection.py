import os
import threading
from Reconstruction.Reconstruction import reconstructionShareholder
from Utils.Utils_function import write_data
from Utils.Utils_function import check_dir
from Sharing.Sharing import sharingShareholder
from groups import parametres


par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE

CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
WHICH_PHASE = par.WHICH_PHASE

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES

COD3000 = par.COD3000
COD3000_desc = par.COD3000_desc
DELIM = par.DELIM
def split(data, char):
    return data.split(char)


class ManageClientConnection(threading.Thread):
    def __init__(self, clientAddress, clientsocket, data, address, broadcast):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        self.data = data
        self.address = address
        self.broadcast = broadcast

    def run(self):
        if self.broadcast == False:
            self.Unicast()
        else:
            self.Broadcast()

    def Unicast(self):
        print "---------------------------------------------------------------------------------------------------"
        print ("New connection added from: ", self.clientAddress)

        data_from_dealer = ''
        data = True
        while data:
            data = self.csocket.recv(BUFFER_SIZE_REQUEST_MESSAGES)
            data_from_dealer += data

            if data_from_dealer.find(DELIM) != -1:
                break
        print data_from_dealer

        # Split the information with ||| char
        # info[0] = WHICH_PHASE
        # info[1] = DATA

        info = split(data_from_dealer, CHAR_MSG_SPLIT)

        # SHA
        # model data: SHA|||s_i||t_i||h(x_i)||id_user
        if info[0] == WHICH_PHASE[0]:
            print "     Request SHARING PHASE"
            print "     info[1]= " + str(info[1])

            # take the data informations: s_i||t_i||h(x_i)||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            s_i = data[0]
            t_i = data[1]
            hx_i = data[2]
            id_user = data[3]
            print "     data passed to __sharing function: s_i=" + str(s_i) + " t_i=" + str(t_i) + " hx_i=" + str(
                hx_i) + " id_user=" + str(id_user)
            self.__sharing(s_i, t_i, hx_i, id_user)

        # REC
        # model data: REC|||x_i|| id_user
        elif info[0] == WHICH_PHASE[1]:
            print "     Request RECONSTRUCTION PHASE"
            print "     info[1]= " + str(info[1])

            # take the data informations: x_i|| id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            x_i = int(data[0])
            id_user = data[1]
            print "     data passed to __reconstruction function: x_i=" + str(x_i) + " id_user=" + str(id_user)

            self.__reconstruction(x_i, id_user)
        else:
            print "     ERROR, UNRECOGNIZED PHASE: " + str(info[0])
            msg = COD3000 + CHAR_DATA_SPLIT + COD3000_desc

            # replay to the user with the External Server code
            self.csocket.send((bytes(msg).encode("utf-8")))
            print "     Client at " + str(self.clientAddress) + " disconnected..."

    def __sharing(self, s_i, t_i, hx_i, id_user):
        sharingShareholder(self, s_i, t_i, hx_i, id_user)

    def __reconstruction(self, x_i, id_user):
        reconstructionShareholder(self, x_i, id_user)

    def Broadcast(self):
        # model data: c0||c1||..||c_t-1||id_user
        print "---------------------------------------------------------------------------------------------------"
        print ("New BROADCAST MESSAGE arrived FROM: ", self.address)
        print "     received message:", self.data

        # Since is a UDP connection the information are inside data var

        # Split the informations that are in the format: c_0||c_2||c_3||..||c_(t-1)||id_user
        info = split(self.data, CHAR_DATA_SPLIT)

        # The information about id_user is in the last position
        id_user = info[len(info) - 1]

        # Save the information at the path PATH_DATA_USERS=/home-user/data_users/id_user/commitments

        # Checks if exists the id_user directory yet
        # If it does not exists create it
        path_user = PATH_DATA_USERS + "/" + id_user
        check_dir(path_user)

        # Create a file called "commitments" with the [c_0||c_2||c_3||..||c_(t-1)] informations
        # Oss: le info vengono appese, cosi si ha uno storico degli share (per il momento),
        #      quindi l'informazione all'ultima riga e'  quella piu' aggiornata

        path_file_name = path_user + "/" + FILE_NAME_COMM
        # prepariamo i dati da inserire nel file:
        #       elimina l "||id_user" e aggiungo per la newline
        d = self.data[:-(len(id_user) + len(CHAR_DATA_SPLIT))] + "\n"

        # write data into file
        write_data(path_file_name, d)
