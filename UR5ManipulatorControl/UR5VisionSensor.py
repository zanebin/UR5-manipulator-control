#!/usr/bin/env python
# encoding: utf-8

"""
Enable the vision sensor in V-REP,Python
use the scene：UR5VisionSensor.ttt

@Author: Zane
@Contact: ely.hzb@gmail.com
@File: VisionSensorDemo.py
@Time: 2019-07-23 15:55
"""
import vrep
import sys
import numpy as np
import math
import matplotlib.pyplot as mpl
import time

##### Python connect to the V-REP client

print('Program started')
# Close potential connections
vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
print("Connection success")

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)
print("Simulation start")

##### Obtain the handle
errorCode,visionSensorHandle = vrep.simxGetObjectHandle(clientID,'Cam',vrep.simx_opmode_oneshot_wait)

##### Get the image of vision sensor
errprCode,resolution,image = vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
time.sleep(0.1)
errprCode,resolution,image = vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)

#Process the image to the format (64,64,3)
sensorImage = []
sensorImage = np.array(image,dtype = np.uint8)
sensorImage.resize([resolution[0],resolution[1],3])

#Use matplotlib.imshow to show the image
mpl.imshow(sensorImage,origin='lower')

    
