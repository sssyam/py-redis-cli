import socket
import ssl

def get_socket(option, authToken=''):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ## connection.settimeout(5)
        if option['tls'] == True:
            connection = ssl.wrap_socket(connection)
        
        connection.connect((option['host'], option['port']))
        print("Connection Successful")
        if option['tls']:
            connection.send("PING \n".encode())
            data = connection.recv(1024).decode()
            if "-NOAUTH" in data:
                while True:
                    if authToken == '':
                        authToken = input ("AUTH: ")
                    testCommand = ("AUTH " + authToken + " \n")
                    connection.send(testCommand.encode())
                    data = connection.recv(1024).decode()
                    if "-ERR" in data:
                        print("Invalid AUTH token, Try Again !!")
                        authToken = ''
                    elif "+OK" in data:
                        break
                    else:
                        raise Exception("UnknownReply: " + data + " for AUTH ")
            elif "PONG" not in data:
                raise Exception("UnknownReply: " + data + " for PING ")
                        
        return connection, authToken
    except Exception as e:
        print (e)
        print("Connection Failed! Check hostname, port and if you have connectivity to that host and port! Also check health of node !")
        connection.close()
        return None, authToken

if __name__ == "__main__":
    option = {}
    option['host'] = "www.google.com"
    option['port'] = 23452
    option['tls'] = True
    conn = get_socket(option)
    print(conn)
