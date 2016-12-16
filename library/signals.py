from zashel.websocket import WebSocketMetaSignal as Signal


class HandlerRegister():
    handlers = list()
    @classmethod
    def register_handler(cls, handler):
        cls.handlers.append(handler)
    @classmethod
    def unregister_handler(cls, handler):
        cls.handlers.remove(handler)
    @classmethod
    def emit(cls, signal):
        for handler in cls.handlers:
            handler.emit(signal)

def emit(signal): #I have to think it better
    HandlerRegister.emit(signal)

InitializingDataSignal = Signal("initializingdata")
FinishedInitializingDataSignal = Signal("finishedinitializingdata")

LockRowSignal = Signal("lockrow", ("file", "unique_id"), (str, str))
UnlockRowSignal = Signal("unlockrow", ("file", "unique_id"), (str, str))

WritingFileSignal = Signal("writingfile", ("file",), (str,))
WritingToFileSignal = Signal("writingtofile", ("old_file", "new_file"), (str, str))
FinishedWritingFileSignal = Signal("finishedwritingfile", ("file",), (str,))

ChangedRowSignal = Signal("changedrow", ("file", "unique_id", "field", "value"), (str, str, str, str))
NewRowSignal = Signal("newrow", ("file", "data"), (str, dict))
DelRowSignal = Signal("delrow", ("file", "unique_id"), (str, str))

NewIndexSignal = Signal("newindex", ("file", "field"), (str, str))
DelIndexSignal = Signal("delindex", ("file", "field"), (str, str))

#GUI Signals

OpenInterfaceSignal = Signal("openinterface", ("interface", "data"), (str, list))
CloseInterfaceSignal = Signal("closeinterface", ("interface",), (str,))
ActionInterfaceSignal = Signal("actioninterface", ("action", "interface", "variables"), (str, str, dict))


LocaleSignal = Signal("locale", ("locale",), (dict,))
SetVariableSignal = Signal("setvariable", ("variable", "json"), (str, object))
SetDivVisibleSignal = Signal("setdivvisible", ("div_id", ), (str, ))
SetDatasetSignal = Signal("setdataset", ("interface", "data"), (str, str))

HiSignal = Signal("hi")
DrawNewInterfaceSignal = Signal("drawnewinterface", ("type_parent", "parent_name", "interface"),
                                (str, str, str))