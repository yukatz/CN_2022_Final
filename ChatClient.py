import random
import socket
import threading


class Client:
    def __init__(self):
        self.host = "localhost"
        self.port = 52000
        self.name = None
        self.portUDP = None
        self.file_dict = {}
        """Open TCP socket"""
        self.client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self):
            """Open TCP socket"""
            self.client_sock.connect((self.host, self.port))
            print("Connected")
            self.name = input("Enter your name: ")

            msg = self.client_sock.recv(1024).decode()
            if msg=='NAME':
                self.client_sock.send(self.name.encode())
            print(f"Hello {self.name} and welcome to our chat\n"
                  f" To send a message to all participants, type and send\n"
                  f" To send a message to one person, type * and then his nickname that you can find in clients list\n"
                  f" To download a file, type # and the the name include .type \n"
                  f" To see connected clients, type ""Clients list""\n"
                  f" To see files you can download, type ""Files list"""

                  f" To quit, type QUIT ")
            thread_send = threading.Thread(target=self.send, args=(self.client_sock,))
            thread_receiving = threading.Thread(target=self.receiving, args=(self.client_sock,))
            thread_send.start()
            thread_receiving.start()

    def send(self, client):
        while True:
            msg = input()
            client.send(msg.encode())

    def receiving(self, client):
        while True:
            msg = client.recv(1024).decode()
            msg_split = msg.split(" ")
            if msg == 'NAME':
                self.client_sock.send(self.name.encode())
            if msg[0]=='&':
                self.portUDP = client.recv(1024).decode()
                len = client.recv(1024).decode()
                udpSocket = threading.Thread(target=self.udp_client_connection)
                udpSocket.start()
            if msg_split[0] != self.name:
                print(msg)



    def udp_client_connection(self):
            clientSocketUdp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            clientSocketUdp.sendto("Im here".encode(), ('localhost', int(self.portUDP)))
            if clientSocketUdp:
                print("opened")
                modifiedMessage, serverAddress = clientSocketUdp.recvfrom(2048)
                if modifiedMessage=='lets play':
                    while clientSocketUdp:
                        modifiedMessage, serverAddress = clientSocketUdp.recvfrom(2048)
                        print(modifiedMessage)



if __name__ == '__main__':
    cli = Client()
    cli.connect()





