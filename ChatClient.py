import socket
import threading


class Client:
    def __init__(self):
        self.host = "localhost"
        self.port = 50000
        self.name = None
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
                  f" To download a file, type ""file"" and the the name include .type \n"
                  f" To quit, type QUIT ")
            thread_send = threading.Thread(target=self.send())
            thread_receiving = threading.Thread(target=self.receiving)
            thread_send.start()
            thread_receiving.start()

    def send(self):
        while True:
            msg = input()
            self.client_sock.send(msg.encode())

    def receiving(self):
        print("msg")

        while True:
            msg = self.client_sock.recv(1024).decode()
            print("msg")
            if msg == 'NAME':
                self.client_sock.send(self.name.encode())
            else:
                print(msg)






if __name__ == '__main__':
    client = Client()
    client.connect()





