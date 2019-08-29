import socket


class ClientAppNetwork:
    """
    Класс сетевого модуля клиентского приложения
    """
    def __init__(self, port, server_ip):
        addr = server_ip.split(":")
        self.server_addr = addr[0], int(addr[1])
        self.host = "localhost"
        self.port = port
        self.socket = None
        self.conn = None

    def install(self):
        """
        Старт работы сетевого модуля
        :return: статус работы сервера. False при ошибке соединения или создания сокета
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(2)
        except socket.error:
            print("Failed to create socket for client application")
            return False

        try:
            self.conn = self.socket.connect(self.server_addr)
        except socket.error:
            print("Failed to connect to the server")
            self.socket.close()
            self.socket = None
            return False
        print("INSTALLED")
        return True

    def send_to_server(self, data: str) -> str or None:
        """
        Отправка выражения на сервер
        :param data: выражение
        :type data: str
        :return: ответ сервера
        :rtype: str or None
        """
        if self.socket:
            try:
                self.socket.send(data.encode())
                print("SENT", data)
            except socket.timeout:
                return "Failed to send data to the server. Please check the server availability"
            try:
                response = self.socket.recv(1024)
                print("RECEIVED", response.decode())
                return response.decode()
            except socket.timeout:
                print("Server timeout limit reached")

        else:
            return None

    def __del__(self):
        self.send_to_server('finish')
        if self.conn is not None:
            self.conn.close()
        if self.socket is not None:
            self.socket.close()
            print("CLOSED")