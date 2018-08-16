import matplotlib as mpl
import csv
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# Net vertical displacement
# net horizontal displacement
# Avergae Time Between taps
# Time to complete a full cycle

def plotMulti():
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    x = t = np.linspace(0,11,12)
    z = -1 * (t)*(t-10)
    ax.set_xlim([0,20])
    ax.set_ylim([0,20])
    ax.set_zlim([0,30])
    ax.plot(x, t, z, label='parametric curve')
    ax.legend()

    plt.show()


def reccurringPlot(data1,data2,data3):
    plt.ion() ## Note this correction
    fig=plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_zlim([0,30])
    i=0
    x=list()
    y=list()
    z=list()

    while i < len(data1):
        x.append(data1[i])
        y.append(data2[i])
        z.append(data3[i])
        i+=1;
        ax.plot(x, y, z)
        plt.show()
        plt.pause(0.1) #Note this correction
    # plt.close(fig)

data1=list()
data2=list()
data3=list()
with open('Test.csv','rU') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        data1.append(float(row[0]))
        data2.append(float(row[1]))
        data3.append(float(row[2]))

reccurringPlot(data1,data2,data3)
