import socket, config, os, shutil, re
from zipfile import ZipFile
from services.debug_tools import DebugTools

def len_of_num(i):
    # get digit-count of a number, by getting its the string-length of its absolute value form
    return len(str(abs(i)))

def byte_me(data):
    # convert provided data into bytes, unless it is already bytes.
    #   Function name is also a rough estimation of how I reacted anytime the
    #   solution to an error was type conversion between strings, ints, and bytes
    if isinstance(data, bytes):
        return data
    else:
        return bytes(data, config.MESSAGE_ENCODING)

def throw_client_error(error_message: str, target = None):
    # safely print out error messages as well as attempting to
    #   forward those messages to the other end of the connection,
    #   if a target is provided and sending the message is possible
    print(error_message)
    if target:
        try:
            target.send(byte_me(error_message))
        except Exception as e:
            # if a target was provided but sending the message was not possible,
            #   inform user the communication was unsuccessful and why
            print(f"FURTHER: Could not forward error message to server!\n{e}")
            return False
        
def write_zip_file(package_destination, package_code, packet_dict):
    # pump the packet_dict into a zip file

    # define the full file_path
    zip_path = f"{package_destination}{package_code}.zip"
    # try-except block just in case it fails
    try:
        # open the zip as write-binary
        with open(zip_path, 'wb') as zip_file:
            # loop through the packet_dict
            for i in range(len(packet_dict)):
                # write a packet from the dict into the file
                zip_file.write(packet_dict[i])
        return True
    except Exception as e:
        # in case of emergency, dump an error message
        throw_client_error(e)
        return False

def send_packet(target, packet):
    # loop to make sure the packet gets sent and resent until the full-length
    #   version of the packet is received by the client
    while True:
        # try repeatedly, but catch the possibility of a closed connection
        try:
            # count the number of bytes successfully sent
            sent_bytes_count = target.send(packet)
            # if it matches the length of the packet, we succeeded and can leave
            if sent_bytes_count == len(packet):
                return True
        except Exception as e:
            # handle the possibility of a hard-failed send and/or closed connection
            throw_client_error(e)
            return False

def request_and_download_package(package_destination, package_code, server):
    try:
        # create and send download request
        message = f"download:{package_code}"
        server.send(byte_me(message))

        # await server's confirmation that the file exists
        verification_response = server.recv(1024)
        verification_response = verification_response.decode(config.MESSAGE_ENCODING)
        verification_response = verification_response.split(':')

        # parse response to make sure file *does* exist
        if verification_response[0] != f"{package_code}":
            raise Exception(verification_response)
        expected_packet_count = int(verification_response[1])

        # prepare space to store relevant packets
        packet_dict = {}

        # inform server we're ready to receive data
        send_packet(server, b'ready')

        # loop until we receive the "done" packet, 
        while True:
            # receive the packet
            packet = server.recv(1024)
            # if it is the "done" packet we break the loop and move on to writing the zip file
            if packet == b'done':
                break
            # parse the packet for the packet_num and the actual raw data that goes into the zip file
            packet_num, chunk = packet.split(b':',1)
            # convert the packet_num into usable int format
            packet_num = int(packet_num)
            # all packets other than the last one should be max-length
            if len(packet) == 1024 or packet_num == expected_packet_count - 1:
                # use the packet_num as te key and make the chunk its value
                packet_dict[packet_num] = chunk
                # print out data so users don't panic during long downloads
                print(f"received {packet_num}")
                # send the "This packet had an acceptable length" reply
                reply = byte_me(f"{packet_num}:+")
                send_packet(server, reply)
            else:
                # sendt he "this packet didn't have an acceptable length" reply
                reply = byte_me(f"{packet_num}:-")
                send_packet(server, reply)
        
        print("Done receiving")
        # write the zip file and check to see if it succeeded to determine the T/F return value
        success = write_zip_file(package_destination, package_code, packet_dict)
        if not success:
            return False
        print("Done saving")
        return True
    except Exception as e:
        throw_client_error(f"abort:{e}", server)
        return False


def parse_package_code_for_destination(package_code):
    # start building a relative addres to the destination of the package
    package_destination = "rpo_client/content/"

    # content folder is based on the first-charcter flag of th epackage_code
    match package_code[0]:
        case 'm':
            package_destination += 'modules/'
        case 'e':
            package_destination += 'system_expansions/'
        case 's':
            package_destination += 'systems/'
        case default:
            return False
        
    return package_destination

def prompt_for_package_stats():
    # variables to store package_code and package_destination in
    package_code = ""
    package_destination = ""
    # nested while loops to ensure that only (syntactically) valid
    #   package_codes/package_destinations will be returned
    while True:
        # inner loop handles actually prompting the user, as well as initial
        #   regex validation of the entered package_code
        while True:
            # prompt user for package code
            package_code = input("Package code to download (e.g. 'm00000001') or enter 'x' to cancel download: ")
            # make it lowercase to ensure capitalization for prefix or hex letters is properly optional
            package_code = package_code.lower()
            # allow user to exit the entire prompt and cancel the download request from here
            if package_code == 'x':
                return False, False

            # regex pattern of how package_codes are supposed to be formatted.
            #   note that the package_code is an ASCII character prefixing 8 hexadecimal characters
            code_pattern = "^[mse][0-9a-f]{8}$"

            # compare package_code to code_pattern and make sure it matches
            if re.search(code_pattern, package_code):
                break

        # parse out a package_destination, and if the package_code passes both
        #   the package_code and package_destination verification steps,
        #   we return both parts to be used in the download request
        package_destination = parse_package_code_for_destination(package_code)
        if package_destination: # is not False
            return package_code, package_destination

def unzip_downloaded_package(package_destination, package_code):
    # assemble the relative path to the unzipped folder
    unzipped_folder_name = f"{package_destination}{package_code}"

    # assemble the relative path to the zip file
    zip_path = f"{unzipped_folder_name}.zip"

    # open the zip file
    succeeded = None
    try:
        with ZipFile(zip_path, 'r') as zipped_package:
            # if the unzipped folder already exists, delete it
            #   (because I couldn't find info on the defalt overwriting behavior of ZipFile.extractall())
            if os.path.exists(unzipped_folder_name):
                shutil.rmtree(unzipped_folder_name)

            # extract the zipped package into its destination
            #   have to manually define a destination because default path is to the Current Working Directory
            #   which would be a bad place to put the files
            zipped_package.extractall(package_destination)
            succeeded = True
    except:
        succeeded = False

    # get rid of the zipped package now that it is extracted and we aren't holding it open anymore
    os.remove(zip_path)
    return succeeded

def download_package():
    # fetch server's IP and PORT from the config file
    ip = config.SERVER_IP
    port = config.SERVER_PORT
    # assemble it into tuple for convenient later use
    server_block = (ip, port)

    # create socket object for all interactions with server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # prompt user for package code, and parse a package_destination out of it as well
    #   if user enters 'x', cancel the download request and early-return
    package_code, package_destination = prompt_for_package_stats()
    if package_code == False or package_destination == False:
        print("Cancelling download request")
        return False
    
    # in future updates, this will be wrapped a set of nested loops that will
    #   download the package and all of its prerequisites, but for now we're
    #   only downloading one file
    while True:
        # connect socket to server. Doing it here is easier than having the
        #   server wait for the client to send a success message
        try:
            server.connect(server_block)
        # if connection fails, provide reason and exit
        except Exception as e:
            print("######################################################\n"
                "# Server Connection Failed for the following reasons #\n"
                "######################################################\n"
                f"{e}")
            return False

        # request and download the file. Verification steps included inside function
        succeeded = request_and_download_package(package_destination, package_code, server)
        # not yet sure how to handle a failed download situation, especially
        #   because the download may have failed due to a lost connection that
        #   I do not yet know how to check for or correct
        if not succeeded:
            return False
        
        # unzip the package into its destination. if package unzips correctly,
        #   download was successful, so we can leave
        succeeded = unzip_downloaded_package(package_destination, package_code)
        if succeeded:
            return True

download_package()
