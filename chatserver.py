import socket,sys, re
from threading import Thread
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if (len(sys.argv) < 2):
    print("ENTER: python chatserver.py hostname:port")
    sys.exit()
input_list = sys.argv[1].split(':')
HOSTNAME =input_list[0]
PORT = int(input_list[1])
cli = {}
cli_sockets = []
socket.bind((HOSTNAME,PORT))

def clientconnection() :
    while True :
        c,c_addr = socket.accept()
        print("%s:%s has connected." % c_addr)
        c.send("Hello 1 \n")
        cli_sockets.append(c)
        Thread(target= manageconnection, args=(c,c_addr)).start()

def manageconnection(c,c_addr) :

    x = c.recv(1024)
    nick = x.strip("NICK ")
    if len(nick)<=12 and re.match("^[A-Za-z0-9\_]+$",nick) is not None:
        c.send("OK \n")
    else :
        c.send(" ERROR - nickname is not valid \n")
        nick= 'unkwown'
    message = "%s has joined the chat \n"% nick
    broadcast(message,c)
    cli[c] = nick
    while True :
        y = c.recv(1024).decode('utf-8')
        message = y.strip("MSG ")
        if not message:
            c.close()
            del cli[c]
            sendname = "%s has left the chat \n"% nick
            print("%s:%s has diconnected." % c_addr)
            broadcast(sendname,c)
            break
        else :
            if len(message) > 255 and re.match("^[^\x00-\x7F]*$",message) is None:
                c.send("ERROR - message is not valid")
                send_message = "MSG "+nick +" "
            else:
                send_message = "MSG "+nick +" "+ message
            broadcast(send_message,c)

def broadcast(message, conn_cli):
    for i in cli_sockets:
        if i != socket and i != conn_cli :
            try:
                i.send(message.encode('utf-8'))
            except:
                pass

while True:
    socket.listen(100)
    print("Waiting for connections")
    program = Thread(target=clientconnection)
    program.start()
    program.join()
    socket.close()
