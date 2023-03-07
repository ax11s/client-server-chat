import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345



ip = input('Podaj adresik serwera: ')
uname = input('Podaj nick: ')
try:
    s.connect((ip, port))
except:
    print("\n\t ZLY ADRES AASDDAASDA\n")
try:
    s.send(uname.encode('UTF-8'))


    running = True

    def receiveMsg(sock):
        serverdead = False
        while running and (not serverdead):
            try:
                msg = sock.recv(1024).decode('UTF-8')
                print(msg)
            except:
                print('W SERWEJ JEBNEL PIERUN \n kliknij cos zeby zamknac kienta')
                serverdead = True

    threading.Thread(target = receiveMsg, args = (s,)).start()
    while running:
        tempMsg = input()
        msg = uname + ' >> ' + tempMsg
        if '/exit' in msg:
            running = False
            s.send('/exit'.encode('UTF-8'))
        else:
            s.send(msg.encode('UTF-8'))

except:
    print("\n\t Kurwa nwm error te\n")
