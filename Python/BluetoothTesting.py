import sys
import serial
from IMU import IMU
import matplotlib
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv

count = 0
start = 0.0
end = 0.0
TOUT = 10
ser = serial.Serial("COM11",9600,timeout = TOUT)
print "Connected"

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
        if samplesCollected < 50:
            print "Keep device still"
        elif samplesCollected < 150:
            print "Move Y direction"
            xCal.append(float(valueArray[0]))
        elif samplesCollected < 200:
            print "Stop"
        elif samplesCollected < 300:
            print "Move X direction"
            yCal.append(float(valueArray[1]))
            zCal.append(float(valueArray[2]))
        else:
            print "Stop"
        
        samplesCollected += 1
        dataBuilder = list()
    else:
        dataBuilder.append(var)
    var = ser.read()

with open('CalibrationSignal.csv','wb') as file:
    for i in range(0,len(xCal)):
        line = "%s,%s,%s,0,0,0\n" % (xCal[i],yCal[i],zCal[i])
        file.write(line)
        
plt.subplot(311)
plt.plot(xCal)
plt.subplot(312)
plt.plot(yCal)
plt.subplot(313)
plt.plot(zCal)
plt.show()
print "Calibration Completed"
