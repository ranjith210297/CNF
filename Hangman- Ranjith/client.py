import socket
so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=8080
so.connect(('192.168.0.105',port))
while True:

    print("\n              Welcome to the game, Hangman!")
    print("-"*50)
    print("Select any One Option")
    print("1.New User ")
    print("2.Existing User \n")
    opition = input()
    so.sendall(opition.encode())

    while True:
        if(opition == "1"):
            userName = input("Enter your Name: ")
            so.send(userName.encode())

        elif(opition == "2"):
            existingName = input("Enter Your existing Username : ")
            so.send(existingName.encode())
        else:
            print("Enter Valid Input.")
            continue

        Status = so.recv(1024).decode()


        if Status == "start":
            print(so.recv(1024).decode())

            while True:
                msg = so.recv(1024).decode()

                if msg == "you won":
                    print(msg,end='')
                    so.close()
                    break
                elif msg[-1] == "1": 
                    print("entered")
                    print(msg[:-1], end='')
                    so.sendall(input().encode())
                else:
                    print(msg,end = '')
