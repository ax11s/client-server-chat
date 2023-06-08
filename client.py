import socket
import threading


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345



ip = input('Server address: ')
uname = input('Set a nickname: ')
try:
    s.connect((ip, port))
except:
    print("\n\t Wrong server address\n")
try:
    s.send(uname.encode('ascii'))


    clientRunning = True

    def receiveMsg(sock):
        serverDown = False
        while clientRunning and (not serverDown):
            try:
                msg = sock.recv(1024).decode('ascii')
                print(msg)
            except:
                print('connection closed, press a button to close')
                serverDown = True

    threading.Thread(target = receiveMsg, args = (s,)).start()
    while clientRunning:
        tempMsg = input()
        msg = uname + ' >> ' + tempMsg
        if '/exit' in msg:
            clientRunning = False
            s.send('/exit'.encode('ascii'))
        else:
            s.send(msg.encode('ascii'))

except:print("\n\t Error\n")
