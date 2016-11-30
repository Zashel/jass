from .data import *
from .config import Config
from .handler import Handler
from zashel.virtualgpio import VirtualGPIO
from .websocket import *

class App():
    def __init__(self):
        self._config = Config()
        self._handler = Handler(self)
        self._vgpio = VirtualGPIO(self._config["VirtualGPIO"]["remote"], handler=self._handler)

    def run(self):
        self._vgpio.run()

    @property
    def vgpio(self):
        return self._vgpio

    @property
    def handler(self):
        return self._vgpio

    @property
    def config(self):
        return self._config
