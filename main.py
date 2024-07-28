#test
import matplotlib.pyplot as plt
import numpy as np

#plot 1:
y1 = np.array([3, 8, 1, 10])
y2 = np.array([6, 2, 7, 11])

plt.subplot(1, 2, 1)

plt.plot(y1, linestyle = "dashed", marker = "*", \
	markersize = 10, mec = "red", mfc = "blue", \
	color = "purple", linewidth = 2)

plt.plot(y2)

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("Sports Watch Data", fontdict = font1, loc = 'left')
plt.xlabel("Average Pulse", fontdict = font2)
plt.ylabel("Calorie Burnage", fontdict = font2)

plt.grid(axis = "x", linestyle = "--", color = "red", \
		 linewidth = 1)

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])

plt.subplot(1, 2, 2)
plt.plot(x, y)

plt.suptitle("MY SHOP")

plt.show()