from gui import ClientAppGUI
from network import ClientAppNetwork


class ClientApp:
    """
    Класс клиентского приложения, состоящего из GUI и модуля сетевого взаимодействия
    """
    def __init__(self, port, server_ip):
        print("Initialising client application on port {} and with server IP {}".format(port, server_ip))
        self.network = ClientAppNetwork(port, server_ip)
        self.GUI = ClientAppGUI(self.network)

    def run(self):
        """
        Запуск приложения
        :return: None
        """
        if self.network.install():
            self.GUI.install()

    def __del__(self):
        del self.network
        del self.GUI
