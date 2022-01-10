import netifaces as ni
from CustomThreads.SocketThread import SocketThread
from CustomThreads.groups import parametres

# constants
par = parametres()
INTERFACE = par.INTERFACE
PORT_TO_LISTEN = par.PORT_TO_LISTEN

INTERFACE2 = par.INTERFACE2
PORT_TO_LISTEN = par.PORT_TO_LISTEN

if __name__ == "__main__":
    ni.ifaddresses(INTERFACE)
    ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
    # print ip
    IP_HOST = ip

    ni.ifaddresses(INTERFACE2)
    ip = ni.ifaddresses(INTERFACE2)[ni.AF_INET][0]['addr']
    # print ip
    IP_HOST2 = ip

    # Starting two threads for each interface:
    # - one for the Shareholders 10.0.0.0/24
    # - one for the external server 99.0.0.0/24

    # listener on first interface is for Shareholder communications
    unicast_conn = SocketThread('0.0.0.0', PORT_TO_LISTEN)
    # unicast_conn.setDaemon(True)
    unicast_conn.start()

    unicast_conn.join()
