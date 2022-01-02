#!/usr/bin/env python3
import ffmpeg
import streaming.NSProxy as NS

class VideoStreamer:
    def __init__(self, streamKey):
        self.rtmpAddr = NS.RTMP_ADDRESS + '/' + streamKey
        self.stream = (
            ffmpeg
            .input('pipe:', r='6')
            .output(self.rtmpAddr,vcodec='libx264', pix_fmt='yuv420p', preset='ultrafast', tune='zerolatency',
            r='30', g='50', video_bitrate='1.4M', maxrate='4M', bufsize='0M', segment_time='6',
            format='flv', loglevel="quiet")
        )

    def run(self):
        self.process = ffmpeg.run_async(self.stream, pipe_stdin=True)

    def write_bytes(self, bytes):
        self.process.stdin.write(bytes)

    def close(self):
        self.process.stdin.close()
        self.process.terminate()


if __name__ == '__main__':
    v = VideoStreamer('rgb')
    