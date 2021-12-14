from flask import Flask
from flask_restx import Resource, Api, fields
from enumerators import Modes, modeSwitch
import SynchronizedData as SD

class AccessPoint(object):
    app = Flask(__name__)
    api = Api(app)

    def __init__(self):
        self.mode = SD.Mode()

    def run(self):
        self.app.run(debug=True)

    def setMode(self, code):
        newMode = modeSwitch.get(code, Modes.INVALID)
        if(newMode != Modes.INVALID):
            self.mode.setMode(newMode)


# access variable 'restAP' to communicate with server
restAP = AccessPoint()


modeInModel = AccessPoint.api.model('ModeIn', {
    'mode': fields.Integer(required=True, description='Mode code for vehicle to switch to'),
    'mgck': fields.Integer(required=True, description='Magic number for verification')
})

modeInParser = AccessPoint.api.parser()
modeInParser.add_argument(
    'mode', type=int, required=True, help='Mode code for vehicle to switch to'
)
modeInParser.add_argument(
    'mgck', type=int, required=True, help='Magic number for verification'
)

modeOutModel = AccessPoint.api.model('ModeOut', {
    'mode': fields.Integer(description='Mode code, the vehicle is currently in')
})


@AccessPoint.api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@AccessPoint.api.route('/mode')
class Mode(Resource):
    @AccessPoint.api.marshal_with(modeOutModel)
    def get(self):
        return { 'mode': restAP.mode.getMode().value }

    @AccessPoint.api.expect(modeInModel)
    @AccessPoint.api.marshal_with(modeOutModel)
    def put(self):
        args = modeInParser.parse_args()
        restAP.setMode(args['mode'])
        return { 'mode': args['mode'] }



if __name__ == '__main__':
    restAP.run()