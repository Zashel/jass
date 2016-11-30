from zashel.virtualgpio import VirtualGPIOBaseHandler

class Handler(VirtualGPIOBaseHandler):
    def __init__(self, app):
        self._app = app

    def emit(self, signal):
        self._app.vgpio.send_all(signal)