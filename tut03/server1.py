import socket			

def main():
    
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
        print ("Socket successfully created")
        port = 12345	
        s.bind(('', port))		
        print ("socket binded to %s" %(port))
        s.listen(0)
        print("Socket is listening..")
        c, addr = s.accept()
        print ('Got connection from', addr )
        s.close()
        while(True):	
            c.send('Thank you for connecting\nProvide your input: '.encode())
            input=c.recv(1024).decode()
            print("Client: ",input)
            try:
                ans=str(eval(input))
            except:
                ans="Invalid input format"
            print("Response: ",ans)
            c.send(ans.encode())
            cont=c.recv(1024).decode()
            if(cont=="n"):
                print("Connection closed with client", addr)
                c.close()
                break

if __name__ == "__main__":
    main()
