import socket, config, os, shutil, re
from zipfile import ZipFile

#####

def prompt_for_package_code():
    # prompt user for package code
    package_code = input("Package code (e.g. 'm00000001'): ")

    # regex pattern of how package_codes are supposed to be formatted
    #   note that the package_code is an ASCII character prefixing a hexadecimal number
    code_pattern = "^[mde][0-9A-Fa-f]{8}$"

    # compare package_code to code_pattern and make sure it matches
    if re.search(code_pattern, package_code) == None:
        # return false if invalid 
        return False
    else:
        # else return the validly-formatted package_code
        #   (may not be a truly valid package_code if no package on the server has that code)
        return package_code

def parse_package_code_for_destination(package_code):

    # start building a relative address to the destination of the package
    package_destination = "rpo_client/"

    # content folder is based on the first-character flag of the package_code
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

def request_and_download_package(package_destination, package_code, server):
    """
    KNOWN BUG:  if client and server are on different machines, client not likely to receive
                full package it is trying to download, causing the received file to be many times
                shorter than the original, and causing the server script to crash due to lost
                connection during transfer.
    """

    # assemble the path to the zip file that will be created and received from the server
    zip_path = f"{package_destination}{package_code}.zip"

    # create the message to be sent to the server to request the package
    message = f"download,{package_code}"

    # open the zip file as 'write binary'
    with open(zip_path, 'wb') as zip_file:
        # request the file
        server.send(bytes(message, config.MESSAGE_ENCODING))

        # TODO: add "file exists" verification step to both client and server

        # little output-only iteratort just used to track how many packets have been sent during the download
        i = 0
        while True:
            # receive the file contents the server is sending
            response = server.recv(1024)

            # output debug info to screen
            i += 1
            print(f"Receiving block {i} of file {package_code}")

            # write the contents into the zip file
            zip_file.write(response)

            # AFTER the current chunk has already been written to the file, check its length.
            #   If it is less than 1024 bytes, we assume the file is empty and we break the  loop
            if len(response) < 1024:
                break
        print("Done receiving.")
        return True

def unzip_downloaded_package(package_destination, package_code):
    # assemble the relative path to the unzipped folder
    unzipped_folder_name = f"{package_destination}{package_code}"

    # assemble the relative path to the zip file
    zip_path = f"{unzipped_folder_name}.zip"
    
    # open the zip file
    with ZipFile(zip_path, 'r') as zipped_package:
        # if the unzipped folder already exists, delete it
        #   (because I couldn't find info on the default overwriting behavior of ZipFile.extractall)
        if os.path.exists(unzipped_folder_name):
            shutil.rmtree(unzipped_folder_name)

        # extract the zipped package into its destination
        #   have to manually define a destination because default path is to the Current Working Directory,
        #   which would be a bad place to put the files
        zipped_package.extractall(package_destination)

    # get rid of the zipped package now that it is extracted and we aren't holding it open anymore
    os.remove(zip_path)
    
def download_package():
    # fetch server's IP and PORT from the config file
    ip = config.SERVER_IP
    port = config.SERVER_PORT
    # assemble it into tuple for later use
    server_block = (ip, port)

    # create socket object for all interactions with server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect socket to server
    #   TODO: wrap this in a try-catch in case the connection fails
    server.connect(server_block)

    # prompt user for package code. If code was invalid, cancel download op
    package_code = prompt_for_package_code()
    if package_code == False:
        return False
    
    # parse the package code here to help with later file pathing.
    #   the if-statement *shouldn't* ever pass to the early-return, but Murphy's Law
    package_destination = parse_package_code_for_destination(package_code)
    if package_destination == False:
        return False

    # request and download the file. No real verification steps
    succeeded = request_and_download_package(package_destination, package_code, server)
    if succeeded != True:
        return False
    
    # unzip the package into its destination
    unzip_downloaded_package(package_destination, package_code)

# run the test
download_package()