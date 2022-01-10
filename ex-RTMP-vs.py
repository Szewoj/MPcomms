import cv2
import RTMPVideo.streaming.VideoStreamer as VS


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    streamer_rgb = VS.VideoStreamer('rgb')
    streamer_gs = VS.VideoStreamer('gs')

    streamer_rgb.run()
    streamer_gs.run()

    while True:
        ret, img = cap.read()
        if ret:
            
            img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret2, img_rgb = cv2.imencode('.bmp', img)
            ret3, img_gs = cv2.imencode('.bmp', img_g)

            streamer_rgb.write_bytes(img_rgb.tobytes())
            streamer_gs.write_bytes(img_gs.tobytes())

            cv2.imshow('streamer', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    streamer_rgb.close()
    streamer_gs.close()
