import socket
import readline


def cmd(host, port):

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host,port))
    exit = False
    while(not exit):
        command = input(soc.getpeername()[0] + " $ ")
        command = command + " \n"
        if 'exit' == command.strip():
            break
        elif 'monitor' == command.strip():
            try:
                soc.send(command.encode())
                while(True):
                    data = soc.recv(1024).decode().strip()
                    print(data)
            except KeyboardInterrupt:
                print("")
                continue
        else:
            soc.send(command.encode())
            data = soc.recv(1024).decode()
            print(data)

    soc.close()

if __name__ == "__main__":
    host='test-cmd.0koy65.ng.0001.euw1.cache.amazonaws.com'
    port=6379
    cmd(host,port)
