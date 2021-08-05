import socket
import os
import pandas as pd
import numpy as np


SEPARATOR = "<SEPARATOR>"

print("Server Started")
print("--------------------------------")


cols = ['Date', 'FoodID', 'Quantity', 'Cost']
df = pd.DataFrame(columns=cols)


if(os.stat("FoodBill.csv").st_size != 0):
    df = pd.read_csv('FoodBill.csv')

if 'Category' not in df.columns:
    df = df.assign(Category=np.NaN)
if 'Totalcost' not in df.columns:
    df = df.assign(Totalcost=np.NaN)

df["Quantity"] = df["Quantity"].astype(int)
df["Cost"] = df["Cost"].astype(int)


def add_row(conn_socket, date, foodid, quantity, cost):
    foodid_check = ["A", "D", "I", "B"]
    if(foodid[0] not in foodid_check):
        conn_socket.send(b"Food ID should start with A,D,I or B")
        return
    quantity = int(quantity)
    cost = int(cost)
    category = np.NaN
    total = np.NaN
    df.loc[len(df.index)] = [date, foodid, quantity, cost, category, total]
    df.to_csv('FoodBill.csv', index=False)
    conn_socket.send(b"Added Row Successfully")


def modification(conn_socket):

    df["Totalcost"] = ((df["Quantity"])*(df["Cost"]))
    df.to_csv('FoodBill.csv', index=False)
    conn_socket.send(b"Modified Total Cost Successfully")


def view(conn_socket):
    conn_socket.send(bytes(df.to_string(), 'utf-8'))


def update(conn_socket):

    df.loc[df["FoodID"].str.startswith("D"), "Category"] = "Dosa"
    df.loc[df["FoodID"].str.startswith("A"), "Category"] = "Apple"
    df.loc[df["FoodID"].str.startswith("B"), "Category"] = "Biriyani"
    df.loc[df["FoodID"].str.startswith("I"), "Category"] = "Italian"
    df.to_csv('FoodBill.csv', index=False)
    conn_socket.send(b"Updated Category Successfully")


def display_food_details(conn_socket, foodid, date):

    if(date == ""):
        new_df = df.loc[df["FoodID"] == foodid]
        conn_socket.send(bytes(new_df.to_string(), 'utf-8'))
        return
    new_df = df.loc[(df["FoodID"] == foodid) & (df["Date"] == date)]
    conn_socket.send(bytes(new_df.to_string(), 'utf-8'))


def on_new_client(clientsocket, addr, host):
    while True:
        msg = clientsocket.recv(1024).decode()
        args = msg.split(SEPARATOR)

        if(args[0] == "-1"):
            break
        elif(args[0] == "I"):
            add_row(clientsocket, args[1], args[2], args[3], args[4])
        elif(args[0] == "M"):
            modification(clientsocket)
        elif(args[0] == "V"):
            view(clientsocket)
        elif(args[0] == "U"):
            update(clientsocket)
        elif(args[0] == "F"):
            display_food_details(clientsocket, args[1], args[2])
    clientsocket.close()


s = socket.socket()
host = socket.gethostname()
port = 5001


print('Server started!')
print('Waiting for client...\n')

s.bind((host, port))
s.listen(5)
c, addr = s.accept()
print("Connected with:", addr)
on_new_client(c, addr, host)


s.close()
