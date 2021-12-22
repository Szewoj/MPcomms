from flask import Flask, abort
from flask_restx import Resource, Api, fields
from authorization.magics import Magic
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

# Access variable 'restAP' to communicate with server
restAP = AccessPoint()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Models used in communication:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectInModel = AccessPoint.api.model('ConnectRequest', {
    'addr': fields.String(required=True, description='IPv4 address of communication endpoint'),
    'port': fields.Integer(required=True, description='Port used for communication'),
    'vid': fields.Integer(required=True, description='Vehicle ID set for the purpose of identification'),
    'mgc': fields.Integer(required=True, description='Magic number for verification')
})

connectOutModel = AccessPoint.api.model('ConnectResponse', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
})

activateInModel = AccessPoint.api.model('ConnectToggleRequest', {
    'activ': fields.Boolean(required=True, description='Activation flag'),
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'mgc': fields.Integer(required=True, description='Magic number for verification')
})

activateOutModel = AccessPoint.api.model('ConnectToggleResponse', {
    'vid': fields.Integer(required=True, description='Vehicle ID'),
    'activ': fields.Boolean(required=True, description='Activation flag'),
})

modeInModel = AccessPoint.api.model('ModeRequest', {
    'mode': fields.Integer(required=True, description='Mode code for vehicle to switch to'),
    'mgc': fields.Integer(required=True, description='Magic number for verification')
})

modeOutModel = AccessPoint.api.model('ModeResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'mode': fields.Integer(description='Mode code, the vehicle is currently in')
})

emergencyInModel = AccessPoint.api.model('EmergencyActionRequest', {
    'ea': fields.Integer(required=True, description='Code for emergency action for vehicle to perform'),
    'mgc': fields.Integer(required=True, description='Magic number for verification')
})

emergencyOutModel = AccessPoint.api.model('EmergencyActionResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'ea': fields.Integer(description='Emergency action that will be performed')
})
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Parsers used in communication:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
connectInParser = AccessPoint.api.parser()
connectInParser.add_argument(
    'addr', type=str, required=True, help='IPv4 address of communication endpoint'
)
connectInParser.add_argument(
    'port', type=int, required=True, help='Port used for communication'
)
connectInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID set for the purpose of identification'
)
connectInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
activateInParser = AccessPoint.api.parser()
activateInParser.add_argument(
    'activ', type=bool, required=True, help='Activation flag'
)
activateInParser.add_argument(
    'vid', type=int, required=True, help='Vehicle ID'
)
activateInParser.add_argument(
    'activ', type=int, required=True, help='Magic number for verification'
)
# ---
modeInParser = AccessPoint.api.parser()
modeInParser.add_argument(
    'mode', type=int, required=True, help='Mode code for vehicle to switch to'
)
modeInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# ---
emergencyInParser = AccessPoint.api.parser()
emergencyInParser.add_argument(
    'ea', type=int, required=True, help='Code for emergency action for vehicle to perform'
)
emergencyInParser.add_argument(
    'mgc', type=int, required=True, help='Magic number for verification'
)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# REST Access Points:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
@AccessPoint.api.route('/connect')
class Connection(Resource):
    @AccessPoint.api.expect(connectInModel)
    @AccessPoint.api.marshal_with(connectOutModel)
    def post(self):
        if(restAP.getConnectionStatus() in [ConnectionStatus.UNKNOWN, ConnectionStatus.DISCONNECTED]):
            args = connectInParser.parse_args()
            restAP._connection.connect(args['addr'], args['port'], args['vid'])
            return {'vid': restAP.getVehicleID()}
        else:
            abort(409, "Vehicle is already connected to another base")

    @AccessPoint.api.expect(connectInModel)
    @AccessPoint.api.marshal_with(connectOutModel)
    def delete(self):
        if(restAP.getConnectionStatus() not in [ConnectionStatus.UNKNOWN, ConnectionStatus.DISCONNECTED]):
            args = connectInParser.parse_args()
            if(restAP.identifyConnection(args['addr'], args['port'], args['vid'])):
                restAP.disconnect()
                return {'vid': restAP.getVehicleID()}
            else:
                abort(404, "There is no active connection with specified values")
        else:
            abort(404, "There is no active connection")


@AccessPoint.api.route('/connect/activate')
class ConnectionActivate(Resource):
    @AccessPoint.api.expect(activateInModel)
    @AccessPoint.api.marshal_with(activateOutModel)
    def put(self):
        if(restAP.getConnectionStatus() not in [ConnectionStatus.UNKNOWN, ConnectionStatus.DISCONNECTED]):
            args = activateInParser.parse_args()
            if(args['vid'] == restAP.getVehicleID()):
                restAP.activate(args['activ'])
                return {'vid': restAP.getVehicleID(),
                        'activ': args['activ']}
            else:
                abort(404, "There is no active connection with passed ID")
        else:
            abort(404, "There is no active connection")


@AccessPoint.api.route('/mode')
class Mode(Resource):
    @AccessPoint.api.marshal_with(modeOutModel)
    def get(self):
        return { 
            'vid': 5, # TODO change into actual vid
            'mode': restAP.lookupMode().value 
            }

    @AccessPoint.api.expect(modeInModel)
    @AccessPoint.api.marshal_with(modeOutModel)
    def post(self):
        args = modeInParser.parse_args()
        restAP.setMode(args['mode'])
        return {
            'vid': restAP.getVehicleID(), # TODO change into actual vid
            'mode': restAP.lookupMode().value 
            }


@AccessPoint.api.route('/emergency')
class EmergencyAction(Resource):
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def get(self):
        return {
            'vid': restAP.getVehicleID(), # TODO change into actual vid
            'ea': restAP.lookupEmergencyAction().value
            }

    @AccessPoint.api.expect(emergencyInModel)
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def post(self):
        args = emergencyInParser.parse_args()
        restAP.setEmergencyAction(args['ea'])
        return {
            'vid': restAP.getVehicleID(), # TODO change into actual vid
            'ea': restAP.lookupEmergencyAction().value
            }

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


if __name__ == '__main__':
    restAP.run()

