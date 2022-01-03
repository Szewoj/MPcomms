from datetime import datetime

class Message(object):
    def __init__(self, readingDate:str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")):
        self.readingDate = readingDate

    def getMsg(self, vid:int) -> dict:
        return {
            'vehicleId': vid,
            'readingDate': self.readingDate
        }

class PointCloudMsg(Message):
    def __init__(self, readingDate:str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),\
        pointCloudReading:str = None):

        super().__init__(readingDate=readingDate)
        self.pointCloudReading = pointCloudReading

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.pointCloudReading is not None:
            msg['pointCloudReading'] = self.pointCloudReading
        return msg

class LocationMsg(Message):
    def __init__(self, readingDate:str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),\
        slamXCoordinte:float = None, slamYCoordinate:float = None, slamRotation:float = None,\
        realXCoordinate:float = None, realYCoordinate:float = None):

        super().__init__(readingDate=readingDate)
        self.slamXCoordinte = slamXCoordinte
        self.slamYCoordinate = slamYCoordinate
        self.slamRotation = slamRotation
        self.realXCoordinate = realXCoordinate
        self.realYCoordinate = realYCoordinate

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.slamXCoordinte is not None:
            msg['slamXCoordinate'] = self.slamXCoordinte
        if self.slamYCoordinate is not None:
            msg['slamYCoordinate'] = self.slamYCoordinate
        if self.slamRotation is not None:
            msg['slamRotation'] = self.slamRotation
        if self.realXCoordinate is not None:
            msg['realXCoordinate'] = self.realXCoordinate
        if self.realYCoordinate is not None:
            msg['realYCoordinate'] = self.realYCoordinate
        return msg

class LidarReading(Message):
    def __init__(self, readingDate:str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),\
        lidarDistancesReading:str = None):

        super().__init__(readingDate=readingDate)
        self.lidarDistancesReading = lidarDistancesReading

    def getMsg(self, vid:int) -> dict:
        msg = super().getMsg(vid)
        if self.lidarDistancesReading is not None:
            msg['lidarDistancesReading'] = self.lidarDistancesReading
        return msg

if __name__ == '__main__':
    print(LocationMsg(\
        slamRot=5.0,\
        slamYCoord=10.0
        ).getMsg(5))
