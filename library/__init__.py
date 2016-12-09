from .data import Data, initiate_data
from .config import Config
from .handler import Handler
from .signals import HandlerRegister
from zashel.utils import search_win_drive
from zashel.virtualgpio import VirtualGPIO
from zashel.websocket import WebSocket, PingSignal
import subprocess
import time
import os

TIMEOUT = 10

class App():
    def __init__(self):
        self._config = Config()
        self.executing = True
        self._handler = Handler(self)
        self._data = Data(self._config)
        HandlerRegister.register_handler(self._handler)
        self._vgpio = VirtualGPIO(search_win_drive(self._config["VirtualGPIO"]["remote"]), handler=self._handler)
        self._websocket = None
        self._websocket = WebSocket(
                (self._config["WebSocket"]["dir"], self._config["WebSocket"]["port"]),
                self._handler
                )
        self._file_lock = list()
        self._lock = dict()
        self._lock[self.config["complaints"]["file"]] = list()
        self._lock[self.config["commitments"]["file"]] = list()

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
    try:
        app = App()
        app.run()
        subprocess.run([r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                          "--app=file:///{}".format(
                              app.config["WebSocket"]["html"])])
        time.sleep(10)
        while app.executing is True:
            app.executing = False
            print("Ping")
            app.websocket.send_all(PingSignal())
            time.sleep(TIMEOUT)
    finally:
        app.vgpio.disconnect()


if __name__ == "__main__":
    execute()