
from socket import *  # import socket module
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a sever socket
serverPort = 50000
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not found</h1></body></html>\r\n".encode())
        connectionSocket.close()  # Close client socket

serverSocket.close()
sys.exit()
