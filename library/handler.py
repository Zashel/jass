from zashel.virtualgpio import VirtualGPIOBaseHandler


class Handler(VirtualGPIOBaseHandler):
    def __init__(self, app):
        self._app = app
        self._lock = dict()
        self._lock[self.app.config["JAss"]["data"]["complaints"]["file"]] = list()
        self._lock[self.app.config["JAss"]["data"]["commitments"]["file"]] = list()

    def emit(self, signal):
        self._app.vgpio.send_all(signal)

    def signal_initializingdatasignal(self):
        print("Initializing Data")

    def signal_finishedinitializingdata(self):
        print("Ended Initializing Data")

    def signal_lockrow(self, file, unique_id):
        try:
            self._lock[file].append(unique_id) #Thik it better
        except:
            pass

    def signal_unlockrow(self, file, unique_id):
        try:
            self._lock[file].remove(unique_id) #Thik it better
        except:
            pass

