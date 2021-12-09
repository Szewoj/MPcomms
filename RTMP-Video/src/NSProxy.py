import sys
import os

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(os.path.dirname(parent))

import NetworkSettings

IP_ADDRESS = NetworkSettings.IP_ADDRESS
RTMP_APP = NetworkSettings.RTMP_APP
RTMP_ADDRESS = NetworkSettings.RTMP_ADDRESS