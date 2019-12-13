import b0RemoteApi
import time

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi') as client:    
    doNextStep=True

    def simulationStepStarted(msg):
        simTime=msg[1][b'simulationTime'];
        print('Simulation step started. Simulation time: ',simTime)
        
    def simulationStepDone(msg):
        simTime=msg[1][b'simulationTime'];
        print('Simulation step done. Simulation time: ',simTime);
        global doNextStep
        doNextStep = True

    def gyroXCallback(msg):
        print('Gyro X: ', msg[1])
    
    def gyroYCallback(msg):
        print('Gyro Y: ', msg[1])
    
    def gyroZCallback(msg):
        print('Gyro Z: ', msg[1])

    def accelerometerXCallback(msg):
        print('Accelerometer X: ', msg[1])
    
    def accelerometerYCallback(msg):
        print('Accelerometer Y: ', msg[1])
    
    def accelerometerZCallback(msg):
        print('Accelerometer Z: ', msg[1])
    
    def barometerCallback(msg):
        print('Barometer: ', msg[1][2])

    # Motor Thrust
    client.simxSetFloatSignal('particleVelocity1', 0, client.simxDefaultPublisher())
    client.simxSetFloatSignal('particleVelocity2', 0, client.simxDefaultPublisher())
    client.simxSetFloatSignal('particleVelocity3', 0, client.simxDefaultPublisher())
    client.simxSetFloatSignal('particleVelocity4', 0, client.simxDefaultPublisher())

    # Gyroscope
    client.simxGetFloatSignal('gyroX', client.simxDefaultSubscriber(gyroXCallback))
    client.simxGetFloatSignal('gyroY', client.simxDefaultSubscriber(gyroYCallback))
    client.simxGetFloatSignal('gyroZ', client.simxDefaultSubscriber(gyroZCallback))

    # Accelerometer
    client.simxGetFloatSignal('accelerometerX', client.simxDefaultSubscriber(accelerometerXCallback))
    client.simxGetFloatSignal('accelerometerY', client.simxDefaultSubscriber(accelerometerYCallback))
    client.simxGetFloatSignal('accelerometerZ', client.simxDefaultSubscriber(accelerometerZCallback))

    # Barometer
    _, Quadricopter_base = client.simxGetObjectHandle('Quadricopter_base', client.simxServiceCall())
    client.simxGetObjectPosition(Quadricopter_base, -1, client.simxDefaultSubscriber(barometerCallback))

    client.simxSynchronous(True)
    client.simxGetSimulationStepStarted(client.simxDefaultSubscriber(simulationStepStarted))
    client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone))

    start = client.simxStartSimulation(client.simxDefaultPublisher())
    print(start)

    startTime=time.time()
    while time.time() - startTime < 15: 
        if doNextStep:
            doNextStep = False
            # Step Begin Here

            start = time.time()
            
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
            
            client.simxSynchronousTrigger()
            #print(1/(time.time() - start), "Hz")
        client.simxSpinOnce()
    
    client.simxStopSimulation(client.simxDefaultPublisher())