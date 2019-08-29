import sys
import socketserver
from server_logic import Parser


class TextCalculatorServerHandler(socketserver.BaseRequestHandler):
    """
    Класс-обработчик запроса на сервере
    """
    def handle(self):
        p = Parser()

        close = False
        while not close:
            data = self.request.recv(1024).decode()
            print("GOT", data)
            # прислали finish - заканчиваем цикл обработки соединения
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
    port = 8001
    valid_args = True

    # определение порта запуска сервера
    try:
        port_index = args.index('-p')
        try:
            port_arg = args[port_index + 1]
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

    addr = ("localhost", port)

    # создаем TCP сервер для получения
    if valid_args:
        with socketserver.TCPServer(addr, TextCalculatorServerHandler) as server:
            print("Server started work on {x[0]}:{x[1]}".format(x=server.server_address))
            try:
                server.serve_forever()
            except:
                print("\nServer Stopped")
                server.shutdown()
                server.server_close()
