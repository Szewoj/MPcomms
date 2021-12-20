import threading
from enum import Enum

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatus - status enumerator:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class ConnectionStatus(Enum):
    UNKNOWN       = -1
    DISCONNECTED  = 0b00
    PENDING       = 0b01
    CONNECTED     = 0b10
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ConnectionStatusSwitch - status enumerator switch:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectionStatusSwitch = {
    0b00: ConnectionStatus.DISCONNECTED,
    0b00: ConnectionStatus.PENDING,
    0b00: ConnectionStatus.CONNECTED
}
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# SConnection - synchronized connection class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class SConnection(object):
    def __init__(self) -> None:
        self._address = None
        self._vehicleID = -1
        self._status = ConnectionStatus.UNKNOWN
        self._mutex = threading.Lock()

    # TODO connect, start transmitting, stop transmitting, messaging
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---