
#
import numpy as np
from pointrobot.trajectory.polynomial import piecewise_2d, poly3_coefficients
import matplotlib.pyplot as plt

X = [0, 8]
Y = [0, 8]
Vx = [2.5, 0]
Vy = [-2.5, 2.51]
T = [0, 8]

# Compute trajectory
time, traj_x, traj_y, traj_dx, traj_dy = piecewise_2d(X, Y, Vx, Vy, T)

# Plot trajectory
plt.plot(traj_x, traj_y)
plt.show()
# Plot speed
plt.plot(np.sqrt(np.array(traj_dx)**2 + np.array(traj_dy)**2))
plt.show()


i = 0
print('poly 3 coefficients for x: ', poly3_coefficients(X[i], Vx[i], X[i + 1], Vx[i + 1], T[i+1]))
print('poly 3 coefficients for y: ', poly3_coefficients(Y[i], Vy[i], Y[i + 1], Vy[i + 1], T[i+1]))
