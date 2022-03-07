import socket
import threading
import os


class Server:
    def __init__(self):
        self.host = ""
        self.port = 50000
        self.clients_list = {}
        self.files = os.listdir('.')

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
            self.broadcast(f"{client_name} connected")
            self.start_listen(client)


    def start_listen(self,client):
        client_thread = threading.Thread(target=self.listen, args=(client,))
        client_thread.start()


    def listen(self, client):
        while True:
           msg = client.recv(1024).decode()
           split_msg = msg.split()  # slit the messege a *name of destination
           if msg:
               if msg[0] == '*':
                   priv_msg = split_msg[1:]  # without a *name of destination
                   dest = split_msg[0][1:]
                   if dest in self.clients_list:
                      self.privat_conf(priv_msg, self.clients_list[client], dest)
                   else:
                       print(f"{dest} does't exist or disconnected")

               elif msg[0] == '#':
                   file_name = split_msg[0][1:]  # file name (without #)
                   if file_name in self.files:
                       print(f"{file_name} start downloading")
                   else:
                       print("This file does't exist")


               elif msg=='QUIT':
                   print(f"{self.clients_list[client]} has been disconnected : ")
                   self.clients_list.pop(client)

               else:
                   msg_from = f"{self.clients_list[client]} says: {msg}"
                   print(msg_from)
                   self.broadcast(msg_from)

    def broadcast(self, message):
        print("br")
        for key in self.clients_list.keys():
            print(self.clients_list[key])
            print(message)
            key.send(message.encode())

    def privat_conf(self, message, src, dest):
        for key in self.clients_list.keys():
            key.send(message)


if __name__ == '__main__':
    server = Server()
    server.connect()


