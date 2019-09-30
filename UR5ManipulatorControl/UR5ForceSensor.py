#!/usr/bin/env python
# encoding: utf-8

"""
The program is used to get the force sensor's force and torque.
Use the scene：UR5PegInHole2.ttt

@Author: Zane
@Contact: ely.hzb@gmail.com
@File: forceSensor.py   
@Time: 2019-07-31 15:55
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

##### Definition of parameters
sensorName = 'UR5_connection'

##### Obtain the handle
errorCode, returnHandle = vrep.simxGetObjectHandle(clientID, sensorName, vrep.simx_opmode_blocking)
forceSensorHandle = returnHandle

print('Handles available!') 


##### Get the force sensor's force and torque
while vrep.simxGetConnectionId(clientID) != -1:
    # simx_opmode_streaming initialization, no values are read at this time
    errorCode,state,forceVector,torqueVector=vrep.simxReadForceSensor(clientID,forceSensorHandle,vrep.simx_opmode_streaming)
    # Can't read twice at the same time, otherwise you can't read the value.
    time.sleep(1)
    # simx_opmode_buffer to obtain forceVector and torqueVector
    errorCode,state,forceVector,torqueVector=vrep.simxReadForceSensor(clientID,forceSensorHandle,vrep.simx_opmode_buffer)
    # Output the force of XYZ
    print(forceVector)
    # Output the torque of XYZ
    print(torqueVector)
