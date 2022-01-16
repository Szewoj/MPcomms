# --- --- --- --- --- --- --- --- --- --- --- --- ---
# Example fullstack communication code
# --- --- --- --- --- --- --- --- --- --- --- --- ---

# Import used messages from messaging package:
from RestAPI.messaging.Messages import LidarReadingMsg, LocationMsg, PointCloudMsg, formatTime, ImuReadingMsg, DiagnosticDataMsg

# Import enums used in state variables:
from RestAPI.synchronized.SEmergencyAction import EmergencyActions
from RestAPI.synchronized.SMode import Modes

# Import AccessPoint variable form server package:
from RestAPI.server import restAP 

# Import streaming class
import RTMPVideo.streaming.VideoStreamer as VS

# Video generator -- replace with camera capture
import RTMPVideo.DummyCap as DCap, cv2

# Readings generator -- replace with real readings
from readings import ExampleReadings

# Other imports:
import time, random, threading
from datetime import datetime

def sendVideo():
    #cap = DCap.DummyCap()
    cap = cv2.VideoCapture("harry.avi")

    streamer_rgb = VS.VideoStreamer('rgb')
    streamer_gs = VS.VideoStreamer('gs')

    streamer_rgb.run()
    streamer_gs.run()

    while True:
        ret, img_rgb = cap.read()
        if ret:
            img_gs = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            streamer_rgb.publishFrame(img_rgb)
            streamer_gs.publishFrame(img_gs)

if __name__ == "__main__":
    # Start streamer as daemon:
    stream_thread = threading.Thread()
    stream_thread.daemon = True
    stream_thread.start()

    # Start server as daemon:
    restAP.run_async()

    print("Server started on address localhost:5000/api")
    print("Documentation accessible at http://localhost:5000/api/doc")

    while True:
        try:
            time.sleep(0.5)
            # --- --- --- --- --- --- ---
            # --- GENERAL OPERATIONS: ---
            # --- --- --- --- --- --- ---

            # example measurement:
            m_lidar = ExampleReadings.LidarReadings.getNext()
            m_location = ExampleReadings.LocationReadings.getNext()
            m_pointCloud = ExampleReadings.PointCloudReading.getNext()
            

            # --- --- --- --- --- --- ---
            
            # --- --- --- --- --- --- ---
            # ---   SEND READINGS:    ---
            # --- --- --- --- --- --- ---

            if(restAP.isActive()): # <- Active state means that there is
                                   #    existing connection that waits for data
            
                # send lidar measurement
                restAP.send(LidarReadingMsg(
                    lidarDistancesReading=m_lidar
                ))

                # send location measurement
                restAP.send(LocationMsg(
                    slamXCoordinate=m_location["slamXCoordinate"],
                    slamYCoordinate=m_location["slamYCoordinate"],
                    slamRotation=m_location["slamRotation"],
                    realXCoordinate=m_location["realXCoordinate"],
                    realYCoordinate=m_location["realYCoordinate"],
                ))

                # send point cloud reading
                restAP.send(PointCloudMsg(
                    pointCloudReading=m_pointCloud
                ))


            # --- --- --- --- --- --- ---

            # --- --- --- --- --- --- ---
            # ---   POLL CHANGES:     ---
            # --- --- --- --- --- --- ---

            # Mode changed:
            if(restAP.modeChanged()):
                mode = restAP.pollMode() # <- poll resets _changed flag
                # mode changed routine goes here:
                print("[i] Received new mode: " + str(mode))

            # Emergency changed:
            if(restAP.emergencyActionChanged()):
                ea = restAP.pollEmergencyAction() # <- poll resets _changed flag
                # mode changed routine goes here:
                print("[i] Received new emergency action: " + str(ea))

            # --- --- --- --- --- --- ---

            # --- --- --- --- --- --- ---
            # --- SET API VARIABLES:  ---
            # --- --- --- --- --- --- ---

            if(restAP.lookupEmergencyAction() == EmergencyActions.STOP):
                restAP.setMode(Modes.STANDBY)

            # --- --- --- --- --- --- ---
        except KeyboardInterrupt:
            break
