import socket
import re
import sys
import sqlite3
import datetime

# Reference: https://github.com/JeffC25/peer-to-peer/tree/main/src

# Creates a Dictionary of the Clients the User has seen, including themselves
Clients = {}

# Client class to create client instances for communication with each other
class Client():

    # Initializes the client class with the port they want to connect on and the display name
    def __init__(self):
        SERVER = socket.gethostbyname(socket.gethostname())
        self.SERVER = SERVER
        

    # Binds the client socket for communications. Set up in a way to allow back and forth communication
    def start_client(self):

        servPort = input("Enter Client Port: ")
        name = input('Whats the name?: ')
        check_servPort = santitize_input_port(servPort)
        check_name = santitize_input_text(name)
        if check_servPort == "Invalid" or check_name == "Invalid":
            print("Client not initialized correctly. Exiting Program")
            sys.exit()

        self.name = name
        self.servPort = servPort
        
        ADDR = (self.SERVER, int(servPort))
        self.ADDR = ADDR

        Clients[name] = ADDR

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.server.bind(self.ADDR)

    # Connects to the designated port for message exchange
    def connect(self, friend, friend_port):
        self.server.connect((friend, friend_port))

    # Puts itself in listening mode in order to receive messages
    def listen(self):
        self.server.listen()
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
        santitize_input_text(command)
    return command

# Checks text inputs for validity (no special characters involved)
def santitize_input_text(text):

    if not re.match("^[a-zA-Z0-9]*$", text):
        print("Enter valid text")
        return "Invalid"
    else:
        return text
    
# Check numerical inputs for validity (only includes numbers 0-9, no text or special characters)
def santitize_input_port(input):
    if not re.match("^[0-9]*$", input):
        print("Enter a valid port number")
        return "Invalid"
    else:
        return int(input)

# Starts up the Client instance
print("Logging on...")
client = Client()
client.start_client()


# Create a messages database with a messages table if it doesn't already exist. This will store all messages sent/received
# by the current user
db_connect = sqlite3.connect("messages.db")

db_cur = db_connect.cursor()

# Creates table in database. Note name not included right now
db_cur.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INT PRIMARY KEY,
    sender_ip TEXT NOT NULL,
    sender_port INT NOT NULL,
    receiver_ip TEXT NOT NULL, 
    receiver_port INT NOT NULL,                         
    message TEXT NOT NULL,
    time_sent TIMESTAMP NOT NULL)''')


db_connect.commit()
db_connect.close()


# Handles the user_option inputs
while True:

    # initiates user_options
    command = user_options()

    if command == "Users":
        find_friend()
        continue

    # Asks the User for the IP and Port of their friend, then puts the User in the mode to send messages
    # Sends out the chat message to friend, then closes connection to them after in order to be able to receive
    elif command == "Message":
        friend = input("Friend IP: ")
        friend_port = input("Friend Server Port: ")

        # Checks input port for validiity. If invalid, returns to main menu
        check_port = santitize_input_port(friend_port)
        if check_port == "Invalid":
            print("Returning to Main Menu...")
            continue

        client.connect(friend, check_port)

        chat = input("Enter Message: ")
        client.send_Message(chat)
        client.server.close()

        message_connect = sqlite3.connect("messages.db")
        message_cur = message_connect.cursor()

        current_time = datetime.datetime.now()

        # Insert message data into database table
        sql = """INSERT INTO messages (sender_ip, sender_port, receiver_ip, receiver_port, message, time_sent)
                VALUES (?, ?, ?, ?, ?, ?)"""
        message_cur.execute(sql, (client.SERVER, client.servPort, friend, friend_port, chat, current_time))

        # Commit the changes to the database and close db connection
        message_connect.commit()
        message_connect.close()

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


