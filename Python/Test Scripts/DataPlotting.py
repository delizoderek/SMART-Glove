import matplotlib
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv
from IMU import IMU

class IMUPlot:

    def __init__(self,data1,data2,data3,dTime):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.xShift = 1239.06
        self.yShift = -855.444
        self.zShift = -15994
        self.xBound = 0.005
        self.yBound = 0.01
        self.zBound = 0.01
        self.dt = dTime

    def plotData(self):
        ##accelX,accelY,accelZ = self.filterData()
        
        #time, velX = self.getVelocity(accelX,self.dt)
        #time, velY = self.getVelocity(accelY,self.dt)
        #time, velZ = self.getVelocity(accelZ,self.dt)

        #xPos = self.getPosition(time,velX,butter1Shift)
        #yPos = self.getPosition(time,velY,butter2Shift)
        #zPos = self.getPosition(time,velZ,butter3Shift)

        plt.subplot(131)
        plt.plot(self.data1)
        plt.subplot(132)
        plt.plot(self.data2)
        plt.subplot(133)
        plt.plot(self.data3)
        plt.show()

                
    def filterData(self):
        b,a = signal.butter(3,0.5,analog = False)
        #b = [1,-1]
        #a = [1,0.9]
        butter1 = (signal.filtfilt(b,a,self.data1))
        butter2 = (signal.filtfilt(b,a,self.data2))
        butter3 = (signal.filtfilt(b,a,self.data3))

        butter1 = [x / 16384.0 for x in butter1]
        butter2 = [x / 16384.0 for x in butter2]
        butter3 = [x / 16384.0 for x in butter3]
        
        return butter1, butter2, butter3
    
    def runningAverage(self,noisyData):
        smoothed = list()
        summedValues = 0
        count = 1
        L = len(noisyData)
        offset = 10 - (L % 10)
        if offset < 10:
            zer = np.zeros(offset)
            newData = np.concatenate([noisyData, zer])
        else:
            newData = noisyData
            
        for num in newData:
            if (count % 3) == 0:
                smoothed.append(summedValues/3.0)
                summedValues = 0
            count += 1
            summedValues += num
        
        return smoothed

    def getVelocity(self,accel,recordTime):
        Fs = len(accel) / recordTime
        time = np.linspace(0,recordTime,len(accel))
        velocity = list()
        velocity.append(0.0)
        n = 0
        for ax in accel:
            vCurrent = velocity[n] + (ax * time[n])
            velocity.append(vCurrent)
            n +=1
        return time,np.array(velocity[1:])

    def getPosition(self,time,vel,accel):
        n = 0;
        pos = list()
        pos.append(0.0)
        for velocity in vel:
            aPosition = accel[n] * (pow(time[n],2))
            vPosition = velocity * time[n]
            newPos = pos[n] + vPosition + (0.5 * aPosition)
            pos.append(newPos)
            n += 1
        return pos[1:]

    def calculateShift(self,data):
        minVal = 10000
        maxVal = 0

        for i in data:
            if abs(i) < abs(minVal):
                minVal = i

            if abs(i) > abs(maxVal):
                maxVal = i

                
            shiftValue = maxVal - ((maxVal - minVal) / 2)
        return shiftValue

axOff = list()
ayOff = list()
azOff = list()
data1 = list()
data2 = list()
data3 = list()

with open('CalibrationSignal.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        axOff.append(float(row[0]))
        ayOff.append(float(row[1]))
        azOff.append(float(row[2]))

with open('IMUDataFar_iD.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))
t = np.linspace(0,120,len(axOff))
axOff = [x / 16384 for x in axOff]
ayOff = [x / 16384 for x in ayOff]
azOff = [x / 16384 for x in azOff]

plt.subplot(311)
plt.plot(t,axOff)
plt.title("X Accelerometer Calibration Signal")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(312)
plt.plot(t,ayOff)
plt.title("Y Accelerometer Calibration Signal")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(313)
plt.plot(t,azOff)
plt.title("Z Accelerometer Calibration Signal")
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude (m/s^2)")
##mpu = IMU()
##mpu.setTime(120.0)
##mpu.calcOffsets(axOff,ayOff,azOff)
##mpu.setAcceleration(data1,data2,data3)
##X,Y,Z = mpu.getAcceleration()


##plt.subplot(231)
##plt.plot(data1)
##plt.title("X Accelerometer Non-Filtered")
##plt.subplot(232)
##plt.plot(data2)
##plt.title("Y Accelerometer Non-Filtered")
##plt.subplot(233)
##plt.plot(data3)
##plt.title("Z Accelerometer Non-Filtered")
##plt.subplot(234)
##plt.plot(X)
##plt.title("X Accelerometer Filtered")
##plt.subplot(235)
##plt.plot(Y)
##plt.title("X Accelerometer Filtered")
##plt.subplot(236)
##plt.plot(Z)
##plt.title("X Accelerometer Filtered")

plt.show()
