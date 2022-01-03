from datetime import datetime
from messaging.Messages import ImuReadingMsg
from server import restAP
import time

if __name__ == "__main__":
    restAP.setMode(2)
    restAP.run_async()

    while True:
        try:
            time.sleep(1)
            bl = restAP.send(
                ImuReadingMsg(
                    accelerationX=1.7,
                    accelerationY=1.8,
                    accelerationZ=1.9
                )
            )
            print(bl)
        except KeyboardInterrupt:
            break
