# P2P_Communication

This is a very simplistic P2P communication that uses a TCP socket to allow clients to communicate directly with each other. If wanted, a user may also set up a server, which will solely keep track of all the users that have actively registered with the server, then send that list to any users who request it **Note: Server functiionality not implemented at the moment**

## Files

- **client.py**: Enables a User to set up a TCP socket and allow them to either receive messages from other users or send messages.
- **server.py**: Sets up a server to handle the list of known users. Clients need to actively register with the server in order to appear on the server list. **Note: Server functiionality not implemented at the moment**

## Usage

Python is required to run this code. 

**client.py**: To begin using, run the follow command:
> python client.py




