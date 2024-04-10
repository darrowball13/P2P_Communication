import socket
import re
import sys
import threading


Clients = []
Names = []

class Server():

    def __init__(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        SERVER = socket.gethostbyname(socket.gethostname())
        self.SERVER = SERVER

    def send_message(self, message):
        for connection in Clients:
            connection.send(message.encode("utf-8"))

    def start(self):

        servPort = input("Enter Server Port: ")
        check_servPort = santitize_input_port(servPort)
        if check_servPort == "Invalid":
            print("Invalid port for Server. Exiting Program")
            sys.exit()

        ADDR = (self.SERVER, int(check_servPort))
        self.ADDR = ADDR
        server.bind(ADDR)

        print(f'Server is listening on {ADDR}')

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

def santitize_input_port(input):
    if not re.match("^[0-9]*$", input):
        print("Enter a valid port number")
        return "Invalid"
    else:
        return int(input)


print("Server is starting up")
server = Server()
server.start()

