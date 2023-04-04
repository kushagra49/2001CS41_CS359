import socket
import threading
# function to handle a client, given its socket


def calculator(c, addr):
    # while loop to keep taking input till client exits
    while (True):
        # welocme msg
        c.send('Thank you for connecting\nProvide your input: '.encode())
        input = c.recv(1024).decode()  # recieve input
        print("Client", addr, input)
        try:
            ans = str(eval(input))  # using eval to calculate ans
        except:
            ans = "Invalid input format"
        print("Response", addr, ans)
        c.send(ans.encode())  # sending ans
        # recieving input to decide whether to continue or not
        cont = c.recv(1024).decode()
        if (cont == "n"):
            print("Connection closed with client", addr)
            c.close()
            break


def main():
    # creating socket once, binding and listening
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen()
    print("Socket is listening..")
    # loop to accept clients
    while (True):
        # accept connection
        c, addr = s.accept()
        print('Got connection from', addr)
        # create new thread with function created for each client and start it
        t1 = threading.Thread(target=calculator, args=(c, addr))
        t1.start()


if __name__ == "__main__":
    main()
