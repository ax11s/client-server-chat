import socket
import threading



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))

clients = {}

s.bind(('127.0.0.1', 12345))
s.listen()
print('Starcik serwerka :)')
print('IP: ' + ip)




def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = ' /all - to do wszystkich piszesz\n /msg - to piszesz do 1 typa np. /msg murzyn \n /exit - wyjscie \n /ludziki - to lista ludzi na serwerze \n /info - to jest to menu'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'Ludziki na serwerze :\n'
            found = False
            if '/ludziki' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) +'\t:' + name+'\n'
                client.send(response.encode('ascii'))
            elif '/info' in msg:
                client.send(help.encode('ascii'))
            elif '/all' in msg:
                msg = msg.replace('/all','')
                for k,v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '/exit' in msg:
                response = 'CLIENT DISCONNECTED'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                 
                print(uname + ' Wydupcyl z serwerka')

                clientConnected = False
            else:
                for name in keys:
                    if('/msg '+name) in msg:
                        msg = msg.replace('/msg '+name, '')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if(not found):
                    client.send('Zly targecik idiocie'.encode('ascii'))
        except:
            clients.pop(uname)


            clientConnected = False


        


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')



    client.send('Polczono, tu masz komeny: /info'.encode('ascii'))
    
    if(client not in clients):
        clients[uname] = client
        threading.Thread(target = handleClient, args = (client, uname, )).start()
        