#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol
import glob
import os
import shutil
import subprocess
import pyautogui


# IP = ????
PHOTO_PATH = "C:\screenshot\screen.jpg"


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first

    # Then make sure the params are valid

    # (6)
    value,msg = protocol.check_cmd(cmd)
    if value:
        if msg == "DIR":
          files_list = glob.glob(cmd[4:])
          if files_list:
             return True, "DIR", cmd[4:]
        elif msg == "DELETE":
            files_list = glob.glob(cmd[7:])
            if files_list:     
              return True, "DELETE",cmd[7:] 
        elif msg == "COPY":
            start_slice = cmd.find('C:\\')+2
            end_slice = cmd.find('C:\\',start_slice)
            slice1 = cmd[:end_slice]
            slice2 = cmd[end_slice:]
            files_list1 = glob.glob(slice1[5:])
            files_list2 = glob.glob(slice2)
            print(files_list1)
            print(files_list2)
            if files_list1 and files_list2:
                return True, "COPY", cmd[5:]   
        elif msg == "EXECUTE":
          files_list = glob.glob(cmd[8:])
          if files_list:
                return True,"EXECUTE",cmd[8:]
        elif msg == "TAKE_SCREENSHOT":
            files_list = glob.glob(PHOTO_PATH[:14])
            if files_list:
                return True,"TAKE_SCREENSHOT",PHOTO_PATH
        elif msg == "SEND_PHOTO":
            return True,"SEND_PHOTO",PHOTO_PATH
    return False, "ERROR", cmd 


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    if command == "DIR":
        response = str(glob.glob(params))
    elif command == "DELETE":
        os.remove(params)
        response = "file deleted!"
    elif command == "COPY":
        start_slice = params.find('C:\\')+2
        end_slice = params.find('C:\\',start_slice)
        slice1 = params[:end_slice]
        slice2 = params[end_slice:]
        shutil.copy(slice1,slice2)
        response = "file copied!!!"
    elif command == "EXECUTE":
        subprocess.call(params)
        response = "app running succssesful!!!!"
    elif command == "TAKE_SCREENSHOT":
        image = pyautogui.screenshot()
        image.save(params)
        response = "screenshot succsess!!"
    elif command == "SEND_PHOTO":
        size = os.path.getsize(PHOTO_PATH)
        length = protocol.create_msg(str(size))
        response = length
    # (7)

    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0",protocol.PORT))
    server_socket.listen()
    print("server is up")
    (client_socket,client_address) = server_socket.accept()
    print("client connected :)")
    # (1)
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(command,params)

                # add length field using "create_msg"
                if command == "SEND_PHOTO":
                    size = os.path.getsize(PHOTO_PATH) 
                    client_socket.send(response)
                    image = open(PHOTO_PATH)
                    bytes = image.read()
                    while(size > 0):
                      client_socket.send(bytes)
                      size - 9999
                else:    
                  response = protocol.create_msg(response)
                  # send to client
                  client_socket.send(response)
                    # if command == 'SEND_FILE':
                    #     # Send the data itself to the client

                        # (9)
                
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response)

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            response = protocol.create_msg(response)
            #send to client
            client_socket.send(response)


            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
