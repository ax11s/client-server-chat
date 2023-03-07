import socket
import threading
import datetime



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 12345
adress = '127.0.0.1'

clients = {}

s.bind((adress, port))
s.listen()
print('Starcik serwerka :)')
print('IP: ' + ip)


def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = '/all - to do wszystich piszesz\n /komendy - to masz to menu \n /exit - wydupiasz z serwera\n /ludziki - daje ci liste ludzikow na serwerze \n /msg - to piszesz do kogos bezposrednio np. /msg debil \n'

    while clientConnected:
        try:
            
            msg = client.recv(1024).decode('UTF-8')
            response = 'Ludziki na serwerku :\n'
            found = False
            
            if '/ludziki' in msg:

                clientNo = 0

                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) +'\t:' + name+'\n'
                client.send(response.encode('UTF-8'))

            elif '/komendy' in msg:
                client.send(help.encode('UTF-8'))

            elif '/all' in msg:
                msg = msg.replace('/all','')
                for k,v in clients.items():
                    v.send(msg.encode('UTF-8'))
                
            elif '/exit' in msg:
                response = 'Cwel sie rozlaczyl'
                client.send(response.encode('UTF-8'))
                clients.pop(uname)
                print(uname + ' LEFT')
                clientConnected = False

            else:

                for name in keys:
                    if('/msg '+name) in msg:
                        msg = msg.replace('@'+name, '')
                        clients.get(name).send(msg.encode('UTF-8'))
                        found = True

                if(not found):
                    client.send('Zly nick debilu'.encode('UTF-8'))

        except:
            clients.pop(uname)
            print(uname + ' LEFT')
            clientConnected = False


        


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    print('Polaczono z serwerkiem'%str(uname))
    print('------------------------------------------------------------------------------------------------------')
    client.send('Elo, tu masz komendy: /komendy'.encode('ascii'))
    
    if(client not in clients):
        clients[uname] = client
        threading.Thread(target = handleClient, args = (client, uname, )).start()
        