#!/usr/bin/env python3
import ffmpeg

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# VideoStreamer - rtmp video provider class:
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class VideoStreamer:
    __RTMP_ADDRESS = "rtmp://localhost/live" # for provided nginx settings it stays the same
# ---
    def __init__(self, streamKey):
        self.streamKey = streamKey
        self.running = False
        
    def getRTMPAddress(self) -> str:
        return VideoStreamer.__RTMP_ADDRESS + '/' + self.streamKey
# ---
    def run(self):
        self.stream = (
            ffmpeg
            .input('pipe:')
            .output(self.getRTMPAddress(), vcodec='libx264', pix_fmt='yuv420p', preset='ultrafast', tune='zerolatency',
            s='640x480', format='flv', loglevel="panic")
        )
        self.process = ffmpeg.run_async(self.stream, pipe_stdin=True)
# ---
    def write_bytes(self, bytes):
        self.process.stdin.write(bytes)
# ---
    def close(self):
        self.process.stdin.close()
        self.process.terminate()
# ---

if __name__ == '__main__':
    v = VideoStreamer('rgb')
    