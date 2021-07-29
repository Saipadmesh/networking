import socket
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
filename = "test.txt"
filesize = os.path.getsize(filename)
# -------------------------
uname = input("Enter username: ")
pw = input("Enter password: ")
with open(filename, 'w') as file:
    file.write(uname+" "+pw)
# -------------------------

HOST = '127.0.0.1'   # Server's hostname or IP address
PORT = 8800          # Port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected...')
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # bufsize argument of recv() is 1024, which is max amount of data that can be received at once
    data = s.recv(BUFFER_SIZE)

print('Received: ', repr(data))
