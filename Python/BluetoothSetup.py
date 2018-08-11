import sys
import serial
import csv
import time
from DataPlotting import IMUPlot
count = 0
start = 0.0
end = 0.0
TOUT = 10
ser = serial.Serial("COM11",9600,timeout = TOUT)
print "Connected"
ser.write("c")
print "Sent Connection Call"
print "Calibrating"
var = ser.read();
calibrationData = list()
dataBuilder = list()
while var != 'd':
    if var == '_':
        dataLine = ''.join(dataBuilder)
        if dataLine[0] == '\x00':
            dataLine = dataLine[1:]
        print dataLine
        calibrationData.append(dataLine)
    else:
        dataBuilder.append(var)
    var = ser.read()
    
recordedData = []
start = time.time()
print "Out of while loop"
##
##while (end - start) <= 10.0:
##    dataIn = []
##    val = ser.read()
##    while val != '_':
##        dataIn.append(val)
##        val = ser.read()
##        
##    if dataIn[0] == '\x00':
##        dataIn = dataIn[1:]
##        
##    parsedData = ''.join(dataIn)
##    recordedData.append(parsedData)
##    print parsedData
##    end = time.time()
##
##xData = list()
##yData = list()
##zData = list()
##
##with open('IMUData.csv','wb') as file:
##    for line in recordedData:
##        temp = line.split(',')
##        xData.append(temp[0])
##        yData.append(temp[1])
##        zData.append(temp[2])
##        file.write(line)
##        file.write('\n')
##
##    file.close()
##
##IMU = IMUPlot(xData,yData,zData)
##IMU.plotData()
