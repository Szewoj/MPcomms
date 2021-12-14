import threading
from enumerators import Modes

# --- MODE OBJECT ---

class Mode(object):

    def __init__(self) -> None:
        self._changed = False
        self._mode = Modes.STANDBY
        self._mutex = threading.Lock()
    
    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def getMode(self) -> Modes: # clears _changed flag
        self._mutex.acquire()
        retval = self._mode
        self._changed = False
        self._mutex.release()
        return retval

    def getModeCode(self) -> int: # leaves _changed flag
        self._mutex.acquire()
        retval = self._mode.value
        self._mutex.release()
        return retval

    def setMode(self, mode: Modes) -> None:
        self._mutex.acquire()
        self._mode = mode
        self._changed = True
        self._mutex.release()

#---
