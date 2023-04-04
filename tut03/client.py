import socket
import sys


def main():
    # check if appropriate number of command line arguments are provided
    n = len(sys.argv)
    if (n != 3):
        print("Enter 2 command line arguments only, first hostname or ip, second port number of server")
        quit()
    # create the socket, af_inet for ipv4, sock_stream for tcp
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2])
    # get ip and port from command line args
    # connect, try and excpet for error handling if server is busy or connection was refused
    try:
        s.connect((sys.argv[1], port))
    except ConnectionRefusedError:
        print("Server Busy, try again later")
        quit()
    except:
        print("Invalid IP or Port")
        quit()
    # while loop for client
    while (True):
        # recieve welcome msg
        welcome = s.recv(1024).decode()
        print(welcome)
        tocal = input()
        # get and send input
        s.send(tocal.encode())
        # recieve the response and print it
        print("Response:", s.recv(1024).decode())
        # ask for input to continue or not in client itself
        # while loop to get only y or n as input, if y send it to server, if n close socket and quit
        while (True):
            print("Do you wish to Continue?(y/n)")
            i = input()
            if (i == "y"):
                s.send(i.encode())
                break
            elif (i == "n"):
                s.send(i.encode())
                s.shutdown(2)
                s.close()
                quit()
            else:
                "Provide y/n only"


if __name__ == "__main__":
    main()
