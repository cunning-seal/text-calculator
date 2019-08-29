from app import ClientApp
import sys

if __name__ == '__main__':
    run_args = sys.argv[1:]

    port = 8000
    server_ip = 'localhost:8001'
    valid_args = True
    try:
        port_index = run_args.index('-p')
        try:
            port_arg = run_args[port_index + 1]
            if port_arg.isdigit():
                port = int(port_arg)
            else:
                print("Invalid arguments definition: -p")
                valid_args = False
        except IndexError:
            print("Invalid arguments definition: -p")
            valid_args = False
    except ValueError:
        pass

    try:
        server_ip_index = run_args.index('-a')
        try:
            server_ip = run_args[server_ip_index + 1]
        except IndexError:
            print("Invalid arguments definition: -a")
            valid_args = False
    except ValueError:
        pass

    if valid_args:
        c = ClientApp(port, server_ip)
        c.run()
