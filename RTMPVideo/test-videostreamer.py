import cv2
import streaming.VideoStreamer as VS
import time


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    streamer = VS.VideoStreamer('rgb')

    streamer.run()

    while True:
        ret, img = cap.read()
        if ret:
            ret2, img2 = cv2.imencode('.png', img)

            streamer.write_bytes(img2.tobytes())

            cv2.imshow('streamer', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    streamer.close()
