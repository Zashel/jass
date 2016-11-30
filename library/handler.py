from zashel.virtualgpio import VirtualGPIOBaseHandler

class Handler(VirtualGPIOBaseHandler):
    def __init__(self, app):
        self._app = app