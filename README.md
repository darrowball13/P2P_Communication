# P2P_Communication

This is a very simplistic P2P communication that uses a TCP socket to allow clients to communicate directly with each other. If wanted, a user may also set up a server, which will solely keep track of all the users that have actively registered with the server, then send that list to any users who request it **Note: Server functiionality not implemented at the moment**

## Files

- **client.py**: Enables a User to set up a TCP socket and allow them to either receive messages from other users or send messages.
- **server.py**: Sets up a server to handle the list of known users. Clients need to actively register with the server in order to appear on the server list. **Note: Server functiionality not implemented at the moment**

## Usage

Python is required to run this code. 

**client.py**: To begin using, run the follow command:
> python client.py

This will prompt the User to enter the Port they wish to connect on, and a name that they wish to use for connections. After, the User will be presented with the following options:
- **_Users_**: This will print out the list of Users the current User has seen, including themselves
- **_Message_**: The user will be prompted to provide another Users IP Address and Port number. Once these are provided, they can type in a message that will be sent to the other User based on the provided IP/Port. Note that in order for this to work the other User must be in "receiving" mode
- **_Receive_**: This will put the user in "receiving" mode. They will be listening on their port for any incoming messages, and once a message is received the port will no longer be listening
- **_Disconnect_**: This will end the Users connection and exit the program
- **_Register_**: The user will be prompted to provide the server's IP address and Port number. Once connected to the server, the server will add the User to its list of known Users. 
    - **Note: This functionality is currently unavailable**


**server.py**: To begin using, run the follow command:
> python server.py

This will prompt the User to enter the Port they wish the server to act on. Once established, the server will constantly listen for incoming connections. Once a User connects, their connection will be added to the servers list of Clients, and the server will prompt them for a name that they will go by. If the server is prompted to provide it's list of clients, it will send the entire list to the User who requested it.



