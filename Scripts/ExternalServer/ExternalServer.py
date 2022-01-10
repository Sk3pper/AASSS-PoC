import netifaces as ni
from CustomThreads.SocketThread import SocketThread
from CustomThreads.groups import parametres

# costanti/var globali
par = parametres()
INTERFACE = par.INTERFACE
PORT_TO_LISTEN = par.PORT_TO_LISTEN


if __name__ == "__main__":
    ni.ifaddresses(INTERFACE)
    ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
    # print ip  # should print "192.168.100.37"
    IP_HOST = ip


    # start thread listenere connections unicast
    unicast_conn = SocketThread(IP_HOST, PORT_TO_LISTEN)
    # unicast_conn.setDaemon(True)
    unicast_conn.start()
    unicast_conn.join()

