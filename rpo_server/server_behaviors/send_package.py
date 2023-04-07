import socket

def len_of_num(i):
    # simply get the digit-count of an int by getting the string length of its absolute value form
    return len(str(abs(i)))

def byte_me(data: str):
    # convert data into bytes unless they already are
    if isinstance(data, bytes):
        return data
    else:
        return bytes(data, 'utf-8')

def throw_server_error(error_message: str, client = None):
    # pseudo-safe error message dumping in case of emergencies.
    #   also attempts to inform the client about errors, if one
    #   is both provided and reachable
    print(error_message)
    if client:
        try:
            client.send(byte_me(error_message))
        except Exception as e:
            print(f"FURTHER: Could not forward error message to client!\n{e}")
            return False

def parse_package_name_to_file_path(package_name, client_included_for_errors):
    # parses the first character of the package_name to determine which
    #   subfolder of "rpo_server/content" we should look for the package in
    relative_folder_path = "rpo_server/content/"
    match package_name[0]:
        case 'm':
            relative_folder_path += 'modules/'
        case 'e':
            relative_folder_path += 'system_expansions/'
        case 's':
            relative_folder_path += 'systems/'
        case default:
            throw_server_error("Error: Invalid file type requested.", client_included_for_errors)
            return False
        
    # assemble the full file_path to the zip in question
    file_path = relative_folder_path + package_name + '.zip'
    return file_path

def get_packets_from_file(file_path):
    # open the zip file as read-binary, pump it into a dictionary
    #   and return that dictionary for later use elsewhere
    with open(file_path, 'rb') as buffer:
        # prep the dictionary to hold the packets
        packet_dict = {}
        # loop until file is empty
        while True:
            # dict starts at length 0
            packet_num = len(packet_dict)
            # read a chunk out of the buffer, being careful about 
            #   packet lengths
            chunk = buffer.read(1023 - len_of_num(packet_num))
            # if the chunk is empty, break the loop and return the dict
            if chunk == b'':
                break
            # convert packet_num to bytes
            packet = byte_me(f"{packet_num}:")
            # concatenate the chunk onto the packet_num to create a full packet
            packet = packet + chunk
            # quickly check the packet to determine if it's safe to send
            packet_check = packet.split(b':',1)
            if len(packet_check) != 2:
                # TODO find a way to seek backward to the beginning of the failed packet
                #   and then use the 'continue' keyword to re-attempt this cycle of the loop
                throw_server_error(packet)
                return False
            # if everything checks out, packet goes in the dict
            packet_dict[packet_num] = packet

        # return the dict
        return packet_dict

def send_packet(client, packet):
    # safer way to send a packet
    while True:
        # repeatedly try to send it until either an exception occurs
        #   (likely a disconnection) or the packet sends in its full length
        try:
            # send the packet and get the number of bytes successfully sent
            sent_bytes_count = client.send(packet)
            # compare the number of bytes sent to the length of the packet
            if sent_bytes_count == len(packet):
                return True
        # if it fails, complain to the logs (but not the client) and report
        #   failure to calling function
        except Exception as e:
            throw_server_error(e)
            return False

def send_file_packet(client, packet_dict: dict, packet_num: int):
    # repeatedly attempt to send the specified file packet until
    #   the client confirms they have received and accepted that packet
    #   as valid
    while True:
        # pull packet out of dictionary
        packet = packet_dict[packet_num]
        # send it
        send_status = send_packet(client,packet)
        # confirm it sent correctly
        print(f"Sent {packet_num}")
        if not send_status:
            # if it didn't, we reattempt by going back to the top of the loop
            continue
        
        # the expected response if the packet is accepted is the following
        expected_positive_response = byte_me(f"{packet_num}:+")
        # wait for the client to send their response
        client_received_status = client.recv(1024)
        # if the client's response is that they accepted the packet, we leave here
        if client_received_status == expected_positive_response:
            break

def send_file(client, package_name, file_path):
    # if any exceptions occur, soft-throw them with throw_server_error()
    try:
        # open zip file into packet_dict
        packet_dict = get_packets_from_file(file_path)
        # get length of dict for later math
        packet_count = len(packet_dict)
        # send client file_exists confirmation and a packet_count to expect
        package_stats = byte_me(f"{package_name}:{packet_count}")
        send_status = send_packet(client, package_stats)
        if not send_status:
            return False
        
        # receive client's ready (or abort) message
        ready_message = client.recv(1024)
        
        # if client wasn't ready
        if ready_message != b'ready':
            # complain, but don't include client in the complaint
            #   because that could cause some sort of feedback loop
            throw_server_error(ready_message) 

        # loop through packets and send+confirm them one at a time
        for packet_num in range(packet_count):
            send_file_packet(client, packet_dict, packet_num)

        # when all packets have been sent
        send_packet(client, b'done')

    except Exception as e:
        throw_server_error(e, client)
        return False

def send_content(client, address, full_message):
    # process download request for proper formatting
    if len(full_message) < 2:
        error_message = "ERROR:content request improperly formatted!"
        throw_server_error(error_message, client)
        return False
    
    # pull package_name out of download request
    package_name = full_message[1]

    # parse to file_path
    file_path = parse_package_name_to_file_path(package_name,client)
    if not file_path:
        return False
    
    # (next sprint) find prerequisites
    # (next sprint) communicate prerequisites to client
    # (next sprint) client sends list of which prerequisites are already met, to be removed from transfer list
    # (next sprint) for each of the *missing* prerequisites:
        # open the file and send its contents
            # verification already included
        # if fail return false

    send_successful = send_file(client, package_name, file_path)
    if not send_successful:
        return False
    return True