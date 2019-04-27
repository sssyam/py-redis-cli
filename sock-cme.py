import socket
import readline

host='test-cme-tls.0koy65.clustercfg.euw1.cache.amazonaws.com'
port=6379

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect((host,port))
exit = False
while(not exit):
    command = input("$ ")
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
            soc.send(command.encode())
            data = soc.recv(1024).decode()
        print(data)

soc.close()
