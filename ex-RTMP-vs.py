import cv2
import RTMPVideo.streaming.VideoStreamer as VS


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    streamer = VS.VideoStreamer('rgb')

    streamer.run()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

    while True:
        ret, img = cap.read()
        if ret:
            ret2, img2 = cv2.imencode('.jpg', img, encode_param)

            streamer.write_bytes(img2.tobytes())

            cv2.imshow('streamer', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    streamer.close()
