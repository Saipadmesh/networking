import socket
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8800  # Port to listen on (only ports>1023 can be used)

# AF_INET is the internet address family for IPv4
# SOCK_STREAM is the socket type for TCP
# bind() is used to associate socket with a specific network interface and port number
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # We get a new socket object [conn] from accept(), which is the socket used to communicate with the client
    conn, addr = s.accept()
    with conn:  # The with statement closes the socket automatically
        print('Connected by', addr)
        while True:
            data = conn.recv(BUFFER_SIZE).decode()
            filename, filesize = data.split(SEPARATOR)
            filename = os.path.basename(filename)
            #filesize = int(filesize)
            with open(filename, 'r+') as f:
                text = f.read().split()
                if(text[0] == "Saipadmesh" and text[1] == "sp1211"):
                    f.write("\nSize of file is "+filesize)
                    conn.sendall(b"Authorization Successful!!")
                else:
                    conn.sendall(b"Incorrect username and password!!")
                break
            if not data:
                break
