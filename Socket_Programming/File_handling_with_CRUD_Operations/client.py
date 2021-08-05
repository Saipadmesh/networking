import socket
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
host = socket.gethostname()
port = 5001

s.connect((host, port))
lst = [-1, 0, 1, 2, 3]
while True:
    number = int(
        input("0: Add new row\n1: Delete row\n2: Print data\n3:Save to file\nEnter option (-1 to break): "))

    if number in lst:
        send_str = str(number)
        if(number == 0):
            roll_num = input("Enter Roll Number: ")
            name = input("Enter name: ")
            cgpa = input("Enter CGPA: ")
            send_str = send_str+SEPARATOR+roll_num+SEPARATOR+name+SEPARATOR+cgpa
        if(number == 1):
            roll_num = input("Enter Roll Number: ")
            send_str = send_str+SEPARATOR+roll_num
        s.send(bytes(send_str, 'utf-8'))
        if(number == -1):
            break
    print(s.recv(1024).decode())
    print("\n")
s.close()
