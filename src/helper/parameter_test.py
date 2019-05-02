import sys

def help():
    help_string="""
        Command HELP:
        py-redis-cli [OPTIONS]

        OPTIONS:
            -h <hostname>
            --host <hostname>       Specify the endpoint to connect to
            --host=<hostname>

            -p <port>
            --port <port>           Specify the port to connect to
            --port=<port>

            -t
            --tls                   Specify to connect over SSL/TLS

            -c
            --cluster               Specify to use cluster mode

            --help                  Print this help

    """
    print(help_string)

def is_option(value):
    if value in ["-h", "-p", "-t" , "-c", "--host", "--port", "--tls", "--cluster"] :
        return True
    elif "--host=" in value or "--port=" in value:
        return True
    else:
        return False

def eval_options(args):

    # Argument Store Body and Init

    i = 0
    l = len(args)

    ### print("Paramter Passed: " + str(args))

    option = {}
    option['host'] = ''
    option['port'] = ''
    option['tls'] = False
    option['cluster'] = False
    option['status'] = False

    # Argument Parsing

    try:
        while( i < l ):

            ### print( "Before Loop " + str(i) + " < " + str(l))
            ### print( "Argument Targeted: " + args[i])

            if args[i] == '-h' or args[i] == "--host": 
                if i+1 >= l:
                    raise Exception("Error: Hostname not given!")
                if is_option(args[i+1]):
                    raise Exception("Error: Invalid Hostname: " + args[i+1] + " ! Please try again !!")
                option['host'] = args[i+1]
                # print("Got Host")
                i = i + 2
            elif args[i] == '-p' or args[i] == "--port": 
                if i+1 >= l:
                    raise Exception("Error: Port not given!")
                option['port'] = int(args[i+1])
                if option['port'] < 1 or option['port'] > 65535:
                    raise Exception("Error: Port Should be in range [1,65535]")
                # print("Got Port")
                i = i + 2
            elif args[i] == '-t' or args[i] == '--tls':
                # print("Got TLS")
                option['tls'] = True
                i = i + 1
            elif args[i] == '-c' or args[i] == '--cluster':
                option['cluster'] = True
                # print("Got Cluster")
                i = i + 1
            elif "--host=" in args[i]:
                parse =  args[i].split("=")
                hostname = parse[1].strip()
                if is_option(hostname):
                    raise Exception("Invalid Hostname: " + hostname + " ! Please try again !!")
                option['host'] = hostname
                # print("Got Host")
                i = i + 1
            elif "--port=" in args[i]:
                option['port'] = int(args[i].split("=")[1].strip())
                # print("Got Port")
                i = i + 1
            elif "--help" == args[i]:
                raise Exception("")

            else:
                raise Exception("Invalid option " + args[i])

            # print( "After Loop: " + str(i) + " < " + str(l))
    
    except ValueError:
        print("Error: Invalid Port. The Port should be Integer in range of [1,65535] ! Please try again !")
        help()
        return option

    except Exception as e:
        print(e)
        help()
        return option

    # Compulsory Argument Check for 

    if option['host'] == '':
        print("No Hostname Specified. Using localhost.")
        option['host'] = 'localhost'

    if option['port'] == '':
        print("No Port Specified. Using default port for redis '6379'.")
        option['port'] = 6379

    # Return Successful

    option['status']=True
    return option


if __name__ == "__main__":
    args = sys.argv[1:]
    print( eval_options( args ) )