import readline
from helper.socket_supply import get_socket
import select
import traceback

def get_output(socket):
    # socket.send("\n".encode())
    socket.setblocking(0)
    #read, _, _ = select.select( [socket],  [], [] )
    
    data = ''
    olddata = ''
    #socket.recv(data)
    #print(data)
    #if len(read) > 0:
    #    data = data + socket.recv(1024).decode()
    #

    #socket.settimeout(1)
    while data == '' or olddata != data:
        try:
            #while True:
            olddata = data
            value =  socket.recv(1024).decode()
            print( "Value received:" + value )
            data = data + value
        except Exception as e:
            pass
        # traceback.print_exc()
        # print(e)
    
    
    socket.settimeout(5)
    socket.setblocking(1)
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


def command_line(option, socket, authToken):
    moved = False
    command = ''

    while True:
        if not moved:
            command = input (socket.getpeername()[0] + ":" + str(option['port']) + " $ ")
            if "exit" == command:
                exit(0)
            if command == '':
                continue
            command = command + " \n"

        moved = False
        socket.send(command.encode())

        if "monitor" in command.strip() or "subscribe" in command.split(' ')[0].strip():
            listening_mode(socket)
            continue

        # get data from the socket
        data = get_output(socket).strip()
        
        if data[:6] == "-MOVED" and option['cluster']:
            ip_and_port = data.split(' ')[2]
            ip, port = ip_and_port.split(':')
            option['host'] = ip
            option['port'] = int(port)
            socket, authToken = get_socket(option, authToken)
            if socket == None:
                exit(1)
            moved = True
            continue

        print(data)
        print("===============================\n\n")


