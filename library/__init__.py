from .data import *
from .config import Config
from .handler import Handler
from .signals import HandlerRegister
from zashel.virtualgpio import VirtualGPIO
from .websocket import *


class App():
    def __init__(self):
        self._config = Config()
        self._handler = Handler(self)
        HandlerRegister.register_handler(self._handler)
        self._vgpio = VirtualGPIO(self._config["VirtualGPIO"]["remote"], handler=self._handler)

    def run(self):
        self._vgpio.run()

    @property
    def vgpio(self):
        return self._vgpio

    @property
    def handler(self):
        return self._handler

    @property
    def config(self):
        return self._config

if __name__ == "__main__":
    app = App()
    app.run()