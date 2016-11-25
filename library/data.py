from .signals import *
from zashel.utils import CsvAsDb, search_win_drive
import os

def initiate_data(config):
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
        self._commitments = CsvAsDb(self._remote_commitments)
        self._commitments.write_to(self._local_commitments)
        self._remote_complaints = os.path.join(
            self._config["JAss"]["data"]["remote"],
            self._config["JAss"]["data"]["complaints"]["file"]
        )
        self._local_complaints = os.path.join(
            self._config.local_path,
            self._config["JAss"]["data"]["complaints"]["file"]
        )
        self._complaints = CsvAsDb(self._remote_complaints)
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