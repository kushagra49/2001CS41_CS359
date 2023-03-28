# Import socket module
import socket		
import sys	
def main():
    n=len(sys.argv)
    if(n!=3):
        print("Enter 2 command line arguments only, first hostname or ip, second port number of server")
        quit()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
    port = int(sys.argv[2])			
    try:
        s.connect((sys.argv[1], port))
    except ConnectionRefusedError:
        print("Server Busy, try again later")
        quit()
    except:
        print("Invalid IP or Port")
        quit()
    while(True):
        welcome=s.recv(1024).decode()
        print (welcome)
        tocal=input()
        s.send(tocal.encode())
        print("Response:",s.recv(1024).decode())
        while(True):
            print("Do you wish to Continue?(y/n)")
            i=input()
            if(i=="y"):
                s.send(i.encode())
                break
            elif(i=="n"):
                s.send(i.encode())
                s.shutdown(2)
                s.close()
                quit()
            else:
                "Provide y/n only"

if __name__ == "__main__":
    main()
	
