import socket
import select
# socket_list for read list of select, sock_write list for write list of select
socket_list = []
sock_write = []
# socket_staus for storing the type of input expected(2 types, one expression, one yes or no)
socket_status = {}
# socket_input for storing the input
socket_input = {}
# function gets input seperated depending on case whether its expression, saving procedure same, but debug statements different at server
# simply stores recieved input in socket_input


def get_input(c):
    if (socket_status[c] == 0):
        input = c.recv(1024).decode()
        print("Client", c.getpeername(), input)
        socket_input[c] = input
    else:
        cont = c.recv(1024).decode()
        socket_input[c] = cont
# output function


def send_output(c):
    # case seperated, status->0 need to evaluate, 1 check whether to continue
    if (socket_status[c] == 0):
        # try used as output function called even when there is no input, as all sockets are part of write list
        try:
            inp = socket_input[c]
        except:
            return
        # calculate ans and send, similar to previous servers
        try:
            ans = str(eval(inp))
        except:
            ans = "Invalid input format"
        print("Response", c.getpeername(), ans)
        c.send(ans.encode())
        # change status, and delete the input
        socket_status[c] = 1
        del socket_input[c]
    else:
        try:
            cont = socket_input[c]
        except:
            return
        # similar logic as above case, just check if y or n, change status accordingly or close the socket and remove from lists
        if (cont == "n"):
            print("Connection closed with client", c.getpeername())
            socket_list.remove(c)
            c.close()
            sock_write.remove(c)
        elif (cont == "y"):
            c.send('Thank you for connecting\nProvide your input: '.encode())
            socket_status[c] = 0
            del socket_input[c]
# function to recieve connections from the main socket


def rcv_connection(s):
    c, addr = s.accept()
    c.send('Thank you for connecting\nProvide your input: '.encode())
    print('Got connection from', addr)
    # accept connection and add to both lists
    socket_list.append(c)
    sock_write.append(c)
    socket_status[c] = 0


def main():
    # create the main socket to recieve connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen()
    # add main socket to read list as well
    socket_list.append(s)
    print("Socket is listening..")
    while (True):
        # check for select every time at start of loop, 0 makes the select non blocking
        read, write, err = select.select(socket_list, sock_write, [], 0)
        # if socket is readable, check if it's main socket, and call appropriate functions
        for x in read:
            if (x == s):
                rcv_connection(s)
            else:
                get_input(x)
        # if socket is writable call output function
        for x in write:
            send_output(x)


if __name__ == "__main__":
    main()
