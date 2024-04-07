import socket
import threading


Clients = []
Names = []

class Server():

    def __init__(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        SERVER = socket.gethostbyname(socket.gethostname())
        servPort = input("Enter Server Port: ")

        ADDR = (SERVER, int(servPort))
        self.ADDR = ADDR
        server.bind(ADDR)

        print(f'Server is listening on {ADDR}')

    def send_message(self, message):
        for connection in Clients:
            connection.send(message.encode("utf-8"))

    def start(self):
        while True:
            connection, addr = self.server.accept()
            print(f'User {str(addr)} has been added to the list')
            connection.send("Name?".encode("utf-8"))
            name = connection.recv(1024)
            Names.append(name)
            Clients.append(connection)
            print(f'The username chosen is {str(name)}')
            self.send_message(f'{name} is online')
    
    def handle_client(self, connection):

        while True:
            try:
                message = connection.recv(1024).decode('utf-8')
                self.send_message(message)
            except:
                index = Clients.index(connection)
                Clients.remove(connection)
                connection.close()
                name = Names[index]
                self.send_message(f'{name} has logged off'.encode('utf-8'))
                Names.remove(name)
                break

print("Server is starting up")
server = Server()
server.start()

