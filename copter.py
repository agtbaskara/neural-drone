import b0RemoteApi
import time
import numpy as np
import math
from remote import Remote

# 1. sudut roll (φ)
# 2. sudut pitch (θ)
# 3. sudut yaw(ψ)
# 4. kecepatan sudut roll (p)
# 5. kecepatan sudut pitch (q)
# 6. kecepatan sudut yaw (r)
# 7. posisi z (z)
# 8. kecepatan translasi z (V z )

"""
mat_x_dot = np.array([[1],
                  [2],
                  [3],
                  [4],
                  [5],
                  [6],
                  [7],
                  [8]])

mat_A = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

mat_x = np.array([[1],
                  [2],
                  [3],
                  [4],
                  [5],
                  [6],
                  [7],
                  [8]])

mat_B = np.array([[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]])

mat_u = np.array([[1],
                  [2],
                  [3],
                  [4]])

u1 = K[0][2]*(ketinggian-75)/1000 + K[0][5]*kec_vertikal/100
u2 = K[1][6]*(roll_deg+rollangle)/100000 + K[1][9] *(-gy)/1000000 + K[1][1]*(-ypos)/1000 + K[1][4]*y_speed/100000
u3 = K[2][7]*(-pitch_deg+pitchangle)/100000 + K[2][10]*(-gx)/1000000 + K[2][0]*xpos/1000 + K[2][3]*x_speed/100000
u4 = K[3][8]*(headingDegrees)/100000 +(K[3][11]/1000000)*(-gz)

w1 = Ainv [0][0]*u1 +Ainv[0][1]*u2 +Ainv[0][2]*u3 +Ainv[0][3]*u4
w2 = Ainv [1][0]*u1 +Ainv[1][1]*u2 +Ainv[1][2]*u3 +Ainv[1][3]*u4
w3 = Ainv [2][0]*u1 +Ainv[2][1]*u2 +Ainv[2][2]*u3 +Ainv[2][3]*u4
w4 = Ainv [3][0]*u1 +Ainv[3][1]*u2 +Ainv[3][2]*u3 +Ainv[3][3]*u4

wc1 = w1
wc2 = w2
wc3 = w3
wc4 = w4

motor1 = (int)((wc1/0.6729) +w0)
motor2 = (int)((wc2/0.6644) +w0)
motor3 = (int)((wc3/0.6813) +w0)
motor4 = (int)((wc4/0.6341) +w0)
"""

def simulationStepStarted(msg):
    simTime=msg[1][b'simulationTime']
    print('Simulation step started. Simulation time: ',simTime)
    
def simulationStepDone(msg):
    simTime=msg[1][b'simulationTime']
    print('Simulation step done. Simulation time: ',simTime)
    global doNextStep
    doNextStep = True

def gyroXCallback(msg):
    global acceleration_roll

    print('Gyro X: ', msg[1])

    acceleration_roll = msg[1]

def gyroYCallback(msg):
    global acceleration_pitch

    print('Gyro Y: ', msg[1])

    acceleration_pitch = msg[1]

def gyroZCallback(msg):
    global acceleration_yaw

    print('Gyro Z: ', msg[1])

    acceleration_yaw = msg[1]

def accelerometerXCallback(msg):
    print('Accelerometer X: ', msg[1])

def accelerometerYCallback(msg):
    print('Accelerometer Y: ', msg[1])

def accelerometerZCallback(msg):
    global acceleration_altitude

    print('Accelerometer Z: ', msg[1])

    acceleration_altitude = msg[1]

def orientationCallback(msg):
    global orientation_roll
    global orientation_pitch
    global orientation_yaw
    
    print('Orientation Roll: ', math.degrees(msg[1][0]))
    print('Orientation Pitch: ', math.degrees(msg[1][1]))
    print('Orientation Yaw: ', math.degrees(msg[1][2]))
    
    orientation_roll = msg[1][0]
    orientation_pitch = msg[1][1]
    orientation_yaw = msg[1][2]

def barometerCallback(msg):
    global altitude

    print('Barometer: ', msg[1][2])

    altitude = msg[1][2]

orientation_yaw = 0
orientation_pitch = 0
orientation_roll = 0
acceleration_yaw = 0
acceleration_pitch = 0
acceleration_roll = 0
altitude = 0
acceleration_altitude = 0
rcin = [0, 0, 0, 0, 0, 0, 0, 0]

mat_x_ref = np.array([[orientation_roll],
                      [orientation_pitch],
                      [orientation_yaw],
                      [acceleration_roll],
                      [acceleration_pitch],
                      [acceleration_yaw],
                      [altitude],
                      [acceleration_altitude]])

mat_K = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

mat_A = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

# Initialize Simulator
client = b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi') 
doNextStep=True

# Motor Thrust
client.simxSetFloatSignal('F450_particleVelocity1', 0, client.simxDefaultPublisher())
client.simxSetFloatSignal('F450_particleVelocity2', 0, client.simxDefaultPublisher())
client.simxSetFloatSignal('F450_particleVelocity3', 0, client.simxDefaultPublisher())
client.simxSetFloatSignal('F450_particleVelocity4', 0, client.simxDefaultPublisher())

# Gyroscope
client.simxGetFloatSignal('F450_gyroX', client.simxDefaultSubscriber(gyroXCallback))
client.simxGetFloatSignal('F450_gyroY', client.simxDefaultSubscriber(gyroYCallback))
client.simxGetFloatSignal('F450_gyroZ', client.simxDefaultSubscriber(gyroZCallback))

# Accelerometer
client.simxGetFloatSignal('F450_accelerometerX', client.simxDefaultSubscriber(accelerometerXCallback))
client.simxGetFloatSignal('F450_accelerometerY', client.simxDefaultSubscriber(accelerometerYCallback))
client.simxGetFloatSignal('F450_accelerometerZ', client.simxDefaultSubscriber(accelerometerZCallback))

# Orientation
_, F450 = client.simxGetObjectHandle('F450', client.simxServiceCall())
client.simxGetObjectOrientation(F450, -1, client.simxDefaultSubscriber(orientationCallback))

# Barometer
client.simxGetObjectPosition(F450, -1, client.simxDefaultSubscriber(barometerCallback))

# Initialize Remote
remote = Remote()

# Start Simulator
client.simxSynchronous(True)
client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulationStepStarted))
client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone))

start = client.simxStartSimulation(client.simxDefaultPublisher())
print(start)

def remap(x, in_min, in_max, out_min, out_max):
    return((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

startTime=time.time()
while time.time() - startTime < 150:
    rcin = remote.get_input()
    if doNextStep:
        doNextStep = False
        # Step Begin Here

        throttle = remap(rcin[2], 988, 2012, 0, 10)
        client.simxSetFloatSignal('F450_particleVelocity1', throttle, client.simxDefaultPublisher())
        client.simxSetFloatSignal('F450_particleVelocity2', throttle, client.simxDefaultPublisher())
        client.simxSetFloatSignal('F450_particleVelocity3', throttle, client.simxDefaultPublisher())
        client.simxSetFloatSignal('F450_particleVelocity4', throttle, client.simxDefaultPublisher())
        
        """
        u1 = K[0][2]*(altitude-75)/1000+K[0][5]*vertical_speed/100
        u2 = K[1][6]*(roll_deg+rollangle)/100000 + K[1][9] *(-gy)/1000000 + K[1][1]*(-ypos)/1000 + K[1][4]*y_speed/100000
        u3 = K[2][7]*(-pitch_deg+pitchangle)/100000 + K[2][10]*(-gx)/1000000 + K[2][0]*xpos/1000 + K[2][3]*x_speed/100000
        u4 = K[3][8]*(headingDegrees)/100000 +(K[3][11]/1000000)*(-gz)

        w1 = Ainv [0][0]*u1 +Ainv[0][1]*u2 +Ainv[0][2]*u3 +Ainv[0][3]*u4
        w2 = Ainv [1][0]*u1 +Ainv[1][1]*u2 +Ainv[1][2]*u3 +Ainv[1][3]*u4
        w3 = Ainv [2][0]*u1 +Ainv[2][1]*u2 +Ainv[2][2]*u3 +Ainv[2][3]*u4
        w4 = Ainv [3][0]*u1 +Ainv[3][1]*u2 +Ainv[3][2]*u3 +Ainv[3][3]*u4

        wc1 = w1
        wc2 = w2
        wc3 = w3
        wc4 = w4

        motor1 = (int)((wc1/0.6729) +w0)
        motor2 = (int)((wc2/0.6644) +w0)
        motor3 = (int)((wc3/0.6813) +w0)
        motor4 = (int)((wc4/0.6341) +w0)

        if time.time() - startTime < 5:
            client.simxSetFloatSignal('particleVelocity1', 6, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity2', 0, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity3', 6, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity4', 0, client.simxDefaultPublisher())
        
        if time.time() - startTime > 5:
            client.simxSetFloatSignal('particleVelocity1', 0, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity2', 6, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity3', 0, client.simxDefaultPublisher())
            client.simxSetFloatSignal('particleVelocity4', 6, client.simxDefaultPublisher())
        """
        # Step End Here
        client.simxSynchronousTrigger()
    client.simxSpinOnce()

client.simxStopSimulation(client.simxDefaultPublisher())