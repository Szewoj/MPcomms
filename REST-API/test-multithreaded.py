from server import restAP
import time

if __name__ == "__main__":
    restAP.setMode(2)
    restAP.run_async()
    while True:
        time.sleep(1)
