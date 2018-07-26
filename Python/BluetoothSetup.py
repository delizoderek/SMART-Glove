import sys
import serial
import csv


ser = serial.Serial("COM11",9600)
print "Connected"
ser.write("Ready for data")
print "Sent Connection Call"

try:
    recordedData = []
    while 1:
        dataIn = []
        val = ser.read(1)
        while val != '_':
            dataIn.append(val)
            val = ser.read(1)

        parsedData = ''.join(dataIn)
        recordedData.append(parsedData)
        print parsedData
         
except KeyboardInterrupt:
    with open('IMUData.csv','wb') as file:
        for line in recordedData:
            file.write(line)
            file.write('\n')

        file.close()
