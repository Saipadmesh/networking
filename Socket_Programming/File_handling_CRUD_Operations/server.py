import socket
import _thread as thread
import os
import string
import pandas as pd
import numpy as np
import sys

SEPARATOR = "<SEPARATOR>"

print("This is a SERVER program")
print("--------------------------------")

# nn = input("Enter column name: ")
# dd = int(input("Enter column datatype: "))
# col_type[nn] = data_type[dd]

# nn = input("Enter column name: ")
# dd = int(input("Enter column datatype: "))
# col_type[nn] = data_type[dd]

cols = ['Roll_Number', 'Name', 'CGPA']
df = pd.DataFrame(columns=cols)
df = df.set_index('Roll_Number')
df.astype({'CGPA': float})
if(os.stat("File.csv").st_size != 0):
    df = pd.read_csv('File.csv', index_col='Roll_Number')

#df.index += 1


def add_row(conn_socket, roll_num, name, cgpa):
    new_row = {'Name': name, 'CGPA': float(cgpa)}

    try:
        df.loc[roll_num] = new_row
        df.to_csv('File.csv', index=True)
        conn_socket.send(b"Added Row Successfully")
    except:
        conn_socket.send(b"Operation failed")


def delete_row(conn_socket, roll_num):

    try:
        df.drop(roll_num, inplace=True)
        df.to_csv('File.csv', index=True)
        conn_socket.send(b"Row deleted Successfully")
    except:
        conn_socket.send(b"Operation failed")


def save(conn_socket):
    try:
        df.to_csv('File.csv', index=True)
        conn_socket.send(b"Saved Successfully")
    except:
        conn_socket.send(b"Operation failed")


############SOCKET CONNECTION#################


def on_new_client(clientsocket, addr, host):
    while True:
        msg = clientsocket.recv(1024).decode()
        args = msg.split(SEPARATOR)

        if(args[0] == "-1"):
            break
        elif(args[0] == "0"):
            add_row(clientsocket, args[1], args[2], float(args[3]))
        elif(args[0] == "1"):
            delete_row(clientsocket, args[1])
        elif(args[0] == "2"):
            clientsocket.send(bytes(df.to_string(), 'utf-8'))
        elif(args[0] == "3"):
            save(clientsocket)
    clientsocket.close()


s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 5001                # Reserve a port for your service.


print('Server started!')
print('Waiting for clients...\n')

s.bind((host, port))        # Bind to the port
s.listen(5)

while True:
    c, addr = s.accept()     # Establish connection with client.
    thread.start_new_thread(on_new_client, (c, addr, host))
#    ll = [host, addr, (end-start+1), "Data sent"]
#    log.append(pd.DataFrame(ll), ignore_index = True)

s.close()
