import numpy as np

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

    def calcAxOffset(self,Ax):
        maxAx = max(Ax)
        minAx = min(Ax)

        dAx = (maxAx - minAx) / 2.0
        self.axShift = maxAx - dAx

    def calcAyOffset(self,Ay):
        maxAy = max(Ay)
        minAy = min(Ay)

        dAy = (maxAy - minAy) / 2.0
        self.ayShift = maxAy - dAy

    def calcAzOffset(self,Az):
        maxAz = max(Az)
        minAz = min(Az)

        dAz = (maxAz - minAz) / 2.0
        self.azShift = maxAz - dAz
        
    def setAcceleration(self,Ax,Ay,Az):
        self.ax = [x - self.axShift for x in Ax]
        self.ay = [y - self.ayShift for y in Ay]
        self.az = [z - self.azShift for z in Az]

    def getOffsets(self):
        print "X Offset: ",self.axShift," Y Offset: ",self.ayShift," Z Offset: ",self.azShift
