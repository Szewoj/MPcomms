from flask import Flask
from flask_restx import Api
from synchronized.SMode import *
from synchronized.SEmergencyAction import *
from synchronized.SConnection import *

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# AccessPoint class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class AccessPoint(object):
    app = Flask(__name__)
    api = Api(app)

    def __init__(self):
        self._mode = SMode()
        self._emergencyAction = SEmergencyAction()
        self._connection = SConnection()
        self._th = None

    def run(self):
        self.app.run(debug=True, use_reloader=False)

    def run_async(self):
        self._th = threading.Thread(target=self.run).start()

    # --- Connection ---
    def getVehicleID(self) -> int:
        return self._connection.getID()

    def getConnectionStatus(self) -> ConnectionStatus:
        return self._connection.getStatus()

    def isOnline(self) -> bool:
        return self._connection.isOnline()

    def isOffline(self) -> bool:
        return self._connection.isOffline()

    def connect(self, address:str, port:int, vid:int) -> None:
        self._connection.connect(address, port, vid)

    def disconnect(self) -> None:
        self._connection.disconnect()

    def identifyConnection(self, address:str, port:int, vid:int) -> bool:
        return self._connection.identify(address, port, vid)

    def activate(self, toggle:bool) -> None:
        if toggle:
            self._connection.enable()
        else:
            self._connection.disable()    

    # --- Mode ---
    def getMode(self) -> SMode:
        return self._mode

    def pollMode(self) -> Modes:
        return self._mode.pollMode()

    def lookupMode(self) -> Modes:
        return self._mode.lookupMode()

    def setMode(self, code) -> None:
        newMode = modeSwitch.get(code, Modes.INVALID)
        if(newMode != Modes.INVALID):
            self._mode.setMode(newMode)

    # --- EmergencyAction ---
    def getEmergencyAction(self) -> SEmergencyAction:
        return self._emergencyAction

    def pollEmergencyAction(self) -> EmergencyActions:
        return self._emergencyAction.pollAction()

    def lookupEmergencyAction(self) -> EmergencyActions:
        return self._emergencyAction.lookupAction()

    def setEmergencyAction(self, code) -> None:
        newEA = emergencyActionsSwitch.get(code, EmergencyActions.INVALID)
        if(newEA != EmergencyActions.INVALID):
            self._emergencyAction.setAction(newEA)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
