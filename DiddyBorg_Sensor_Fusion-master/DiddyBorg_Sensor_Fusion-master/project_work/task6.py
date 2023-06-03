import csv
import numpy as np
import math as mat
import matplotlib.pyplot as plt

csv_file1 = open('../../data/task6/motor_control_tracking_task6.csv')
csv_reader1 = csv.reader(csv_file1)
csv_file2 = open('../../data/task6/imu_tracking_task6.csv')
csv_reader2 = csv.reader(csv_file2)

motor_data_reading = []
for raw in csv_reader1:
    motor_data_reading.append(raw)
motor_data = [[float(x) for x in row] for row in motor_data_reading]
motor_data = np.array(motor_data)

imu_data_reading = []
for raw in csv_reader2:
    imu_data_reading.append(raw)
imu_data = [[float(x) for x in row] for row in imu_data_reading]
imu_data = np.array(imu_data)

imu_Z_gyro = imu_data[4190:6142, 8]
imu_Z_gyro = 2.8*imu_Z_gyro*2*np.pi/360
motor_wheel = motor_data[25:268, 1:3]
motor_wheel_expand = motor_wheel.repeat(8, axis=0)
wheel_speed = np.sqrt(np.square(motor_wheel_expand[:,0]) + np.square(motor_wheel_expand[:,1]))

dt = 0.05
X_init = 15.8
Y_init = 50
fi_init = np.pi/2

X = np.zeros(1945, float)
Y = np.zeros(1945, float)
fi = np.zeros(1945, float)
X[0] = X_init
Y[0] = Y_init
fi[0] = fi_init

for i in range(1944):
    X[i+1] = 7*dt*wheel_speed[i]*np.cos(fi[i]) - imu_Z_gyro[i]*(np.square(dt)/2)*wheel_speed[i]*np.sin(fi[i]) + X[i]
    Y[i+1] = 7*dt*wheel_speed[i]*np.sin(fi[i]) + imu_Z_gyro[i]*(np.square(dt)/2)*wheel_speed[i]*np.cos(fi[i]) + Y[i]
    fi[i+1] = dt*imu_Z_gyro[i] + fi[i]


plt.plot(X,Y, label='Robot-position', linewidth=0.5)
for i in range(1943):
    if i == 0:
        plt.quiver(X[i],Y[i],
               np.cos(fi[i]),np.sin(fi[i]),
                width=0.05, alpha=1,color='green',label='init_pose')
    if i%50 == 0 and i!=0:
        plt.quiver(X[i],Y[i],
               np.cos(fi[i]),np.sin(fi[i]),
                width=0.05, alpha=0.5,color='blue')
plt.quiver(X[-1],Y[-1],
               np.cos(fi[-1]),np.sin(fi[-1]),
                width=0.05, alpha=1,color='red',label='last_pose')
# ax[1,0].set_xlabel('p(x)$')
# ax[1,0].set_ylabel('p(y)$')
# plt.set_ylim(0,80)
# plt.set_xlim(0，80)
plt.legend()
plt.show()