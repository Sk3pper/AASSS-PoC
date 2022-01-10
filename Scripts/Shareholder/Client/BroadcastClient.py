import socket
import sys


import socket

SERVER = "10.10.10.255"
PORT = 7000
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    out_data = raw_input()
    # out_data = 'ei'
    client.sendto(out_data, (SERVER, PORT))
    if out_data == 'bye':
        break
client.close()

