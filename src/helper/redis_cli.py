from helper.parameter_test import eval_options
from helper.socket_supply import get_socket
from helper.command_handler import command_line

def init(arguments):
    args = arguments[1:]
    option = eval_options(args)
    
    if option['status'] == False:
        exit(1)

    try:
        socket, authToken = get_socket(option)

        if socket == None:
            exit(1)

        command_line(option, socket, authToken)
    except KeyboardInterrupt:
        print("Exiting ...... ")
