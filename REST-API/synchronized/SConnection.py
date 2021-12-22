import threading
from enum import Enum

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatus - status enumerator:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class ConnectionStatus(Enum):
    UNKNOWN           = -1
    DISCONNECTED      = 0b000
    PENDING           = 0b001
    CONNECTED_STANDBY = 0b010
    CONNECTED_ACTIVE  = 0b110
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatusSwitch - status enumerator switch:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectionStatusSwitch = {
    0b000: ConnectionStatus.DISCONNECTED,
    0b001: ConnectionStatus.PENDING,
    0b010: ConnectionStatus.CONNECTED_STANDBY,
    0b110: ConnectionStatus.CONNECTED_ACTIVE
}
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SConnection - synchronized connection class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SConnection(object):
    def __init__(self) -> None:
        self._mutex = threading.Lock()
        self._address = "-1"
        self._port = -1
        self._vehicleID = -1
        self._status = ConnectionStatus.UNKNOWN

    def identify(self, address:str, port:int, vid:int) -> bool:
        self._mutex.acquire()
        # ---
        retval = (address == self._address and\
                port == self._port and\
                vid == self._vehicleID)
        # ---
        self._mutex.release()
        return retval

    def connect(self, address:str, port:int, vid:int) -> None:
        self._mutex.acquire()
        # ---
        self._address = address
        self._port = port
        self._vehicleID = vid
        self._status = ConnectionStatus.CONNECTED_STANDBY
        # ---
        self._mutex.release()

    def disconnect(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.DISCONNECTED
        # ---
        self._mutex.release()

    def enable(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.CONNECTED_ACTIVE
        # ---
        self._mutex.release()

    def disable(self) -> None:
        self._mutex.acquire()
        # ---
        self._status = ConnectionStatus.CONNECTED_STANDBY
        # ---
        self._mutex.release()

    def getStatus(self) -> ConnectionStatus:
        self._mutex.acquire()
        # ---
        retval = self._status
        # ---
        self._mutex.release()
        return retval

    def getID(self) -> int:
        self._mutex.acquire()
        # ---
        retval = self._vehicleID
        # ---
        self._mutex.release()
        return retval

    # TODO connect, start transmitting, stop transmitting, messaging
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---