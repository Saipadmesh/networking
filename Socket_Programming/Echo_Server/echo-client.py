import socket

HOST = '127.0.0.1'   # Server's hostname or IP address
PORT = 8800          # Port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello World')
    # bufsize argument of recv() is 1024, which is max amount of data that can be received at once
    data = s.recv(1024)

print('Received', repr(data))
