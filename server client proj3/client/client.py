#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol


# IP = ????
SAVED_PHOTO_LOCATION = "C:\screenshot\screenshot\screen.jpg"

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    if cmd == "SEND_PHOTO":
        value,msg = protocol.get_msg(my_socket)
        while msg > 0:
            image = my_socket.recv(9999)
            image.save(SAVED_PHOTO_LOCATION)
            msg = msg - 9999
    else:    
      value,msg = protocol.get_msg(my_socket)
      if value == True:
        print("server response:\n" + msg)
    
    # (8) treat all responses except SEND_PHOTO

    # (10) treat SEND_PHOTO


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))
    # (2)
     
    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()