import socket
import threading
from ManageClientConnection import ManageClientConnection
from groups import parametres

par = parametres()
TIMEOUT_CONNECTIONS = par.TIMEOUT_CONNECTIONS
BUFFER_SIZE_REQUEST_MESSAGES = par.BUFFER_SIZE_REQUEST_MESSAGES


class SocketThread(threading.Thread):
    def __init__(self, host_ip, port, broadcast):
        """
        :rtype: threading.Thread
        """
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.port = port
        self.brd = broadcast
        # set sockets
        if broadcast == False:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Server started, bind on "+str(self.host_ip)+":"+str(self.port))
            self.server.bind((self.host_ip, self.port))
        else:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            print("Server started, bind on " + str(self.host_ip) + ":" + str(self.port))
            self.server.bind((self.host_ip, self.port))


    def run(self):
        # wait connections
        if self.brd == False:
            self.UnicastConnection()
        else:
            self.BroadcastConnection()

    def UnicastConnection(self):
        print("Waiting for client request..")
        while True:
            self.server.listen(100)
            clientsock, clientAddress = self.server.accept()
            clientTh = ManageClientConnection(clientAddress, clientsock, None, None, broadcast=False)
            clientTh.start()
            # self.thread_activeted.append(clientTh)

    def BroadcastConnection(self):
        print("Waiting for client request..")
        while True:
            data, addr = self.server.recvfrom(BUFFER_SIZE_REQUEST_MESSAGES)  # buffer size is 16 Kbytes
            clientTh = ManageClientConnection(None, None, data, addr, broadcast=True)
            clientTh.start()