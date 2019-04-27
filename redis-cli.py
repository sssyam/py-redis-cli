import sys
from sock_cmd import cmd
from sock_cmd_tls import cmd_tls
from sock_cme import cme
from sock_cme_tls import cme_tls

def help():
    s = """
    HELP
        -h <hostname>       Host Name
        -p <port>           Port
        -t                  Enable TLS
        -c                  Cluster Mode Enabled
    """
    print(s)

if __name__ == "__main__":

    host = 'localhost'
    port = 6379
    tls = False
    cluster = False

    args = sys.argv[1:]
    l = len(args)
    i = 0
    while ( i < l ):
        try:
            if args[i] == '-h':
                host = args[i+1]
                i = i + 2
            elif args[i] == '-p':
                port = args[i+1]
                i = i + 2
            elif args[i] == '-t':
                tls = True
                i = i + 1
            elif args[i] == '-c':
                cluster = True
                i = i + 1
            else:
                raise Exception('Invalid Option')
        except Exception as e:
            print(e)
            help()
            exit(1)

    if tls and cluster:
        cme_tls(host, port)
    elif not tls and cluster:
        cme(host, port)
    elif tls and not cluster:
        cmd_tls(host, port)
    else:
        cmd(host, port)
