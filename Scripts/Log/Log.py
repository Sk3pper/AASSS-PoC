import netifaces as ni
from CustomThreads.SocketThread import SocketThread
from CustomThreads.groups import parametres

# constants
par = parametres()
INTERFACE = par.INTERFACE1
PORT_TO_LISTEN1 = par.PORT_TO_LISTEN

INTERFACE2 = par.INTERFACE2
PORT_TO_LISTEN = par.PORT_TO_LISTEN

if __name__ == "__main__":
    ni.ifaddresses(INTERFACE)
    ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
    IP_HOST = ip

    ni.ifaddresses(INTERFACE2)
    ip = ni.ifaddresses(INTERFACE2)[ni.AF_INET][0]['addr']
    IP_HOST2 = ip

    # Starting two threads for each interface:
    # - verso gli Shareholder 10.0.0.0/24
    # - verso l'external server 99.0.0.0/24

    # listener on first interface is for Shareholder communications
    unicast_conn = SocketThread(IP_HOST, PORT_TO_LISTEN)
    # unicast_conn.setDaemon(True)
    unicast_conn.start()

    # listener on first interface is for External Server communications
    unicast_conn_ES = SocketThread(IP_HOST2, PORT_TO_LISTEN)
    unicast_conn_ES.start()

    unicast_conn.join()
    unicast_conn_ES.join()
