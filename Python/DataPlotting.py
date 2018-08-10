import matplotlib
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv

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
        butter1Shift,butter2Shift,butter3Shift = self.filterData()
        
        time, velX = self.getVelocity(butter1Shift,self.dt)
        time, velY = self.getVelocity(butter2Shift,self.dt)
        time, velZ = self.getVelocity(butter3Shift,self.dt)

        xPos = self.getPosition(time,velX,butter1Shift)
        yPos = self.getPosition(time,velY,butter2Shift)
        zPos = self.getPosition(time,velZ,butter3Shift)

        plt.subplot(331)
        plt.plot(time,butter1Shift)
        plt.title("X Acceleration")
        plt.subplot(332)
        plt.plot(time,butter2Shift)
        plt.title("Y Acceleration")
        plt.subplot(333)
        plt.plot(time,butter3Shift)
        plt.title("Z Acceleration")
        plt.subplot(334)
        plt.plot(time,velX)
        plt.title("X Velocity")
        plt.subplot(335)
        plt.plot(time,velY)
        plt.title("Y Velocity")
        plt.subplot(336)
        plt.plot(time,velZ)
        plt.title("Z Velocity")
        plt.subplot(337)
        plt.plot(time, xPos)
        plt.title("X position")
        plt.subplot(338)
        plt.plot(time, yPos)
        plt.title("Y Position")
        plt.subplot(339)
        plt.plot(time, zPos)
        plt.title("Z Position")
        plt.show()

                
    def filterData(self):
        ##b,a = signal.butter(3,0.5,analog = False)
##        b = [1,-1]
##        a = [1,0.9]
##        butter1 = (signal.filtfilt(b,a,self.data1))
##        butter2 = (signal.filtfilt(b,a,self.data2))
##        butter3 = (signal.filtfilt(b,a,self.data3))
##
##        butter1 = [(x - self.xShift)/16384 for x in butter1]
##        butter1Shift = [(x/x) - 1 if (abs(x) < self.xBound) else x for x in butter1]
##
##        ## butter1Shift = runningAverage(butter1Shift)
##
##        butter2 = [(y - self.yShift)/-16384 for y in butter2]
##        butter2Shift = [(y/y) - 1 if (abs(y) < self.yBound) else y for y in butter2]
##
##        butter3 = [(z - self.zShift)/-16384 for z in butter3]
##        butter3Shift = [(z/z) - 1 if (abs(z) < self.zBound) else z for z in butter3]
        butter1Shift = self.data1;
        butter2Shift = self.data2;
        butter3Shift = self.data3;
        return butter1Shift, butter2Shift, butter3Shift
    
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


data1=list()
data2=list()
data3=list()
maxX = 0
minX = 4000
N = 150
trim = 10

with open('IMUData.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))

dp = IMUPlot(data1,data2,data3,40.0)
dp.plotData()
