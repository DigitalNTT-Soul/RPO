import socket
from server_behaviors.send_package import send_content

# define and assemble ip and port for socket creation and binding
ip = "10.0.0.68"
port = 4606
server_block = (ip, port)

# create socket to handle the connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server info to the socket
server.bind(server_block)

# listen for 1 connection?
server.listen(1)

while True:
    # accept the connection from the client
    client, address = server.accept()
    print(f"Connection received from client at {address}")

    # receive message from client (requesting the file)
    full_message = client.recv(1024)
    # decode the message into a usable string format
    full_message = full_message.decode('utf-8')
    
    # message should have comma-separated arguments
    full_message = full_message.split(':')

    # if first argument is the download command, pass the client info and the full message to the send_content function
    if full_message[0] == "download":
        send_content(client, address, full_message)

    # close connection to client now that download is either complete or failed
    print("closing connection")
    client.shutdown(socket.SHUT_WR)