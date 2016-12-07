from zashel.virtualgpio import VirtualGPIOBaseHandler


class Handler(VirtualGPIOBaseHandler):
    def __init__(self, app):
        super().__init__()
        self._app = app


    def emit(self, signal):
        self._app.vgpio.send_all(signal)

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