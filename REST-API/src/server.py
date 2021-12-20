from flask import Flask
from flask_restx import Resource, Api, fields
from enumerators import Modes, modeSwitch,\
                        EmergencyActions, emergencyActionsSwitch
import SynchronizedData as SD

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# AccessPoint class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class AccessPoint(object):
    app = Flask(__name__)
    api = Api(app)

    def __init__(self):
        self._mode = SD.Mode()
        self._emergencyAction = SD.EmergencyAction()

    def run(self):
        self.app.run(debug=True, use_reloader=False)

    # --- Mode ---
    def getMode(self) -> SD.Mode:
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
    def getEmergencyAction(self) -> SD.EmergencyAction:
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
modeInModel = AccessPoint.api.model('ModeRequest', {
    'mode': fields.Integer(required=True, description='Mode code for vehicle to switch to'),
    'mgck': fields.Integer(required=True, description='Magic number for verification')
})

modeOutModel = AccessPoint.api.model('ModeResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'mode': fields.Integer(description='Mode code, the vehicle is currently in')
})

emergencyInModel = AccessPoint.api.model('EmergencyActionRequest', {
    'ea': fields.Integer(required=True, description='Code for emergency action for vehicle to perform'),
    'mgck': fields.Integer(required=True, description='Magic number for verification')
})

emergencyOutModel = AccessPoint.api.model('EmergencyActionResponse', {
    'vid': fields.Integer(description='Vehicle ID'),
    'ea': fields.Integer(description='Emergency action that will be performed')
})
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Parsers used in communication:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
modeInParser = AccessPoint.api.parser()
modeInParser.add_argument(
    'mode', type=int, required=True, help='Mode code for vehicle to switch to'
)
modeInParser.add_argument(
    'mgck', type=int, required=True, help='Magic number for verification'
)

emergencyInParser = AccessPoint.api.parser()
emergencyInParser.add_argument(
    'ea', type=int, required=True, help='Code for emergency action for vehicle to perform'
)
emergencyInParser.add_argument(
    'mgck', type=int, required=True, help='Magic number for verification'
)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# REST Access Points:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
@AccessPoint.api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


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
            'vid': 5, # TODO change into actual vid
            'mode': restAP.lookupMode().value 
            }


@AccessPoint.api.route('/emergency')
class EmergencyAction(Resource):
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def get(self):
        return {
            'vid': 5, # TODO change into actual vid
            'ea': restAP.lookupEmergencyAction().value
            }

    @AccessPoint.api.expect(emergencyInModel)
    @AccessPoint.api.marshal_with(emergencyOutModel)
    def post(self):
        args = emergencyInParser.parse_args()
        restAP.setEmergencyAction(args['ea'])
        return {
            'vid': 5, # TODO change into actual vid
            'ea': restAP.lookupEmergencyAction().value
            }

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---


if __name__ == '__main__':
    restAP.run()


# TODO 
# (post) Add station access point
# (post) Start transmition
# (post) End transmition



