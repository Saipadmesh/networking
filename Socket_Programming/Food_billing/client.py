import socket
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
host = socket.gethostname()
ipAddr = socket.gethostbyname(host)
port = 5001

s.connect((host, port))
lst = ["-1", "I", "M", "V", "U", "F"]
while True:
    input_text = input(
        "I: Insertion\nM: Modification\nV: View\nU: Update\nF: Display details based on FoodID \nEnter option (-1 to break): ")

    if input_text in lst:
        send_str = input_text
        if(input_text == "I"):
            date = input("Enter Date: ")
            foodid = input("Enter FoodID: ")
            quantity = input("Enter Quantity: ")
            cost = input("Enter cost: ")
            send_str = send_str+SEPARATOR+date+SEPARATOR + \
                foodid+SEPARATOR+quantity+SEPARATOR+cost

        if(input_text == "F"):
            foodid = input("Enter FoodID: ")
            date = input("Enter Date(optional-can be blank): ")
            send_str = send_str+SEPARATOR+foodid+SEPARATOR+date

        s.send(bytes(send_str, 'utf-8'))
        if(input_text == "-1"):
            s.close()
            break
        print(s.recv(1024).decode())
    else:
        print("Enter a valid input")
    print("\n")
