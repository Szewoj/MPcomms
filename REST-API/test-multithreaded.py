from datetime import datetime
from server import restAP
import time

if __name__ == "__main__":
    restAP.setMode(2)
    restAP.run_async()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
