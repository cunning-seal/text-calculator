import sys
import socketserver
from server_logic import Parser


class TextCalculatorServerHandler(socketserver.BaseRequestHandler):
    def handle(self):

        p = Parser()

        close = False
        while not close:
            data = self.request.recv(1024).decode()
            print("GOT", data)
            if "finish" in data:
                close = True
                print("Connection finished")
                continue
            resp = p.process(data)
            print(resp)
            try:
                self.request.sendall(resp.encode())
            except BrokenPipeError:
                continue
            except ConnectionResetError:
                continue


if __name__ == '__main__':

    args = sys.argv[1:]

    port = int(args[0]) if len(args) != 0 and args[0].isdigit() else 8001

    addr = ("localhost", port)

    with socketserver.TCPServer(addr, TextCalculatorServerHandler) as server:
        print("Server started work on {x[0]}:{x[1]}".format(x=server.server_address))
        try:
            server.serve_forever()
        except:
            print("\nServer Stopped")
            server.shutdown()
            server.server_close()
