from .signals import *
from zashel.utils import CsvAsDb, search_win_drive
import os

def initiate_data(config):
    #TODO Emit Initiating Data
    remote_commitments = os.path.join(
        config["JAss"]["data"]["remote"],
        config["JAss"]["data"]["commitments"]["file"]
        )
    remote_complaints = os.path.join(
        config["JAss"]["data"]["remote"],
        config["JAss"]["data"]["complaints"]["file"]
        )
    commitments_headers = config["JAss"]["data"]["commitments"]["fields"]
    commitments_index = config["JAss"]["data"]["commitments"]["index"]
    complaints_headers = config["JAss"]["data"]["complaints"]["fields"]
    complaints_index = config["JAss"]["data"]["complaints"]["index"]
    commitments = CsvAsDb(remote_commitments, headers=commitments_headers, index=commitments_index)
    complaints = CsvAsDb(remote_complaints, headers=complaints_headers, index=complaints_index)
    commitments.write(headers=True)
    complaints.write(headers=True)


class SignaledCsdb(CsvAsDb):
    def __init__(self, *args, **kwargs):
        #TODO Emit Instantitating
        super().__init__(self, *args, **kwargs)

    def del_filter(self, *args, **kwargs):
        #TODO Emit Filter Deleted
        super().del_filter(*args, **kwargs)

    def del_index(self, *args, **kwargs):
        #TODO Emit Index Deleted
        super().del_index(*args, **kwargs)

    def del_row(self, *args, *kwargs):
        #TODO Emit Row Deleted
        super().del_row(*args, **kwargs)

    def modify_row(self, field, value):
        #TODO Emit Row Modified
        super()._data[super()._active_row][field] = value

    def insert_row(self, *args, **kwargs):
        #TODO Emit Row Inserted
        super().insert_row(*args, **kwargs)

    def set_active(self, *args, **kwargs):
        #TODO Emit Unlock/Lock
        super().set_active(*args, **kwargs)

    def set_index(self, *args, **kwargs):
        #TODO Emit Index Setted
        super().set_index(*args, **kwargs)

    def write(self, *args, **kwargs):
        #TODO Emit Writing
        super().write(*args, **kwargs)

    def write_to(self, *args, **kwargs):
        #TODO Emit Writing To...
        super().write_to(*args, **kwargs)



class Data():
    def __init__(self, config):
        self._config = config
        self._remote_commitments = os.path.join(
                self._config["JAss"]["data"]["remote"],
                self._config["JAss"]["data"]["commitments"]["file"]
                )
        self._local_commitments = os.path.join(
                self._config.local_path,
                self._config["JAss"]["data"]["commitments"]["file"]
                )
        self._commitments = SignaledCsdb(self._remote_commitments)
        self._commitments.write_to(self._local_commitments)
        self._remote_complaints = os.path.join(
            self._config["JAss"]["data"]["remote"],
            self._config["JAss"]["data"]["complaints"]["file"]
        )
        self._local_complaints = os.path.join(
            self._config.local_path,
            self._config["JAss"]["data"]["complaints"]["file"]
        )
        self._complaints = SignaledCsdb(self._remote_complaints)
        self._complaints.write_to(self._local_complaints)

    @property
    def commitments(self):
        return self._commitments

    @property
    def complaints(self):
        return self._complaints

    def export(self):
        pass
        #TODO

    def save(self):
        self._commitments.write()
        self._complaints.write()

    def save_remote(self):
        #Emitir señales
        #TODO
        self._commitments.write_to(self._remote_commitments)
        self._commitments.write_to(self._local_commitments)
        self._complaints.write_to(self._remote_complaints)
        self._complaints.write_to(self._local_complaints)