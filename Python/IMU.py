import numpy as np
from scipy import signal
import scipy.integrate as integrate

class IMU:
    def __init__(self):
        self.ax = list()
        self.ay = list()
        self.az = list()
        self.gx = list()
        self.gy = list()
        self.gz = list()
        self.axShift = 0.0
        self.ayShift = 0.0
        self.azShift = 0.0
        self.xBound = 0.0
        self.yBound = 0.0
        self.zBound = 0.0
        self.interval = 0.0
        self.time = list()
        self.originIdx = list()
    
    def calcOffsets(self,Ax,Ay,Az):
        meanAx = np.mean(Ax)
        meanAy = np.mean(Ay)
        meanAz = np.mean(Az)
        
        self.axShift = meanAx
        self.ayShift = meanAy
        self.azShift = meanAz = np.mean(Az)

        Ax = [x - self.axShift for x in Ax]
        Ay = [y - self.ayShift for y in Ay]
        Az = [z - self.azShift for z in Az]

        self.xBound = max(Ax)
        self.yBound = max(Ay)
        self.zBound = max(Az)
        
    def setAcceleration(self,Ax,Ay,Az):
        Ax = [x - self.axShift for x in Ax]
        Ay = [y - self.ayShift for y in Ay]
        Az = [z - self.azShift for z in Az]
        Ax = [x / 16384 for x in Ax]
        Ay = [y / 16384 for y in Ay]
        Az = [z / 16384 for z in Az]
        self.time = np.linspace(0,self.interval,len(Ax))
        self.ax = Ax
        self.ay = Ay
        self.az = Az

    def applyBounding(self):
        self.ax = [x*0 if abs(x) < self.xBound / 16384 else x for x in self.ax]
        self.ay = [y*0 if abs(y) < self.yBound / 16384 else y for y in self.ay]
        self.az = [z*0 if abs(z) < self.zBound / 16384 else z for z in self.az]
    
    def originIndices(self,originTracker):
        indices = list()
        n = 0
        for origin in originTracker:
            if origin == 1:
                indices.append(n)
            n += 1
        self.originIdx = indices
        return indices

    def reduceError(self,xp,yp,zp):
        b = [1,-1]
        a = [1,0.9]

        return signal.filtfilt(b,a,xp)
    
    def getAcceleration(self):
        return self.ax, self.ay, self.az
        
    def setTime(self,dTime):
        self.interval = dTime
    
    def getOffsets(self):
        print "X Offset: ",self.axShift," Y Offset: ",self.ayShift," Z Offset: ",self.azShift
