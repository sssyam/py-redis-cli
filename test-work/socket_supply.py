import socket
import ssl

def get_socket(option):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ## connection.settimeout(5)
        if option['tls'] == True:
            connection = ssl.wrap_socket(connection)
        
        connection.connect((option['host'], option['port']))
        print("Connection Successful")
        return connection

    except Exception:
        print("Connection Failed! Check hostname, port and if you have connectivity to that host and port! Also check health of node !")
        connection.close()
        return None

if __name__ == "__main__":
    option = {}
    option['host'] = "www.google.com"
    option['port'] = 23452
    option['tls'] = True
    conn = get_socket(option)
    print(conn)