import socket
from server_behaviors.send_module import send_content

ip = "10.0.0.68"
port = 4606
server_block = (ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_block)
server.listen(1)

while True:
    client, address = server.accept()
    full_message = client.recv(1024).decode('utf-8').split(',')

    if full_message[0] == "download":
        send_content(client, address, full_message)