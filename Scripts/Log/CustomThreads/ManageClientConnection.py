import os
import threading
from LogMessage.LogMessage import logMsg
from Utils.Utils_function import write_data
from Utils.Utils_function import check_dir
from LogError.LogError import logErr
from groups import parametres


par = parametres()
PATH_DATA_USERS = par.PATH_DATA_USERS

CHAR_DATA_SPLIT = par.CHAR_DATA_SPLIT
CHAR_MSG_SPLIT = par.CHAR_MSG_SPLIT
WHICH_LOG = par.WHICH_LOG

BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES
DELIM_LOG = par.DELIM_LOG


def split(data, char):
    return data.split(char)


class ManageClientConnection(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress

    def run(self):
        print "---------------------------------------------------------------------------------------------------"
        print ("New connection added from: ", self.clientAddress)
        # data = self.csocket.recv(BUFFER_SIZE_REQUEST_MESSAGES)

        # you have to read all data, TPC is not message-based prototocl but is a stream protocol so the data
        # could be splitted in a more than one packet
        data_from = ''
        data = True
        while data:
            data = self.csocket.recv(BUFFER_SIZE_REQUEST_MESSAGES)
            data_from += data

            if data_from.find(DELIM_LOG) != -1:
                break
        # print data_from
        # Delete DELIM_LOG
        data_from = data_from[:-len(DELIM_LOG)]

        # Split the information with -|- char
        # info[0] = WHICH_LOG
        # info[1] = DATA

        # DELETE DELIM msg
        data_from = data_from.replace("---", "")
        # print data_from
        info = split(data_from, CHAR_MSG_SPLIT)
        # print info

        # MSG
        # model: MSG-|-timestamp|-|From|-|To|-|Payload|-|Phase
        if info[0] == WHICH_LOG[0]:
            print "     Request LOG-MESSAGE"
            print "     info[1]= " + str(info[1])

            # take the data informations: timestamp||From||To||Payload||Phase||id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            timestamp = data[0]
            From = data[1]
            To = data[2]
            Payload = data[3]
            Phase = data[4]
            id_user = data[5]
            print "     data passed to __logMsg function: timestamp= " + str(timestamp) + \
                  " From= " + str(From) + \
                  " To= " + str(To) + \
                  " Payload= " + str(Payload) +\
                  " Phase= "+str(Phase) +\
                  " id_user= " + str(id_user)
            self.__logMsg(timestamp, From, To, Payload, Phase, id_user)

        # ERROR
        # model: ERROR-|-timestamp|-|Phase|-|Actor|-|CODError|-|Payload|-|id_user
        elif info[0] == WHICH_LOG[1]:
            print "     Request LOG-ERROR"
            print "     info[1]= " + str(info[1])

            # take the data informations: x_i|| id_user
            data = split(info[1], CHAR_DATA_SPLIT)
            timestamp = data[0]
            Phase = data[1]
            Actor = data[2]
            CODError = data[3]
            Payload = data[4]
            id_user = data[5]

            print "     data passed to __logMsg function: timestamp= " + str(timestamp) + \
                  " Actor= " + str(Actor) + \
                  " CODError: "+str(CODError)+\
                  " Payload= " + str(Payload) + \
                  " Phase= " + str(Phase) + \
                  " id_user= " + str(id_user)

            self.__logError(timestamp, id_user, Phase, Actor, CODError, Payload)
        else:
            print "     ERROR, UNRECOGNIZED PHASE: " + str(info[0])
            self.csocket.send((bytes("ERROR, UNRECOGNIZED PHASE: " + str(info[0])).encode("utf-8")))

    def __logMsg(self, timestamp, From, To, Payload, Phase, id_user):
        logMsg(self, timestamp, From, To, Payload, Phase, id_user)

    def __logError(self, timestamp, id_user, Phase, Actor, CODError, Payload):
        logErr(self, timestamp, id_user, Phase, Actor, CODError, Payload)
