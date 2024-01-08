#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    if data[:7] == "DIR C:\\":
        return True
    elif data[:10] == "DELETE C:\\":
        return True
    elif data[:8] == "COPY C:\\":
        return True
    elif data[:7] == "EXECUTE":
        return True
    elif data[:15] == "TAKE_SCREENSHOT":
        return True
    elif data[:10] == "SEND_PHOTO":
        return True
        
    # (3)
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    data = zfill_length + data
    """
    user_length = str(len(data))
    zfill_length = user_length.zfill(LENGTH_FIELD_SIZE)
    data = zfill_length + data
    # (4)
    return data.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    check = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if int(check) <= 9999 and int(check) >=0:
    # (5)
       return True, my_socket.recv(int(check)).decode()
    return False, "Error"


# EXECUTE C:\Program Files\TeamViewer\TeamViewer.exe