import socket
import threading
import os
from msilib.schema import File


class Server:
    def __init__(self):
        self.host = ""
        self.port = 50000
        self.clients_list = {}
        self.files = os.listdir('.')
        self.filepack1 = {}
        self.filepack2 = {}


    def connect(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((self.host, self.port))
        print('The Server is Up')

        while True:
            serv_sock.listen(1)
            client, address = serv_sock.accept()
            client.send('NAME'.encode())
            client_name = client.recv(1024).decode()
            print(f"{client_name} connected")
            self.clients_list[client] = client_name
            self.broadcast(f"{client_name} connected",client)
            self.start_listen(client)

    def start_listen(self, client):
        client_thread = threading.Thread(target=self.listen, args=(client,))
        client_thread.start()

    def listen(self, client):
        while True:
            msg = client.recv(1024).decode()
            split_msg = msg.split()  # split the messege a *name of destination
            print(split_msg)
            if msg:
                if msg[0] == '*':
                    priv_msg = split_msg[1:]  # without a *name of destination
                    priv_msg = ','.join(priv_msg)
                    dest = split_msg[0][1:]
                    if dest in self.clients_list.values():
                        self.privat_conf(f"{self.clients_list[client]} says: {priv_msg}", dest)
                    else:
                        print(f"{dest} does't exist or disconnected")

                elif msg[0] == '#':
                    file_name = split_msg[0][1:]  # file name (without #)
                    if file_name in self.files:
                        udp_con = threading.Thread(target=self.udp_conn, args=(file_name,client,))
                        udp_con.start()
                        print("Udp thread started")
                        self.file_cut(file_name)
                        print(f"{self.filepack1[0]}")
                        udp_con.send(f"{file_name} start downloading".encode())
                    else:
                        print(f"{self.clients_list[client]} tried to download not existing file")
                        client.send("This file doesn't exist".encode())


                elif msg == 'QUIT':
                    print(f"{self.clients_list[client]} has been disconnected : ")
                    self.clients_list.pop(client)

                else:
                    msg_from = f"{self.clients_list[client]} says: {msg}"
                    print(msg_from)
                    self.broadcast(msg_from,client)

    def broadcast(self, message, client):
        for key in self.clients_list.keys():
            if key != client:
                print(self.clients_list[key])
                print(message)
                key.send(message.encode())

    def privat_conf(self, message, dest):
        for key, val in self.clients_list.items():
            if val == dest:
                key.send(message.encode())

    def udp_conn(self, file,client):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((self.host, self.port))
        udpCli, address = serverSocket.accept()
        if serverSocket:
            client.send(f"& {13} {serverSocket}".encode())
            print("udp up")
        while True:
            msg = serverSocket.recv(1024).decode()
            if msg=='im here':
                udpCli.send(f"{file} start download".encode())

    def file_cut(self, file_name):
        file = open(file_name, 'rb')
        packet = file.read(1024)
        index = 0
        while packet:
            self.filepack1[index] = packet
            index += 1
            packet = file.read(1024)
        file.close()




if __name__ == '__main__':
    server = Server()
    server.connect()
