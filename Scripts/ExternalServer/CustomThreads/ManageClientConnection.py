import threading

from Utils.Utils_function import logMsg
from Sharing.Sharing import sharing1ES, sharing2ES
from Reconstruction.Reconstruction import reconstructionES1, reconstructionES2
from groups import parametres

par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS
CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
WHICH_PHASE = par.WHICH_PHASE

COD3000 = par.COD3000
COD3000_desc = par.COD3000_desc

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES

DELIM = par.DELIM


def split(data, char):
    return data.split(char)


class ManageClientConnection(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress

    def run(self):
        """
        la connessione e' stabilita con chi vuole paralre con il dealer. A questo punto deve estrapolare
        le informazioni che sta ricevendo.
        Ci sono due casi:
            - SHARING PHASE
            - RECONSTRUCTION PHASE
        Per capire in che fase si sta operando all'inizio i messaggi sono formatti nel seguente modo:
                                WHICH_PHASE|||DATA
        In cui:
        - WHICH_PHASE==SHA1 --> DATA=[mc||External Service Name||id_user]
        - WHICH_PHASE==SHA2 --> DATA=[sPrime||id_user]

        - WHICH_PHASE==REC1 --> DATA=[sPrime||x1,x2,..,xn||sSecond||mcPrime||eMS||id_user]
        - WHICH_PHASE==REC2 --> DATA=[k||kPrime||MS||(g^sPrime h^rPrime)||MC||id_user]

        Le informazioni che si salva il dealer PER UTENTE sono:
            - c0||c1||..||c(t-1)
            - MC

        Le informazioni come per il caso dello shareholder vengono salvate dentro alla cartella con tutti gli utenti,
        che nel cloud avra' un altro path quale "/home-user/data_users/", la cartella data_users e' gia' stata creata
        e il volume viene montato li, QUINDI i dati non vengono persi anche se il container va in down
        """

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


        # 2- splitta le informazioni che saranno nel formato: [WHICH_PHASE|||DATA]
        # info[0] = WHICH_PHASE
        # info[1] = DATA

        info = split(data_from_dealer, CHAR_MSG_SPLIT)

        # [FROM DEALER] SHA1
        if info[0] == WHICH_PHASE[0]:
            print "     Request SHARING PHASE - STEP ONE"
            print "     info[1]= " + str(info[1])
            # model: SHA1|||MC||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            mc = data[0]
            id_user = data[1]
            print "     data passed to __sharing1 function: mc=" + str(mc) + " id_user=" + str(id_user)
            self.__sharing1(mc, id_user)

        # [FROM CLIENT]SHA2
        elif info[0] == WHICH_PHASE[1]:
            print "     Request SHARING PHASE - STEP TWO"
            print "     info[1]= " + str(info[1])

            # model: SHA2|||MC||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            mc = data[0]
            id_user = data[1]
            # LogMSG pure del client che non puo' farlo da JS
            logMsg("Client", "ExternalServer", data_from_dealer, "SHARING", id_user)

            print "     data passed to __sharing2 function: mc=" + str(mc) + " id_user=" + str(id_user)
            self.__sharing2(mc, id_user)

        # FROM DEALER] REC1
        elif info[0] == WHICH_PHASE[2]:
            print "     Request RECONSTRUCTION PHASE - STEP ONE"
            print "     info[1]= " + str(info[1])

            # model: REC1|||eMS||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            eMS = data[0]
            id_user = data[1]
            print "     data passed to __reconstruction1 function: eMS=" + str(eMS) + " id_user=" + str(id_user)
            self.__reconstruction1(eMS, id_user)

        # [FROM CLIENT] REC2
        elif info[0] == WHICH_PHASE[3]:
            print "     Request RECONSTRUCTION PHASE - STEP TWO"
            print "     info[1]= " + str(info[1])

            # model: REC2|||eMS||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            eMS = data[0]
            id_user = data[1]

            # LogMSG pure del client che non puo' farlo da JS
            logMsg("Client", "ExternalServer", data_from_dealer, "RECONSTRUCTION", id_user)

            print "     data passed to __reconstruction2 function: eMS=" + str(eMS) + " id_user=" + str(id_user)
            self.__reconstruction2(eMS, id_user)

        else:
            print "     ERROR, UNRECOGNIZED PHASE: " + str(info[0])
            msg = COD3000 + CHAR_DATA_SPLIT + COD3000_desc

            # replay to the user with the External Server code
            self.csocket.send((bytes(msg).encode("utf-8")))
            print "     Client at " + str(self.clientAddress) + " disconnected..."


    def __sharing1(self, mc, id_user):
        sharing1ES(self, mc, id_user)

    def __sharing2(self, mc, id_user):
        sharing2ES(self, mc, id_user)

    def __reconstruction1(self,eMS, id_user):
        reconstructionES1(self,eMS,id_user)

    def __reconstruction2(self, x_i, id_user):
        reconstructionES2(self, x_i, id_user)