from .signals import *
from zashel.utils import CsvAsDb, search_win_drive
import os

def initiate_data(config):
    emit(InitializingDataSignal())
    remote_data = search_win_drive(config["data"]["remote"])
    remote_commitments = os.path.join(
        remote_data,
        config["commitments"]["file"]
        )
    remote_complaints = os.path.join(
        remote_data,
        config["complaints"]["file"]
        )
    commitments_headers = config["commitments"]["fields"].split("|")
    commitments_index = config["commitments"]["index"].split("|")
    complaints_headers = config["complaints"]["fields"].split("|")
    complaints_index = config["complaints"]["index"].split("|")
    print(remote_commitments)
    print(remote_complaints)
    commitments = CsvAsDb(remote_commitments, headers=commitments_headers, index=commitments_index)
    complaints = CsvAsDb(remote_complaints, headers=complaints_headers, index=complaints_index)
    commitments.write(headers=True)
    complaints.write(headers=True)
    emit(FinishedInitializingDataSignal())

class SignaledCsdb(CsvAsDb):
    def _del_index(self, field):
        self.del_index(field)

    def del_index(self, field):
        self._del_index(field)
        emit(DelIndexSignal(self._file_path, field))

    def _del_row_by_unique_id(self, unique_id):
        index = self._indexes["unique_id"][unique_id][0]
        self.del_row(index)

    def del_row(self, index=None):
        if index == None:
            index = self._active_row
        unique_id = self[self._active_row]["unique_id"]
        self.del_row(index)
        emit(DelRowSignal(index, unique_id))

    def modify(self, field, value):
        self._data[self._active_row][field] = value
        emit(ChangedRowSignal(self._file_path, self._data[self._active_row]["unique_id"], field, value))

    def modify_by_unique_id(self, unique_id, field, value):
        index = self._indexes["unique_id"][unique_id][0]
        self._data[index][field] = value

    def _insert_row(self, data):
        return self.insert_row(data)

    def insert_row(self, data):
        row = self._insert_row(data)
        emit(NewRowSignal(self._file_path, self._data[row]))

    def set_active(self, *args, **kwargs):
        if self._active_row is not None:
            emit(UnlockRowSignal(self._file_path, self._data[self._active_row]["unique_id"]))
        super().set_active(*args, **kwargs)
        emit(LockRowSignal(self._file_path, self._data[self._active_row]["unique_id"]))

    def _sset_index(self, field):
        super().set_index(field)

    def set_index(self, field):
        self._sset_index(field)
        emit(NewIndexSignal(self._file_path, field))

    def write(self, *args, **kwargs):
        emit(WritingFileSignal(self._file_path))
        super().write(*args, **kwargs)
        emit(FinishedWritingFileSignal(self._file_path))

    def write_to(self, new_path, headers=None):
        emit(WritingToFileSignal(self._file_path, new_path))
        super().write_to(new_path, headers)
        emit(FinishedWritingFileSignal(self._file_path))

    def to_send(self):
        final = list()
        for row in self:
            rdict = {"rowid": row}
            rdict.update(dict(self[row]))
            final.append(rdict)
        return final

class Data():
    def __init__(self, config, init=False):
        self._config = config
        if init is True:
            initiate_data(self._config)
        self._remote_commitments = search_win_drive(os.path.join(
                self._config["data"]["remote"],
                self._config["commitments"]["file"]
                ))
        self._local_commitments = os.path.join(
                self._config.local_path,
                self._config["commitments"]["file"]
                )
        self._commitments_index = self._config["commitments"]["index"].split("|")
        self._commitments = SignaledCsdb(self._remote_commitments, index=self._commitments_index)
        self._commitments.write_to(self._local_commitments)
        self._remote_complaints = search_win_drive(os.path.join(
            self._config["data"]["remote"],
            self._config["complaints"]["file"]
        ))
        self._local_complaints = os.path.join(
            self._config.local_path,
            self._config["complaints"]["file"]
        )
        self._complaints_index = self._config["complaints"]["index"].split("|")
        self._complaints = SignaledCsdb(self._remote_complaints, index=self._complaints_index)
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