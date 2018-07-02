import matplotlib as mpl
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

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
