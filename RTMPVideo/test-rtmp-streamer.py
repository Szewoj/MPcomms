import cv2
import ffmpeg


RTMP_PATH = 'rtmp://192.168.0.224:1935/live/rgb'

if __name__ == "__main__":


    process = (
        ffmpeg
        .input('pipe:', r='6')
        .output(RTMP_PATH, vcodec='libx264', pix_fmt='yuv420p', preset='ultrafast', tune='zerolatency',
        r='20', g='50', video_bitrate='1.4M', maxrate='2M', bufsize='2M', segment_time='6',
        format='flv')
        .run_async(pipe_stdin=True)
    )

    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if ret:
            ret2, img2 = cv2.imencode('.png', img)
            process.stdin.write(img2.tobytes())

            cv2.imshow('streamer', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
