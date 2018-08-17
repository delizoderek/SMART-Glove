import sys
import serial
import csv
import time
#from DataPlotting import IMUPlot
from IMU import IMU
count = 0
start = 0.0
end = 0.0
TOUT = 10
filename = raw_input("Enter Filename: ")
filename += ".csv"
ser = serial.Serial("COM11",9600,timeout = TOUT)
print "Connected"
print "Sent Connection Call"
print "Loading Calibration"
xCal = list()
yCal = list()
zCal = list()

with open('..\Data\CalibrationSignal.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        xCal.append(float(row[0]))
        yCal.append(float(row[1]))
        zCal.append(float(row[2]))


imu = IMU()
imu.calcOffsets(xCal,yCal,zCal)
imu.getOffsets()

ser.write("t")

recordedData = []
start = time.time()
while (end - start) <= 30.0:
    dataIn = []
    val = ser.read()
    while val != '_':
        dataIn.append(val)
        val = ser.read()
        
    if dataIn[0] == '\x00':
        dataIn = dataIn[1:]
        
    parsedData = ''.join(dataIn)
    recordedData.append(parsedData)
    end = time.time()
    print "Time Elapsed: %s Data String: %s" % ((end-start),parsedData)

print (end - start)
ser.write("d")
xData = list()
yData = list()
zData = list()

with open(filename,'wb') as file:
    for line in recordedData:
        temp = line.split(',')
        xData.append(float(temp[0]))
        yData.append(float(temp[1]))
        zData.append(float(temp[2]))
        file.write(line)
        file.write('\n')

    file.close()
