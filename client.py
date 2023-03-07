import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

nickname = input("Enter your nickname: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("connected succesfuly")
    while True:
        message = input("::")
        full_message = f"{nickname}: {message}"
        s.sendall(full_message.encode())
        data = s.recv(1024)
        print(data.decode())