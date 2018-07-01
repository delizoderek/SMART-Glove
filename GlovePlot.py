from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x,y,z = [1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1],[1,2,3,4,5,6,7,8,9,10]
ax.plot_wireframe(x,y,z)

plt.show()

