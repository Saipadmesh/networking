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

cols = ['Date', 'User', 'Bandwidth', 'Time', 'Total']
df = pd.DataFrame(columns=cols)
# df = df.set_index('Roll_Number')
df.astype({'Bandwidth': int, 'Time': int, 'Total': int})
if(os.stat("File.csv").st_size != 0):
    # df = pd.read_csv('File.csv', index_col='Roll_Number')
    df = pd.read_csv('File.csv')

if 'ipAddress' not in df.columns:
    df = df.assign(ipAddress="")
df.index += 1


def add_row(conn_socket, date, user, bandwidth, time, ipAddress):
    try:
        bandwidth = int(bandwidth)
        time = int(time)
        total = bandwidth*time
        df.loc[len(df.index)] = [date, user, bandwidth, time, total, ipAddress]
        df.to_csv('File.csv', index=False)
        conn_socket.send(bytes(df.to_string(), 'utf-8'))
        # df.loc[roll_num] = new_row
        # df.to_csv('File.csv', index=True)
        #df.append(new_row, ignore_index=True)
        pass
        #conn_socket.send(b"Added Row Successfully")
    except:
        conn_socket.send(b"Operation failed")


def view_date(conn_socket, date):

    new_df = df.loc[df['Date'] == date]
    conn_socket.send(bytes(new_df.to_string(), 'utf-8'))
    try:
        pass
    except:
        conn_socket.send(b"Operation failed")


def view_user(conn_socket, user):

    try:
        new_df = df.loc[df['User'] == user]
        conn_socket.send(bytes(new_df.to_string(), 'utf-8'))
    except:
        conn_socket.send(b"Operation failed")


def total_sales(conn_socket):
    try:
        new_df = df.groupby(['Date']).agg(
            {'Total': 'sum'}).reset_index()[['Date', 'Total']]
        conn_socket.send(bytes(new_df.to_string(), 'utf-8'))
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
            add_row(clientsocket, args[1], args[2], args[3], args[4], args[5])
        elif(args[0] == "1"):
            view_date(clientsocket, args[1])
        elif(args[0] == "2"):
            view_user(clientsocket, args[1])
        elif(args[0] == "3"):
            total_sales(clientsocket)
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
