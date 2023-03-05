import socket, config
from zipfile import ZipFile

ip = config.SERVER_IP
port = config.SERVER_PORT
server_block = (ip, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect(server_block)

file_name = "m00000002"
folder_path = "rpo_client/modules/"

relative_path = f"{folder_path}{file_name}.zip"

message = f"download,{file_name}"

with open(relative_path, 'wb') as file_object:
    server.send(bytes(message, config.MESSAGE_ENCODING))
    i = 0
    while True:
        print(f"Receiving block {i} of file {file_name}")
        i += 1
        response = server.recv(1024)
        file_object.write(response)
        if len(response) < 1024:
            break
    print("Done receiving.")

