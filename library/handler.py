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

    def datagrid(self, file):
        datagrid = None
        if file == self._config["complaints"]["file"]:
            datagrid = "complaints_grid"
        elif file == self._config["commitments"]["file"]:
            datagrid = "commitments_grid"
        return datagrid

    def signal_changedrow(self, file, unique_id, field, value):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile.modify_by_unique_id(unique_id, field, value)
        interface = self.datagrid(file)
        self._app.websocket.send_all(ChangedRowSignal(file, unique_id, field, value))

    def signal_newrow(self, file, data):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._insert_row(file, data)
        interface = self.datagrid(file)
        self._app.websocket.send_all(NewRowSignal(file, data))

    def signal_delrow(self, file, unique_id):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._del_row_by_unique_id(unique_id)
        interface = self.datagrid(file)
        self._app.websocket.send_all(SetDatasetSignal(interface, datafile.to_send()))

    def signal_newindex(self, file, field):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._set_index(field)

    def signal_delindex(self, file, field):
        datafile = self.datafile(file)
        if datafile is not None:
            datafile._del_index(field)

    def signal_openinterface(self, signal, addr):
        pass

    def signal_closeinterface(self, signal, addr):
        pass

    def signal_actioninterface(self, signal, addr):
        print("Got an action")
        action = signal.please_do
        interface = signal.interface
        variables = signal.variables
        print(action)
        data_name = interface.replace("_grid", "")
        if action == "sort_grid":
            print("Let's sort!")
            field, sorting = variables["field"], variables["sorting"]
            data = self._app.data.__getattribute__(data_name)
            data.set_sort(field, sorting)
            self._app.websocket.send_all(SetDatasetSignal(interface, data.to_send()))
        elif action == "set_active":
            print("Active {} in {}".format(variables["row"], interface))
            data = self._app.data.__getattribute__(data_name)
            data.set_active(variables["row"])
        elif action == "update_reg":
            field = variables["field"]
            value = variables["value"]
            data = self._app.data.__getattribute__(data_name)
            data[field] = value
            while True:
                if data_name not in self._app._file_lock:
                    break
                time.sleep(1)
            data.write()
            print("guardado")
        elif action == "new_row":
            print(variables["row"])

    def signal_pong(self, signal=None, addr=None):
        print("pong")
        self._app.pong = True

    def signal_bye(self, signal=None, addr=None):
        print("bye")
        WebSocketBaseHandler.signal_bye(self, signal, addr)
        self._app.executing = False

    def signal_hi(self, signal=None, addr=None):
        print("hi")
        self._app.websocket.send_all(SetVariableSignal(
            "local_strings",
            Locale(self._app.config["JAss"]["location"]).to_dict()
            ))
        self._app.websocket.send_all(SetVariableSignal(
            "commitment_type_selections",
            self._app.config["commitments_selectors"]["type"].split("|")
            ))
        self._app.websocket.send_all(SetVariableSignal(
            "commitment_status_selections",
            self._app.config["commitments_selectors"]["status"].split("|")
        ))
        self._app.websocket.send_all(SetVariableSignal(
            "complaint_reason_selections",
            self._app.config["complaints_selectors"]["reason"].split("|")
        ))
        self._app.websocket.send_all(OpenInterfaceSignal(
            "commitments_grid",
            self._app.data.commitments.to_send()
        ))
        self._app.websocket.send_all(OpenInterfaceSignal(
            "complaints_grid",
            self._app.data.commitments.to_send()
        ))

        self._app.websocket.send_all(SetDivVisibleSignal(
            "main"
        ))