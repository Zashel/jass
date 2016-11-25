from zashel.websocket import WebSocketMetaSignal as Signal

#TODO def emit(signal)

LockRowSignal = Signal("lockrow", ("file", "unique_id"), (str, str))
UnlockRowSignal = Signal("unlockrow", ("file", "unique_id"), (str, str))
WritingFileSignal = Signal("writingfile", ("file",), (str,))
WritingToFileSignal = Signal("writingtofile", ("old_file", "new_file"), (str, str))
FinishedWritingFileSignal = Signal("finishedwritingfile", ("file",), (str,))
ChangedRowSignal = Signal("changedrow", ("file", "unique_id", "data"), (str, str, dict))
NewRowSignal = Signal("newrow", ("file", "data"), (str, dict))
DelRowRignal = Signal("delrow", ("file", "unique_id"), (str, str))
NewIndexSignal = Signal("newindex", ("file", "field"), (str, str))
DelIndexSignal = Signal("delindex", ("file", "field"), (str, str))
