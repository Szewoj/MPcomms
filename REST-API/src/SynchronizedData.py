import threading
from enumerators import Modes, EmergencyActions

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Mode object
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
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

    def pollMode(self) -> Modes: # clears _changed flag
        self._mutex.acquire()
        retval = self._mode
        self._changed = False
        self._mutex.release()
        return retval

    def lookupMode(self) -> Modes: # leaves _changed flag unchanged
        self._mutex.acquire()
        retval = self._mode
        self._mutex.release()
        return retval

    def setMode(self, mode: Modes) -> None:
        self._mutex.acquire()
        self._mode = mode
        self._changed = True
        self._mutex.release()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# EmergencyAction object
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class EmergencyAction(object):
    def __init__(self) -> None:
        self._changed = False
        self._action = EmergencyActions.NOTASK
        self._mutex = threading.Lock()
    
    def isChanged(self) -> bool:
        self._mutex.acquire()
        retval = self._changed
        self._mutex.release()
        return retval

    def pollAction(self) -> EmergencyActions: # clears _changed flag
        self._mutex.acquire()
        retval = self._action
        self._changed = False
        self._mutex.release()
        return retval

    def lookupAction(self) -> EmergencyActions: # leaves _changed flag unchanged
        self._mutex.acquire()
        retval = self._action
        self._mutex.release()
        return retval

    def setAction(self, action: EmergencyActions) -> None:
        self._mutex.acquire()
        self._action = action
        self._changed = True
        self._mutex.release()
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
