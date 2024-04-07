import socket

# Reference: https://github.com/JeffC25/peer-to-peer/tree/main/src

# Creates a Dictionary of the Clients the User has seen, including themselves
Clients = {}

# Client class to create client instances for communication with each other
class Client():

    # Initializes the client class with the port they want to connect on and the display name
    def __init__(self):
        SERVER = socket.gethostbyname(socket.gethostname())
        servPort = input("Enter Client Port: ")

        name = input('Whats the name?: ')
        self.name = name
        
        ADDR = (SERVER, int(servPort))
        self.ADDR = ADDR

        Clients[name] = ADDR

    # Binds the client socket for communications. Set up in a way to allow back and forth communication
    def start_client(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.server.bind(client.ADDR)

    # Connects to the designated port for message exchange
    def connect(self, friend, friend_port):
        self.server.connect((friend, friend_port))


    # Puts itself in listening mode in order to receive messages
    def listen(self):
        self.server.listen(1)
        print(f'Listering on {self.ADDR}...')
        connection, addr = self.server.accept()
        return connection, addr

    # Receives an incoming communication and prints it for the receiver. Closes the connection after to allow communication back
    def get_Message(self, connection, addr):
        incoming = connection.recv(1024)
        print(f"{addr}:", incoming.decode())
        connection.close()

    # Sends a message to a connected client.
    def send_Message(self, message):
        self.server.send(message.encode('utf-8'))
        self.server.close()

# Prints out Users the Client has seen, including itself
def find_friend():
    for user in Clients:
        print(f'{str(user)}: {Clients[user]}')

# Allows the User to select between multiple options, and doesn't shut down until a command is seen
def user_options():
    command = input("Enter Command ('Register', 'Message', 'Users', 'Disconnect', 'Receive'): ")
    while not command:
        command = input("Enter Command ('Register', 'Message', 'Users', 'Disconnect', 'Receive'): ")
    return command

# Starts up the Client instance
print("Logging on...")
client = Client()

# Handles the user_option inputs
while True:

    # Binds the Client Socket and initiates user_options
    client.start_client()
    command = user_options()

    if command == "Users":
        find_friend()
        continue

    # Asks the User for the IP and Port of their friend, then puts the User in the mode to send messages
    # Sends out the chat message to friend, then closes connection to them after in order to be able to receive
    elif command == "Message":
        friend = input("Friend IP: ")
        friend_port = int(input("Friend Server Port: "))

        client.connect(friend, friend_port)

        chat = input("Enter Message: ")
        client.send_Message(chat)
        client.server.close()
        continue
    
    # Disconnects the User
    elif command == "Disconnect":
        break

    # Puts the User in the mode to receive messages, and waits for Friend to send message. Closes connection after
    elif command == "Receive":
        connection, addr = client.listen()
        client.get_Message(connection, addr)
        connection.close()
        client.server.close()
        continue

    # If an unrecognized command is seen, asks the User to supply command again
    else:
        print("Enter a Valid Command")
        continue

    # Connects with the Server Instance, which should hold the master list of all Users online. 
    # Note: I want to build functionality where Users can share information directly, but hasn't been implemented yet
    # Note: Does not work currently, which is why it's commented out

    '''
    elif command == "Register":
        print("Enter the Server information to get active users")
        server_ip = input("Server IP: ")
        server_port = int(input("Server Port: "))

        client.connect(server_ip, server_port)
        continue
    '''


