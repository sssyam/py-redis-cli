import sys
from parameter_test import eval_options
from socket_supply import get_socket
from command_handler import command_line

if __name__ == "__main__":
    args = sys.argv[1:]
    option = eval_options(args)
    
    if option['status'] == False:
        exit(1)

    socket = get_socket(option)

    if socket == None:
        exit(1)
    
    command_line(option, socket)