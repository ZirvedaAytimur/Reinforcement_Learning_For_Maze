import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

airsim.wait_key('Press any key to takeoff')
client.takeoffAsync().join()

airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
client.moveToPositionAsync(-10, 10, -10, 5).join()

airsim.wait_key('Press any key to move vehicle to (-20, 10, -10) at 5 m/s')
client.moveToPositionAsync(-20, 10, -10, 5).join()

airsim.wait_key('Press any key to move vehicle to (-20, 20, -10) at 5 m/s')
client.moveToPositionAsync(-20, 20, -10, 5).join()

airsim.wait_key('Press any key to move vehicle to (-20, 20, -20) at 5 m/s')
client.moveToPositionAsync(-20, 20, -20, 5).join()

airsim.wait_key('Press any key to reset to original state')

client.armDisarm(False)
client.reset()