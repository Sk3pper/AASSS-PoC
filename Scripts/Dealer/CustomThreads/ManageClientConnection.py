import threading

from Sharing.Sharing import sharing1Dealer, sharing2Dealer
from Reconstruction.Reconstruction import reconstructionDealer1, reconstructionDealer2
from Utils.Utils_function import logMsg
from groups import parametres

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
FILE_NAME_COMM = par.FILE_NAME_COMM
FILE_NAME_SHARE = par.FILE_NAME_SHARE
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
WHICH_PHASE = par.WHICH_PHASE
CHAR_COORD_SPLIT = par.CHAR_COORD_SPLIT

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES

COD3000 = par.COD3000
COD3000_desc = par.COD3000_desc

DELIM = par.DELIM

def split(data, char):
    return data.split(char)


def strTointList(list):
    newList = []
    for l in list:
        newList.append(int(l))
    return newList


class ManageClientConnection(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress

    def run(self):
        print "------------------------------------------------------------------------------------------"
        print ("New connection added from: ", self.clientAddress)

        # you have to read all data, TPC is not message-based prototocl but is a stream protocol so the data
        # could be splitted in a more than one packet
        data_from_dealer = ''
        data = True
        while data:
            data = self.csocket.recv(BUFFER_SIZE_REQUEST_MESSAGES)
            data_from_dealer += data

            if data_from_dealer.find(DELIM) != -1:
                break
        print data_from_dealer

        info = split(data_from_dealer, CHAR_MSG_SPLIT)


        # REC2
        if info[0] == WHICH_PHASE[3]:
            print "     Request RECONSTRUCTION PHASE - STEP TWO\n"
            print "     info[1]= " + str(info[1])

            # take the informations
            # model: k||kPrime||MS||(g^sPrime h^rPrime)||MC||id_user
            data = split(info[1], CHAR_DATA_SPLIT)

            k = data[0]
            kPrime = data[1]
            MS = data[2]
            MC_dec = data[3]
            MC = data[4]
            id_user = data[5]

            print "     data passed to __reconstruction2 function: k=" + str(k) + \
                  " kPrime=" + str(kPrime) + \
                  " MS=" + str(MS) + \
                  " MC_dec=" + str(MC_dec) + \
                  " MC=" + str(MC) + \
                  " id_user=" + str(id_user)

            self.__reconstruction2(k, kPrime, MS, MC_dec, MC, id_user)

        # SHA1
        elif info[0] == WHICH_PHASE[0]:

                print "     Request SHARING PHASE - STEP ONE\n"
                print "     info[1]= " + str(info[1])
                data = split(info[1], CHAR_DATA_SPLIT)
                mc = data[0]
                id_user = data[1]

                # LogMSG pure del client che non puo' farlo da JS
                logMsg("Client", "Dealer", data_from_dealer, "SHARING", id_user)

                print "     data passed to __sharing function: mc=" + str(mc) + " id_user=" + str(id_user)
                self.__sharing1(mc, id_user)

        # SHA2
        elif info[0] == WHICH_PHASE[1]:
            print "     Request SHARING PHASE - STEP TWO\n"
            print "     info[1]= " + str(info[1])
            data = split(info[1], CHAR_DATA_SPLIT)
            sPrime = int(data[0])
            id_user = data[1]

            # LogMSG pure del client che non puo' farlo da JS
            logMsg("Client", "Dealer", data_from_dealer, "SHARING", id_user)

            print "     data passed to __sharing function: sPrime=" + str(sPrime) + " id_user=" + str(id_user)
            self.__sharing2(sPrime, id_user)

        # REC1
        elif info[0] == WHICH_PHASE[2]:
            print "     Request RECONSTRUCTION PHASE - STEO ONE\n"
            print "     info[1]= " + str(info[1])

            # prendere l'informazione di sPrime, x1,x2,..,xn, sSecond, mcPrime, eMS, id_user, dal messaggio
            data = split(info[1], CHAR_DATA_SPLIT)
            sPrime = int(data[0])
            abscissa_vect = strTointList(split(data[1], CHAR_COORD_SPLIT))
            sSecond = int(data[2])
            mcPrime = data[3]
            eMS = data[4]
            id_user = data[5]

            # LogMSG pure del client che non puo' farlo da JS
            logMsg("Client", "Dealer", data_from_dealer, "RECONSTRUCTION", id_user)

            print "     data passed to __reconstruction function: sPrime=" + str(sPrime) + " abscissa_vect=" + str(
                abscissa_vect) + \
                  " sSecond=" + str(sSecond) + \
                  " mcPrime=" + str(mcPrime) + \
                  " eMS=" + str(eMS) + \
                  " id_user=" + str(id_user)
            self.__reconstruction1(sPrime, abscissa_vect, sSecond, mcPrime, eMS, id_user)
        else:
            print "     ERROR, UNRECOGNIZED PHASE: " + str(info[0])
            msg = COD3000 + CHAR_DATA_SPLIT + COD3000_desc

            # replay to the user with the External Server code
            self.csocket.send((bytes(msg).encode("utf-8")))
            print "     Client at " + str(self.clientAddress) + " disconnected..."

    def __sharing1(self, mc, id_user):
        sharing1Dealer(self, mc, id_user)

    def __sharing2(self, sPrime, id_user):
        sharing2Dealer(self, sPrime, id_user)

    def __reconstruction1(self, sPrime, abscissa_vect, sSecond, mcPrime, eMS, id_user):
        reconstructionDealer1(self, sPrime, abscissa_vect, sSecond, mcPrime, eMS, id_user)

    def __reconstruction2(self, k, kPrime, MS, MC_dec, MC, id_user):
        reconstructionDealer2(self, k, kPrime, MS, MC_dec, MC, id_user)
