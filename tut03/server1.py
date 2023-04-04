import socket


def main():

    while True:
        # creating a socket for every new client connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
        port = 12345
        # binding socket
        s.bind(('', port))
        print("socket binded to %s" % (port))
        s.listen(0)
        print("Socket is listening..")
        # accepting the client socket and address
        c, addr = s.accept()
        print('Got connection from', addr)
        # closing the socket after recieving a connection, for next client new socket will be created, hence the while loop
        s.close()
        # while loop for a client
        while (True):
            # sending welcome msg
            c.send('Thank you for connecting\nProvide your input: '.encode())
            input = c.recv(1024).decode()  # recieving input
            print("Client: ", input)
            try:
                ans = str(eval(input))  # using eval to calculate expression
            except:
                ans = "Invalid input format"
            print("Response: ", ans)
            c.send(ans.encode())  # sending the ans of expression to client
            # asking for input from client, whether to continue or stop
            cont = c.recv(1024).decode()
            if (cont == "n"):  # if no then close the socket and break the client loop
                print("Connection closed with client", addr)
                c.close()
                break


if __name__ == "__main__":
    main()
