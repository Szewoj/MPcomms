import cv2
import ffmpeg


RTMP_PATH = 'rtmp://localhost/live/rgb'

if __name__ == "__main__":


    process = (
        ffmpeg
        .input('pipe:')
        .output(RTMP_PATH, vcodec='libx264', pix_fmt='yuv420p', preset='ultrafast', tune='zerolatency',
        s='640x480', format='flv')
        .run_async(pipe_stdin=True)
    )

    cap = cv2.VideoCapture(0)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

    while True:
        ret, img = cap.read()
        if ret:
            
            ret2, img2 = cv2.imencode('.jpg', img, encode_param)
            process.stdin.write(img2.tobytes())

            cv2.imshow('streamer', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
