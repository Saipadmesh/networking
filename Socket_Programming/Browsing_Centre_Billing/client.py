import socket
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
host = socket.gethostname()
ipAddr = socket.gethostbyname(host)
port = 5001

s.connect((host, port))
lst = [-1, 0, 1, 2, 3]
while True:
    number = int(
        input("0: Add new row\n1: View By Date\n2: View By User\n3: Total Sales\nEnter option (-1 to break): "))

    if number in lst:
        send_str = str(number)
        if(number == 0):
            date = input("Enter Date: ")
            user = input("Enter user: ")
            bandwidth = input("Enter bandwidth: ")
            time = input("Enter time: ")
            send_str = send_str+SEPARATOR+date+SEPARATOR + \
                user+SEPARATOR+bandwidth+SEPARATOR+time+SEPARATOR+ipAddr
        if(number == 1):
            date = input("Enter Date: ")
            send_str = send_str+SEPARATOR+date
        if(number == 2):
            user = input("Enter User: ")
            send_str = send_str+SEPARATOR+user

        s.send(bytes(send_str, 'utf-8'))
        if(number == -1):
            break
        print(s.recv(1024).decode())
    else:
        print("Enter a valid number")
    print("\n")
s.close()
