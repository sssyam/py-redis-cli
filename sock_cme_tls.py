import socket
import readline
import ssl



def cme_tls(host, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc = ssl.wrap_socket(soc)
    soc.connect((host,port))

    soc.send("ping \n".encode())
    auth = soc.recv(1024).decode()
    auth = auth.split(' ')[0]
    auth_needed = False
    auth_token = ''

    if auth == '-NOAUTH' :
        auth_needed = True
        auth_correct = False
        while( not auth_correct ):
            auth_token = input("AUTH: ")
            cmd = 'AUTH ' + auth_token + " \n"
            soc.send(cmd.encode())
            check = soc.recv(1024).decode()
            print(check)
            if  "+OK" in check:
                auth_correct = True

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
            if data[:6] == "-MOVED":
                soc.close()
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.connect((data.split(' ')[2].split(':')[0],port))
                soc = ssl.wrap_socket(soc)
                if auth_needed:
                    cmd = 'AUTH ' + auth_token + " \n"
                    soc.send(cmd.encode())
                    check = soc.recv(1024).decode()
                soc.send(command.encode())
                data = soc.recv(1024).decode()
            print(data)

    soc.close()

if __name__ == "__main__":
    host='clustercfg.test-cme-tls-auth.0koy65.euw1.cache.amazonaws.com'
    port=6379
    cmd_tls(host, port)
