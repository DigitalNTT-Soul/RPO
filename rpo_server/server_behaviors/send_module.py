import socket

def send_content(client, address, full_message):
    print("send_content fired")
    if len(full_message) < 2: return False
    
    file_name = full_message[1]
    relative_folder_path = "rpo_server/content/"
    match file_name[0]:
        case 'm':
            relative_folder_path += "modules/"
        case 'e':
            relative_folder_path += "system_expansions/"
        case 's':
            relative_folder_path += "systems/"
        case default:
            print("Invalid file type requested.")
            return False
    
    file_path = relative_folder_path + file_name + '.zip'

    with open(file_path, 'rb') as buffer:
        i = 0
        while True:
            print(f"Sending chunk {i} of file {file_name} to {client}")
            i += 1

            chunk = buffer.read(1024)
            client.send(chunk)
            if len(chunk) < 1024:
                break
        print("Done Sending.")
        client.shutdown(socket.SHUT_WR)