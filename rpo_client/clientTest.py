import socket, config, os, shutil, re, asyncio
from zipfile import ZipFile

#####

def prompt_for_package_code():
    package_code = input("Package code: ")

    code_pattern = "^[mde][0-9]{8}$"
    if re.search(code_pattern, package_code) == None:
        return False
    else:
        return package_code

def parse_package_code_for_destination(package_code):
    package_destination = "rpo_client/"
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

def request_and_handle_download(package_destination, package_code, server):
    zip_path = f"{package_destination}{package_code}.zip"
    message = f"download,{package_code}"

    with open(zip_path, 'wb') as zip_file:
        server.send(bytes(message, config.MESSAGE_ENCODING))
        i = 0
        while True:
            print(f"Receiving block {i} of file {package_code}")
            i += 1
            response = server.recv(1024)
            zip_file.write(response)
            if len(response) < 1024:
                break
        print("Done receiving.")
        return zip_path

def unzip_downloaded_package(package_destination, package_code):
    unzipped_folder_name = f"{package_destination}{package_code}"
    zip_path = f"{unzipped_folder_name}.zip"
    
    with ZipFile(zip_path, 'r') as zipped_package:
        if os.path.exists(unzipped_folder_name):
            shutil.rmtree(unzipped_folder_name)
        zipped_package.extractall(package_destination)

    os.remove(zip_path)
    
def download_package():
    ip = config.SERVER_IP
    port = config.SERVER_PORT
    server_block = (ip, port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.connect(server_block)

    package_code = prompt_for_package_code()
    if package_code == False:
        return False
    
    package_destination = parse_package_code_for_destination(package_code)
    if package_destination == False:
        return False

    succeeded = request_and_handle_download(package_destination, package_code, server)
    if succeeded == False:
        return False
    
    unzip_downloaded_package(package_destination, package_code)

download_package()