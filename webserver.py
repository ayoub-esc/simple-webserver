import sys
import threading
from socket import *


SERVER_PORT = 6789

def client_handler(connectionSocket, connection_addr):
    try:
        message = connectionSocket.recv(4096).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send("\r\n".encode())
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except (IOError, IndexError):
        #Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())
        connectionSocket.send('Content-Type: text/html\r\n'.encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send('<html><body><h3>Error 404: File not found</h3></body></html>'.encode())
        connectionSocket.send("\r\n".encode())
        #Close client socket
        connectionSocket.close()
    
def run_server(server_port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(5)
    print("The server is ready to receive...")
    threads = []
    keep_going = True
    while keep_going:
        try:
            connection_socket, connection_addr = server_socket.accept()
            t = threading.Thread(target = client_handler, 
                                 args = (connection_socket, connection_addr))
            threads.append(t)
            t.start()
        except KeyboardInterrupt:
            keep_going = False
            server_socket.close()
    print("The server is closing...")

run_server(SERVER_PORT)