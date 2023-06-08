import socket
import threading



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))

clients = {}

s.bind(('127.0.0.1', 12345))
s.listen()
print('Server started')
print('SERVER IP: ' + ip)




def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = ' /all - message all users \n /msg - message a single user ex. /msg user1 \n /exit - exit the program \n /users - list of the current users \n /info - '

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'Current users :\n'
            found = False
            if '/users' in msg:
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
                 
                print(uname + ' Left the server')

                clientConnected = False
            else:
                for name in keys:
                    if('/msg '+name) in msg:
                        msg = msg.replace('/msg '+name, '')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if(not found):
                    client.send('User not found'.encode('ascii'))
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
        
