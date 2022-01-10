import datetime
import socket

CHAR_LOG_DATA_SPLIT = "|-|"
CHAR_LOG_MSG_SPLIT = "-|-"
WHICH_LOG = ['MSG', 'ERROR']
IP_LOG = "LOG"
PORT_LOG = 5000
DELIM_LOG = ".-."

def logError(Phase, Actor, CODError, Payload,  id_user):
    #  ERROR-|-timestamp|-|Phase|-|Actor|-|CODError|-|Payload|-|id_user
    timestamp = str(datetime.datetime.now())

    # timestamp, From, To, Payload, Phase, id_user
    out_data = WHICH_LOG[1] + CHAR_LOG_MSG_SPLIT + \
               str(timestamp) + CHAR_LOG_DATA_SPLIT + \
               str(Phase) + CHAR_LOG_DATA_SPLIT + \
               str(Actor) + CHAR_LOG_DATA_SPLIT + \
               str(CODError) + CHAR_LOG_DATA_SPLIT + \
               str(Payload) + CHAR_LOG_DATA_SPLIT + \
               str(id_user) + DELIM_LOG

    print "          Send to " + IP_LOG + ": " + " out_data = " + out_data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP_LOG, PORT_LOG))
    client.sendall(bytes(out_data).encode("utf-8"))
    client.close()