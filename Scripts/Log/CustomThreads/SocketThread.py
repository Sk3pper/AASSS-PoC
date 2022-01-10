import socket
import threading
from ManageClientConnection import ManageClientConnection
from groups import parametres

par = parametres()
TIMEOUT_CONNECTIONS = par.TIMEOUT_CONNECTIONS


class SocketThread(threading.Thread):
    def __init__(self, host_ip, port):
        """
        :rtype: threading.Thread
        """
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.port = port
        # set sockets

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Server started, bind on "+str(self.host_ip)+":"+str(self.port))
        self.server.bind((self.host_ip, self.port))


    def run(self):
        print("Waiting for client request..")
        while True:
            self.server.listen(100)
            clientsock, clientAddress = self.server.accept()
            clientTh = ManageClientConnection(clientAddress, clientsock)
            clientTh.start()
            # self.thread_activeted.append(clientTh)