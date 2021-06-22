

from socket import *
import sys

SERVER_NAME = 'localhost'
SERVER_PORT = 12000

def run_client(server_name, server_port, filename):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    request = "GET /"+ filename + " HTTP/1.1\r\n Host: localhost:6789\r\n\r\n"
    client_socket.sendall(request.encode())
    message = ""
    count = 0
    while count < 4:
        fromServer = client_socket.recv(4096).decode()
        if(fromServer.count("\r\n")):
            count+=fromServer.count("\r\n")
        message = message + fromServer
    print(message)
    client_socket.close()
    
if __name__ == "__main__":
    sn = sys.argv[1] if len(sys.argv) > 1 else SERVER_NAME
    sp = int(sys.argv[2]) if len(sys.argv) > 2 else SERVER_PORT
    filename = sys.argv[3] if len(sys.argv) > 3 else ""
    run_client(sn, sp, filename)