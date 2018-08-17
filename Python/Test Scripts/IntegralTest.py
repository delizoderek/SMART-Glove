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


with open('CalibrationSignal.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        axOff.append(float(row[0]))
        ayOff.append(float(row[1]))
        azOff.append(float(row[2]))

with open('IMUData60cm_x.csv','rb') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))
        originTap.append(int(row[6]))
        

##x_vel = integrate.cumtrapz(t, Ax, initial=0)
##x_Trap = integrate.cumtrapz(t,x_vel, initial=0)
mpu = IMU()
mpu.calcOffsets(axOff,ayOff,azOff)
mpu.setTime(30.0)
mpu.setAcceleration(data1,data2,data3)
Ax,Ay,Az = mpu.getAcceleration()
totalSum = 0
dt = len(Ax) / 30.0

t = mpu.time

x_vel = [sum(Ax[:i]) * -dt for i in range(len(Ax))]
x_pos = [sum(x_vel[:i]) * dt for i in range(len(x_vel))]
    
y_vel = [sum(Ay[:i]) * dt for i in range(len(Ay))]
y_pos = [sum(y_vel[:i]) * dt for i in range(len(y_vel))]

z_vel = [sum(Az[:i]) * -dt for i in range(len(Az))]
z_pos = [sum(z_vel[:i]) * dt for i in range(len(z_vel))]
##x_vel = [sum(Ax[:i]) * -dt for i in range(len(Ax))]
##x_pos = [sum(x_vel[:i]) * dt for i in range(len(x_vel))]
##    
##y_vel = [sum(Ay[:i]) * dt for i in range(len(Ay))]
##y_pos = [sum(y_vel[:i]) * dt for i in range(len(y_vel))]
##
##z_vel = [sum(Az[:i]) * -dt for i in range(len(Az))]
##z_pos = [sum(z_vel[:i]) * dt for i in range(len(z_vel))]


##plt.plot(x_pos,y_pos)
##print idx
##for i in range(0,len(idx) - 1,2):
##    if (i + 1) > (len(idx)-1):
##        break
##    else:
##        for n in range(idx[i],idx[i+1]):
##            x_pos[n] = 0
##fc = 0.1
plt.figure(1)
plt.subplot(331)
plt.plot(t,Ax)
plt.title("X Acceleration Not-Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(332)
plt.plot(t,Ay)
plt.title("Y Acceleration Not-Bounded")
plt.subplot(333)
plt.plot(t,Az)
plt.title("Z Acceleration Not-Bounded")
plt.subplot(334)
plt.plot(t,x_vel)
plt.title("X Velocity Not-Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(335)
plt.plot(t,y_vel)
plt.title("Y Velocity Not-Bounded")
plt.subplot(336)
plt.plot(t,z_vel)
plt.title("Z Velocity Not-Bounded")
plt.subplot(337)
plt.plot(t,x_pos)
plt.title("X Position Not-Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.xlabel("Time (sec)")
plt.subplot(338)
plt.plot(t,y_pos)
plt.title("Y Position Not-Bounded")
plt.xlabel("Time (sec)")
plt.subplot(339)
plt.plot(t,z_pos)
plt.title("Z Position Not-Bounded")
plt.xlabel("Time (sec)")

mpu.applyBounding()

Ax,Ay,Az = mpu.getAcceleration()

x_vel = [sum(Ax[:i]) * -dt for i in range(len(Ax))]
x_pos = [sum(x_vel[:i]) * dt for i in range(len(x_vel))]
    
y_vel = [sum(Ay[:i]) * dt for i in range(len(Ay))]
y_pos = [sum(y_vel[:i]) * dt for i in range(len(y_vel))]

z_vel = [sum(Az[:i]) * -dt for i in range(len(Az))]
z_pos = [sum(z_vel[:i]) * dt for i in range(len(z_vel))]


plt.figure(2)
plt.subplot(331)
plt.plot(t,Ax)
plt.title("X Acceleration Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(332)
plt.plot(t,Ay)
plt.title("Y Acceleration Bounded")
plt.subplot(333)
plt.plot(t,Az)
plt.title("Z Acceleration Bounded")
plt.subplot(334)
plt.plot(t,x_vel)
plt.title("X Velocity Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.subplot(335)
plt.plot(t,y_vel)
plt.title("Y Velocity Bounded")
plt.subplot(336)
plt.plot(t,z_vel)
plt.title("Z Velocity Bounded")
plt.subplot(337)
plt.plot(t,x_pos)
plt.title("X Position Bounded")
plt.ylabel("Amplitude (m/s^2)")
plt.xlabel("Time (sec)")
plt.subplot(338)
plt.plot(t,y_pos)
plt.title("Y Position Bounded")
plt.xlabel("Time (sec)")
plt.subplot(339)
plt.plot(t,z_pos)
plt.title("Z Position Bounded")
plt.xlabel("Time (sec)")
plt.show()
