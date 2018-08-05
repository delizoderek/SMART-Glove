import sys
import serial
import csv
import time

count = 0
start = 0.0
end = 0.0
ser = serial.Serial("COM11",9600)
print "Connected"
ser.write("Ready for data")
print "Sent Connection Call"
recordedData = []
start = time.time()
while (end - start) <= 40.0:
    dataIn = []
    val = ser.read(1)
    while val != '_':
        dataIn.append(val)
        val = ser.read(1)
        
    if dataIn[0] == '\x00':
        dataIn = dataIn[1:]
        
    parsedData = ''.join(dataIn)
    recordedData.append(parsedData)
    print parsedData
    end = time.time()

with open('IMUData.csv','wb') as file:
    for line in recordedData:
        file.write(line)
        file.write('\n')

    file.close()
