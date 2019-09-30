#!/usr/bin/env python
# encoding: utf-8

"""
PegInHole
Use the scene：UR5PegInHole2.ttt

@Author: Zane
@Contact: ely.hzb@gmail.com
@File: UR5PegInHole.py
@Time: 2019-07-29 15:55
"""
import vrep
import sys
import numpy as np
import math
import matplotlib.pyplot as mpl
import time

##### Definition of parameters

RAD2DEG = math.pi / 180  
# Define step size and timeout of simulation
step = 0.005  
TIMEOUT = 5000
# Define parameters of joint
jointNum = 6
jointName = 'UR5_joint'

##### Python connect to the V-REP client

print('Program started')
# Close potential connections
vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
print("Connection success")

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)
print("Simulation start")

i = 0
ur5ready = 0
while i < TIMEOUT and ur5ready == 0:
    i = i + 1
    errorCode, ur5ready = vrep.simxGetIntegerSignal(clientID, 'UR5READY', vrep.simx_opmode_blocking)
    time.sleep(step)

if i >= TIMEOUT:
    print('An error occurred in your V-REP server')
    vrep.simxFinish(clientID)
    
    
##### Obtain the handle
jointHandle = np.zeros((jointNum,), dtype=np.int)  # 注意是整型
for i in range(jointNum):
    errorCode, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i + 1), vrep.simx_opmode_blocking)
    jointHandle[i] = returnHandle
    time.sleep(2)

errorCode, holeHandle = vrep.simxGetObjectHandle(clientID, 'Hole', vrep.simx_opmode_blocking)
errorCode, ikTipHandle = vrep.simxGetObjectHandle(clientID, 'UR5_ikTip', vrep.simx_opmode_blocking)
errorCode, connectionHandle = vrep.simxGetObjectHandle(clientID, 'UR5_connection', vrep.simx_opmode_blocking)

print('Handles available!')

##### Obtain the position of the hole
errorCode, targetPosition = vrep.simxGetObjectPosition(clientID, holeHandle, -1, vrep.simx_opmode_streaming)
time.sleep(0.5)
errorCode, targetPosition = vrep.simxGetObjectPosition(clientID, holeHandle, -1, vrep.simx_opmode_buffer)
print('Position available!')

###### Joint space control

# Action1 of initConfig
initConfig = [0, 22.5 * RAD2DEG, 67.5 * RAD2DEG, 0, -90 * RAD2DEG, 0]

vrep.simxPauseCommunication(clientID, True)
for i in range(jointNum):
    vrep.simxSetJointTargetPosition(clientID, jointHandle[i], initConfig[i], vrep.simx_opmode_oneshot)
vrep.simxPauseCommunication(clientID, False)
# Make sure the step of simulation has been done
vrep.simxGetPingTime(clientID)
time.sleep(1)

# Get Object Quaternion
errorCode, tipQuat = vrep.simxGetObjectQuaternion(clientID, ikTipHandle, -1, vrep.simx_opmode_blocking)

# Action2 of targetPosition1

# The position of action2
targetPosition[2] = targetPosition[2] + 0.15

# Sent the signal of movement
vrep.simxPauseCommunication(clientID, 1)
vrep.simxSetIntegerSignal(clientID, 'ICECUBE_0', 21, vrep.simx_opmode_oneshot)
for i in range(1, 4):
    vrep.simxSetFloatSignal(clientID, 'ICECUBE_' + str(i), targetPosition[i - 1], vrep.simx_opmode_oneshot)
for i in range(4, 8):
    vrep.simxSetFloatSignal(clientID, 'ICECUBE_' + str(i), tipQuat[i - 4], vrep.simx_opmode_oneshot)
vrep.simxPauseCommunication(clientID, 0)

# Wait
j = 0
signal = 99
while j <= TIMEOUT and signal != 0:
    j = j + 1
    errorCode, signal = vrep.simxGetIntegerSignal(clientID, 'ICECUBE_0', vrep.simx_opmode_blocking)
    time.sleep(step)

errorCode = vrep.simxSetIntegerParameter(clientID, vrep.sim_intparam_current_page, 1, vrep.simx_opmode_blocking)

# Action3 of targetPosition2

# The position2 of action3
targetPosition[2] = targetPosition[2] - 0.05
time.sleep(2)

# Sent the signal of movement
vrep.simxPauseCommunication(clientID, 1)
vrep.simxSetIntegerSignal(clientID, 'ICECUBE_0', 21, vrep.simx_opmode_oneshot)
for i in range(1, 4):
    vrep.simxSetFloatSignal(clientID, 'ICECUBE_' + str(i), targetPosition[i - 1], vrep.simx_opmode_oneshot)
for i in range(4, 8):
    vrep.simxSetFloatSignal(clientID, 'ICECUBE_' + str(i), tipQuat[i - 4], vrep.simx_opmode_oneshot)
vrep.simxPauseCommunication(clientID, 0)

# Wait
j = 0
signal = 99
while j <= TIMEOUT and signal != 0:
    j = j + 1
    errorCode, signal = vrep.simxGetIntegerSignal(clientID, 'ICECUBE_0', vrep.simx_opmode_blocking)
    time.sleep(step)
time.sleep(1)

errorCode = vrep.simxSetIntegerParameter(clientID, vrep.sim_intparam_current_page, 0, vrep.simx_opmode_blocking)
time.sleep(2)

##### Stop simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
errorCode = vrep.simxSetIntegerSignal(clientID, 'ICECUBE_0', 1, vrep.simx_opmode_blocking)
time.sleep(0.5)

##### Close the connection to V-REP
vrep.simxFinish(clientID)
print('Program end')








