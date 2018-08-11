import sys
import serial
from IMU import IMU
count = 0
start = 0.0
end = 0.0
TOUT = 10
ser = serial.Serial("COM11",9600,timeout = TOUT)
print "Connected"
print "Calibrate X"
ser.write("c")
var = ser.read()
xCal = list()
yCal = list()
zCal = list()
dataBuilder = list()
samplesCollected = 0
while var != 'd':
    if var == '_':
        dataLine = ''.join(dataBuilder)
        if dataLine[0] == '\x00':
            dataLine = dataLine[1:]
        print dataLine
        valueArray = dataLine.split(',')
        
        if samplesCollected < 100:
            print "Move Y direction"
            xCal.append(float(valueArray[0]))
        elif samplesCollected < 150:
            print "Stop"
        elif samplesCollected < 350:
            print "Move X direction"
            yCal.append(float(valueArray[1]))
            zCal.append(float(valueArray[2]))
        else:
            print "Stop"
        
        samplesCollected += 1
        print '\n','\n',samplesCollected,'\n','\n'
        dataBuilder = list()
    else:
        dataBuilder.append(var)
    var = ser.read()

imu = IMU()
imu.calcAxOffset(xCal)
imu.calcAyOffset(yCal)
imu.calcAzOffset(zCal)
imu.getOffsets()
print "Calibration Completed"
