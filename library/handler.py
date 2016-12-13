from zashel.virtualgpio import VirtualGPIOBaseHandler
from zashel.websocket import WebSocketBaseHandler
from .config import Locale
from .signals import *


import time


class Handler(VirtualGPIOBaseHandler, WebSocketBaseHandler):
    def __init__(self, app):
        WebSocketBaseHandler.__init__(self)
        VirtualGPIOBaseHandler.__init__(self)
        self._app = app

    def emit(self, signal):
        self._app.vgpio.send_all(signal)

    def terminate(self, counter):
        if counter is 0:
            self._app.executing = False

    def signal_initializingdatasignal(self):
        print("Initializing Data")

    def signal_finishedinitializingdata(self):
        print("Ended Initializing Data")

    def signal_lockrow(self, file, unique_id):
        try:
            self._app._lock[file].append(unique_id) #Thik it better
        except:
            pass

    def signal_unlockrow(self, file, unique_id):
        try:
            self._app._lock[file].remove(unique_id) #Thik it better
        except:
            pass

    def signal_writingfile(self, filename):
        self._app._file_lock.append(filename)

    def signal_writingtofile(self, oldfile, newfile):
        pass

    def signal_finishedwritingfile(self, filename):
        self._app._file_lock.remove(filename)

    def datafile(self, file):
        datafile = None
        if file == self._config["complaints"]["file"]:
            datafile = self._app.data.complaints
        elif file == self._config["commitments"]["file"]:
            datafile = self._app.data.commitments
        return datafile

    def signal_changedrow(self, file, unique_id, field, value):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile.modify_by_unique_id(unique_id, field, value)

    def signal_newrow(self, file, data):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._insert_row(file, data)

    def signal_delrow(self, file, unique_id):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._del_row_by_unique_id(unique_id)

    def signal_newindex(self, file, field):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._set_index(field)

    def signal_delindex(self, file, field):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._del_index(field)

    def signal_openinterface(self, interface):
        pass

    def signal_closeinterface(self, interface):
        pass

    def signal_actioninterface(self, action, interface, variables):
        pass

    def signal_pong(self, signal=None, addr=None):
        print("pong")
        self._app.pong = True

    def signal_bye(self, signal=None, addr=None):
        print("bye")
        WebSocketBaseHandler.signal_bye(self, signal, addr)
        self._app.executing = False

    def signal_hi(self, signal=None, addr=None):
        print("hi")
        self._app.websocket.send_all(LocaleSignal(
            Locale(self._app.config["JAss"]["location"]).to_dict()
            ))
        time.sleep(1)
        self._app.websocket.send_all(OpenInterfaceSignal(
            "commitments_grid",
            self._app.data.commitments.to_send()
            ))