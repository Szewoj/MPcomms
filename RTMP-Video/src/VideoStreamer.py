#!/usr/bin/env python3
import ffmpeg
import NSProxy as NS

class VideoStreamer:
    def __init__(self, streamKey):
        self.rtmpAddr = NS.RTMP_ADDRESS + '/' + streamKey
        print(self.rtmpAddr)


if __name__ == '__main__':
    v = VideoStreamer('rgb')
    