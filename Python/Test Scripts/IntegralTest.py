from scipy import integrate
from scipy import interpolate
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from IMU import IMU
import csv

# my data
axOff = list()
ayOff = list()
azOff = list()
data1 = list()
data2 = list()
data3 = list()
originTap = list()


with open('..\Data\CalibrationSignal.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        axOff.append(float(row[0]))
        ayOff.append(float(row[1]))
        azOff.append(float(row[2]))

with open('..\Data\IMUData60cm_x.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))
        originTap.append(int(row[6]))
        
interval = 30.0     
mpu = IMU()
mpu.setTime(interval)
idx = mpu.originIndices(originTap)
mpu.calcOffsets(axOff,ayOff,azOff)
mpu.setAcceleration(data1,data2,data3)
Ax,Ay,Az = mpu.getAcceleration()

t = np.array(mpu.time)
x_vel = integrate.cumtrapz(t, Ax, initial=0)
x_Trap = integrate.cumtrapz(t,x_vel, initial=0)
f = interpolate.interp1d(t, Ax)
x_vel = [0]
totalSum = 0
dt = len(Ax) / 30.0
x_vel = [sum(Ax[:i]) * -dt for i in range(len(Ax))]
x_pos = [sum(x_vel[:i]) * dt for i in range(len(x_vel))]

x2_vel,y2_vel,z2_vel = mpu.getVelocity()
x2_pos,y2_pos,z2_pos = mpu.getPosition()
print x2_pos
    
##y_vel = integrate.cumtrapz(t, y, initial=0)
##y_pos = integrate.cumtrapz(y_vel,t, initial=0)
##
##z_vel = integrate.cumtrapz(t, z, initial=0)
##z_pos = integrate.cumtrapz(z_vel,t, initial=0)

#x_pos = mpu.reduceError(x_pos,y_pos,z_pos)

##plt.plot(x_pos,y_pos)
##print idx
##for i in range(0,len(idx) - 1,2):
##    if (i + 1) > (len(idx)-1):
##        break
##    else:
##        for n in range(idx[i],idx[i+1]):
##            x_pos[n] = 0
##fc = 0.1
plt.subplot(211)
plt.plot(t,x2_pos)
plt.subplot(212)
plt.plot(t,x_pos)
plt.show()
