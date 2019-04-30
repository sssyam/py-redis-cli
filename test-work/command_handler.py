# import readline
from socket_supply import get_socket
import select

def get_output(socket):
    ### socket.send("\n".encode())
    ## socket.setblocking(False)
    data = ''
    try:
        while True:
            data = data + socket.recv(1024).decode()
            raise Exception
    except Exception as e:
        print(e)
    
    ## socket.setblocking(True)
    return data


def listening_mode(socket):
    ## socket.setblocking(True)
    socket.settimeout(None)
    try:
        while True:
            data = socket.recv(1024).decode()
            print(data)
    except KeyboardInterrupt:
        pass
    
    socket.settimeout(5)


def command_line(option, socket):
    moved = False
    command = ''
    while True:
        if not moved:
            command = input (socket.getpeername()[0] + ":" + str(option['port']) + " $ ")
            if "exit" == command:
                exit(0)
            command = command + " \n"

        moved = False
        socket.send(command.encode())

        if "monitor" in command.strip() or "subscribe" in command.split(' ')[0].strip():
            listening_mode(socket)
            continue
        # get data from the socket
        data = get_output(socket)
        
        if data[:6] == "-MOVED" and option['cluster']:
            ip_and_port = data.split(' ')[2]
            ip, port = ip_and_port.split(' ')
            option['host'] = ip
            option['port'] = port
            socket = get_socket(option)
            if socket == None:
                exit(1)
            moved = True
            continue

        print(data)
        print("===============================\n\n")


