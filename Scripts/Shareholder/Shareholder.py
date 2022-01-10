import signal
import sys
from CustomThreads.SocketThread import SocketThread
import netifaces as ni
from CustomThreads.groups import parametres

# constants
par = parametres()
INTERFACE = par.INTERFACE
PORT_TO_LISTEN = par.PORT_TO_LISTEN
IP_BRD_HOST = par.IP_BRD_HOST

unicast_conn = None
brd_conn = None

if __name__ == "__main__":
    ni.ifaddresses(INTERFACE)
    ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
    # print ip
    IP_HOST = ip

    # Starting two threads for each interface: unicast and broadcast communications

    # listener on first interface is for unicast communications
    unicast_conn = SocketThread(IP_HOST, PORT_TO_LISTEN, broadcast=False)
    # unicast_conn.setDaemon(True)
    unicast_conn.start()

    # listener on second interface is for broadcast communications
    brd_conn = SocketThread(IP_BRD_HOST, PORT_TO_LISTEN, broadcast=True)

    # only for 700-digit test
    # brd_conn = SocketThread(IP_HOST, PORT_TO_LISTEN, broadcast=True)

    # brd_conn.setDaemon(True)
    brd_conn.start()

    unicast_conn.join()
    brd_conn.join()
