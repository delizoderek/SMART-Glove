import matplotlib
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv

def runningAverage(noisyData):
    smoothed = list()
    summedValues = 0
    count = 1
    L = len(noisyData)
    print L
    offset = 10 - (L % 10)
    print offset
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
        

data1=list()
data2=list()
data3=list()
maxX = 0
minX = 4000
N = 150
trim = 10
with open('IMUData.csv','rU') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))

for i in range(0,N-1):
    if maxX < data1[i]:
        maxX = data1[i]

    if minX > data1[i]:
        minX = data1[i]

shiftVal = maxX - ((maxX - minX) / 2)

data1[:] = [x - shiftVal for x in data1]

b = [1,-1]
a = [1,0.9]

filter1 = runningAverage(data1)
filter2 = runningAverage(data2)
filter3 = runningAverage(data3)

filter1 = filter1[trim:len(filter1) - (trim+1)]
filter2 = filter2[trim:len(filter2) - (trim+1)]
filter3 = filter3[trim:len(filter3) - (trim+1)]

filter1 = [(x - 8680)/16384 for x in filter1]
filter2 = [(y + 2070)/16384 for y in filter2]
filter3 = [(z + 15877)/16384 for z in filter3]

butter1 = (signal.filtfilt(b,a,filter1))
butter2 = (signal.filtfilt(b,a,filter2))
butter3 = (signal.filtfilt(b,a,filter3))

print "Max X Accel: ", maxX, " Min X Accel: ", minX
plt.subplot(331)
plt.plot(data1)
plt.title("Non-Filtered Accelerometer X")
plt.subplot(332)
plt.plot(data2)
plt.title("Non-Filtered Accelerometer Y")
plt.subplot(333)
plt.plot(data3)
plt.title("Non-Filtered Accelerometer Z")
plt.subplot(334)
plt.plot(filter1)
plt.title("Filtered Accelerometer X")
plt.subplot(335)
plt.plot(filter2)
plt.title("Filtered Accelerometer Y")
plt.subplot(336)
plt.plot(filter3)
plt.title("Filtered Accelerometer Z")
plt.subplot(337)
plt.plot(butter1)
plt.title("Butter-Filtered Accelerometer X")
plt.subplot(338)
plt.plot(butter2)
plt.title("Butter-Filtered Accelerometer Y")
plt.subplot(339)
plt.plot(butter3)
plt.title("Butter-Filtered Accelerometer Z")
plt.show()


