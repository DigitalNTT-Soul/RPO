import socket

def send_content(client, address, full_message):
    # make sure function happened
    print("send_content fired")

    # if there aren't enough arguments in th full_message, early retrn because we don't have what we need
    if len(full_message) < 2: return False
    
    # fetch file_name which should be second argument
    file_name = full_message[1]

    # begin parsing file_name to assemble relative paths to the desired file
    #   TODO: more error checking
    relative_folder_path = "rpo_server/content/"

    # match first character of file_name to see which content folder to find the package in
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
    
    # assemble relative path to the requested zip file
    file_path = relative_folder_path + file_name + '.zip'

    # open the file as 'read binary' to send it to client
    #   TODO: make sure it exists before trying to read it
    with open(file_path, 'rb') as buffer:
        # packet counte
        i = 0
        while True:
            # packet count display
            print(f"Sending chunk {i} of file {file_name} to {client}")
            i += 1

            # read a chunk from the file
            chunk = buffer.read(1024)

            # send that chunk
            client.send(chunk)

            # if that chunk was shorter than 1024 bytes, it's probably the end of file, so we break loop
            #   TODO: better end of file checking
            if len(chunk) < 1024:
                break

        print("Done Sending.")

        # close connection to client now that download is complete
        client.shutdown(socket.SHUT_WR)