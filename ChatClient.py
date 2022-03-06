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
            # thread_send = threading.Thread(target=self.send, args=(msg,name))
            thread_receving = threading.Thread(target=self.receiving)
            # thread_send.start()
            thread_receving.start()

    def send(self, msg, name):
        while True:
            if msg:
                msg_from = f"{name}: {msg}"
                self.client_sock.send(msg_from.encode())


    def receiving(self):
        while True:
            msg = self.client_sock.recv(1024).decode()
            if msg == 'NAME':
                self.client_sock.send(self.name)



if __name__ == '__main__':
    client = Client()
    client.connect()





