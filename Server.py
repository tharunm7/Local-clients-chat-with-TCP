import threading
import socket

host = '127.0.0.1'                                              #localhost
port = 54321                                                    #random unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        clinet, address = server.accept()
        print(f"connected with (string{address})")

        clinet.send('NICK'.encode('ascii'))
        nickname = clinet.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(clinet)

        print(f'nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        clinet.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(clinet,))
        thread.start()
print("Server is ready....")
receive()