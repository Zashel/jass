from .data import Data
from .config import Config
from .handler import Handler
from .signals import HandlerRegister
from zashel.virtualgpio import VirtualGPIO
from zashel.websocket import WebSocket
import subprocess


class App():
    def __init__(self):
        self._config = Config()
        self._handler = Handler(self)
        self._data = Data(self._config)
        HandlerRegister.register_handler(self._handler)
        self._vgpio = VirtualGPIO(self._config["VirtualGPIO"]["remote"], handler=self._handler)
        self._websocket = WebSocket(
                (self._config["WebSocket"]["dir"], self._config["WebSocket"]["port"]),
                self._handler
                )
        self._file_lock = list()
        self._lock = dict()
        self._lock[self.config["JAss"]["data"]["complaints"]["file"]] = list()
        self._lock[self.config["JAss"]["data"]["commitments"]["file"]] = list()

    def run(self):
        self._vgpio.run()
        self._websocket.listen()

    @property
    def vgpio(self):
        return self._vgpio

    @property
    def handler(self):
        return self._handler

    @property
    def config(self):
        return self._config

    @property
    def websocket(self):
        return self._websocket

    @property
    def data(self):
        return self._data

def execute():
    app = App()
    app.run()
    subprocess.Popen([r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                      "--app=http://{}:{}/".format(
                          app.config["WebSocket"]["dir"],
                          app.config["WebSocket"]["port"])])

if __name__ == "__main__":
    execute()